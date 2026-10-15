import subprocess
import sys
import os

# ✅ 𝐀𝐮𝐭𝐨-𝐢𝐧𝐬𝐭𝐚𝐥𝐥 𝐦𝐢𝐬𝐬𝐢𝐧𝐠 𝐦𝐨𝐝𝐮𝐥𝐞𝐬
def auto_install(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        print(f"📦 Installing missing package: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed: {package}")

# Auto-install required modules
for mod in ["discord.py", "psutil", "requests", "flask"]:
    auto_install(mod)

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import zipfile
import tempfile
import shutil
import time
from datetime import datetime, timedelta
import psutil
import sqlite3
import json
import logging
import threading
import re
import atexit
import requests
from flask import Flask
from threading import Thread
import hashlib
import random
import string

app = Flask('')

@app.route('/')
def home():
    return "𝐈'𝐦 𝐓𝐈𝐓𝐀𝐍 𝐇𝐎𝐒𝐓𝐈𝐍𝐆 𝐃𝐈𝐒𝐂𝐎𝐑𝐃 𝐁𝐎𝐓"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("✅ Flask Keep-Alive server started.")

# ================================
# CONFIGURATION
# ================================
TOKEN = 'MTUyNTgwNzI1MDg5NDA5NDQyNw.Gx46fs.VsBVt48mhBXXXWxsiGcVyTyReY6GSFbatYtWxA'
OWNER_ID = 1139336441927827587
ADMIN_IDS = {1139336441927827587}
BOT_NAME = "TITAN"

# Folder setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BOTS_DIR = os.path.join(BASE_DIR, 'titan_uploads')
TITAN_DATA_DIR = os.path.join(BASE_DIR, 'titan_data')
DATABASE_PATH = os.path.join(TITAN_DATA_DIR, 'titan_bot.db')

# Create necessary directories
os.makedirs(UPLOAD_BOTS_DIR, exist_ok=True)
os.makedirs(TITAN_DATA_DIR, exist_ok=True)

# --- Data structures ---
bot_scripts = {}
user_files = {}
active_users = set()
bot_locked = False

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ================================
# DISCORD BOT SETUP
# ================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove default help command
bot.remove_command('help')

# ================================
# DATABASE SETUP
# ================================
def init_db():
    logger.info(f"📊 Initializing database at: {DATABASE_PATH}")
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_files
                     (user_id INTEGER, file_name TEXT, file_type TEXT, uploaded_at TEXT,
                      PRIMARY KEY (user_id, file_name))''')
        c.execute('''CREATE TABLE IF NOT EXISTS active_users
                     (user_id INTEGER PRIMARY KEY, username TEXT, first_join TEXT, last_seen TEXT)''')
        conn.commit()
        conn.close()
        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}", exc_info=True)

def load_data():
    logger.info("📥 Loading data from database...")
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute('SELECT user_id, file_name, file_type FROM user_files')
        for user_id, file_name, file_type in c.fetchall():
            if user_id not in user_files:
                user_files[user_id] = []
            user_files[user_id].append((file_name, file_type))
        c.execute('SELECT user_id FROM active_users')
        active_users.update(user_id for (user_id,) in c.fetchall())
        conn.close()
        logger.info(f"✅ Data loaded: {len(active_users)} users, {sum(len(files) for files in user_files.values())} files")
    except Exception as e:
        logger.error(f"❌ Error loading data: {e}", exc_info=True)

init_db()
load_data()

# ================================
# HELPER FUNCTIONS
# ================================
def get_user_folder(user_id):
    user_folder = os.path.join(UPLOAD_BOTS_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def is_bot_running(user_id, file_name):
    script_key = f"{user_id}_{file_name}"
    script_info = bot_scripts.get(script_key)
    if script_info and script_info.get('process'):
        try:
            proc = psutil.Process(script_info['process'].pid)
            return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            if script_key in bot_scripts:
                del bot_scripts[script_key]
            return False
    return False

def kill_process_tree(process_info):
    try:
        process = process_info.get('process')
        if process and hasattr(process, 'pid'):
            pid = process.pid
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.terminate()
                    except:
                        pass
                try:
                    parent.terminate()
                    parent.wait(timeout=3)
                except:
                    try:
                        parent.kill()
                    except:
                        pass
            except psutil.NoSuchProcess:
                pass
    except Exception as e:
        logger.error(f"❌ Error killing process: {e}")

def save_user_file(user_id, file_name, file_type='py'):
    with sqlite3.connect(DATABASE_PATH, check_same_thread=False) as conn:
        c = conn.cursor()
        try:
            c.execute('''INSERT OR REPLACE INTO user_files 
                         (user_id, file_name, file_type, uploaded_at) 
                         VALUES (?, ?, ?, ?)''',
                      (user_id, file_name, file_type, datetime.now().isoformat()))
            conn.commit()
            if user_id not in user_files:
                user_files[user_id] = []
            user_files[user_id] = [(fn, ft) for fn, ft in user_files[user_id] if fn != file_name]
            user_files[user_id].append((file_name, file_type))
            logger.info(f"💾 Saved file '{file_name}' for user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error saving file: {e}")

def remove_user_file_db(user_id, file_name):
    with sqlite3.connect(DATABASE_PATH, check_same_thread=False) as conn:
        c = conn.cursor()
        try:
            c.execute('DELETE FROM user_files WHERE user_id = ? AND file_name = ?', 
                      (user_id, file_name))
            conn.commit()
            if user_id in user_files:
                user_files[user_id] = [f for f in user_files[user_id] if f[0] != file_name]
                if not user_files[user_id]:
                    del user_files[user_id]
            logger.info(f"🗑️ Removed file '{file_name}' for user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error removing file: {e}")

def add_active_user(user_id, username=None):
    active_users.add(user_id)
    with sqlite3.connect(DATABASE_PATH, check_same_thread=False) as conn:
        c = conn.cursor()
        try:
            c.execute('''INSERT OR REPLACE INTO active_users 
                         (user_id, username, first_join, last_seen) 
                         VALUES (?, ?, COALESCE((SELECT first_join FROM active_users WHERE user_id = ?), ?), ?)''',
                      (user_id, username, user_id, datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
            logger.info(f"👤 Added active user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error adding active user: {e}")

# ================================
# REQUIREMENTS INSTALLER
# ================================
def install_requirements(user_folder, interaction=None, message=None):
    """Install requirements from requirements.txt if found"""
    req_files = ['requirements.txt', 'requirement.txt']
    installed = False
    
    for req_file in req_files:
        req_path = os.path.join(user_folder, req_file)
        if os.path.exists(req_path):
            logger.info(f"📦 Found {req_file} in {user_folder}, installing...")
            try:
                # Install requirements
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", req_path],
                    cwd=user_folder,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    installed = True
                    logger.info(f"✅ Successfully installed requirements from {req_file}")
                    if interaction:
                        asyncio.run_coroutine_threadsafe(
                            interaction.followup.send(f"✅ Installed requirements from `{req_file}`"),
                            bot.loop
                        )
                    elif message:
                        asyncio.run_coroutine_threadsafe(
                            message.reply(f"✅ Installed requirements from `{req_file}`"),
                            bot.loop
                        )
                else:
                    logger.error(f"❌ Failed to install requirements from {req_file}: {result.stderr}")
                    if interaction:
                        asyncio.run_coroutine_threadsafe(
                            interaction.followup.send(f"⚠️ Failed to install requirements from `{req_file}`: {result.stderr[:200]}"),
                            bot.loop
                        )
                    elif message:
                        asyncio.run_coroutine_threadsafe(
                            message.reply(f"⚠️ Failed to install requirements: {result.stderr[:200]}"),
                            bot.loop
                        )
            except subprocess.TimeoutExpired:
                logger.error(f"❌ Timeout installing requirements from {req_file}")
                if interaction:
                    asyncio.run_coroutine_threadsafe(
                        interaction.followup.send(f"⏰ Timeout installing requirements from `{req_file}`"),
                        bot.loop
                    )
                elif message:
                    asyncio.run_coroutine_threadsafe(
                        message.reply(f"⏰ Timeout installing requirements"),
                        bot.loop
                    )
            except Exception as e:
                logger.error(f"❌ Error installing requirements: {e}")
            
            break  # Stop after finding and processing one requirements file
    
    return installed

# ================================
# SCRIPT RUNNING SYSTEM
# ================================
def run_script(script_path, user_id, user_folder, file_name, interaction):
    try:
        if not os.path.exists(script_path):
            asyncio.run_coroutine_threadsafe(
                interaction.followup.send(f"❌ File not found: `{file_name}`"),
                bot.loop
            )
            return
        
        # Install requirements first
        install_requirements(user_folder, interaction=interaction)
        
        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=user_folder,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8',
            errors='ignore'
        )
        
        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'py',
            'script_key': script_key
        }
        
        asyncio.run_coroutine_threadsafe(
            interaction.followup.send(f"✅ Python script `{file_name}` started!\n📊 PID: `{process.pid}`"),
            bot.loop
        )
        
    except Exception as e:
        asyncio.run_coroutine_threadsafe(
            interaction.followup.send(f"❌ Error starting script: {str(e)}"),
            bot.loop
        )

def run_js_script(script_path, user_id, user_folder, file_name, interaction):
    try:
        if not os.path.exists(script_path):
            asyncio.run_coroutine_threadsafe(
                interaction.followup.send(f"❌ File not found: `{file_name}`"),
                bot.loop
            )
            return
        
        # Install requirements if package.json exists
        package_json = os.path.join(user_folder, 'package.json')
        if os.path.exists(package_json):
            try:
                asyncio.run_coroutine_threadsafe(
                    interaction.followup.send(f"📦 Found `package.json`, installing npm dependencies..."),
                    bot.loop
                )
                npm_result = subprocess.run(
                    ['npm', 'install'],
                    cwd=user_folder,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if npm_result.returncode == 0:
                    asyncio.run_coroutine_threadsafe(
                        interaction.followup.send(f"✅ npm dependencies installed"),
                        bot.loop
                    )
                else:
                    asyncio.run_coroutine_threadsafe(
                        interaction.followup.send(f"⚠️ npm install error: {npm_result.stderr[:200]}"),
                        bot.loop
                    )
            except Exception as e:
                logger.error(f"❌ npm install error: {e}")
        
        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            ['node', script_path],
            cwd=user_folder,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8',
            errors='ignore'
        )
        
        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'js',
            'script_key': script_key
        }
        
        asyncio.run_coroutine_threadsafe(
            interaction.followup.send(f"✅ JS script `{file_name}` started!\n📊 PID: `{process.pid}`"),
            bot.loop
        )
        
    except Exception as e:
        asyncio.run_coroutine_threadsafe(
            interaction.followup.send(f"❌ Error starting JS script: {str(e)}"),
            bot.loop
        )

# ================================
# DISCORD EVENTS
# ================================

@bot.event
async def on_ready():
    logger.info(f"🤖 {bot.user} is ready!")
    logger.info(f"📊 Logged in as: {bot.user.name}")
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        logger.info(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        logger.error(f"❌ Failed to sync slash commands: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.attachments:
        await handle_file_upload(message)

# ================================
# SLASH COMMANDS - ADMIN ONLY
# ================================

@bot.tree.command(name="lock", description="Lock the bot (Admin only)")
@app_commands.default_permissions(administrator=True)
async def slash_lock(interaction: discord.Interaction):
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    global bot_locked
    bot_locked = True
    embed = discord.Embed(title="🔒 BOT LOCKED", description="No new uploads will be accepted.", color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="unlock", description="Unlock the bot (Admin only)")
@app_commands.default_permissions(administrator=True)
async def slash_unlock(interaction: discord.Interaction):
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    global bot_locked
    bot_locked = False
    embed = discord.Embed(title="🔓 BOT UNLOCKED", description="Uploads are now accepted.", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stop", description="Stop a running script")
@app_commands.default_permissions(administrator=True)
async def slash_stop(interaction: discord.Interaction, file_name: str):
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user_id = interaction.user.id
    if not is_bot_running(user_id, file_name):
        embed = discord.Embed(title="❌ NOT RUNNING", description=f"Script `{file_name}` is not running.", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        return
    
    script_key = f"{user_id}_{file_name}"
    if script_key in bot_scripts:
        kill_process_tree(bot_scripts[script_key])
        del bot_scripts[script_key]
    
    embed = discord.Embed(title="🛑 SCRIPT STOPPED", description=f"Stopped `{file_name}`.", color=discord.Color.orange())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="restart", description="Restart a running script")
@app_commands.default_permissions(administrator=True)
async def slash_restart(interaction: discord.Interaction, file_name: str):
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user_id = interaction.user.id
    
    # Stop if running
    if is_bot_running(user_id, file_name):
        script_key = f"{user_id}_{file_name}"
        if script_key in bot_scripts:
            kill_process_tree(bot_scripts[script_key])
            del bot_scripts[script_key]
        await asyncio.sleep(1)
    
    # Start again
    user_folder = get_user_folder(user_id)
    file_path = os.path.join(user_folder, file_name)
    
    if not os.path.exists(file_path):
        embed = discord.Embed(title="❌ FILE NOT FOUND", description=f"File `{file_name}` not found.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    # Find file type
    file_type = 'py'
    for fname, ftype in user_files.get(user_id, []):
        if fname == file_name:
            file_type = ftype
            break
    
    await interaction.response.defer()
    
    if file_type == 'py':
        threading.Thread(target=run_script, args=(file_path, user_id, user_folder, file_name, interaction)).start()
    elif file_type == 'js':
        threading.Thread(target=run_js_script, args=(file_path, user_id, user_folder, file_name, interaction)).start()
    else:
        await interaction.followup.send(f"❌ Unsupported file type: {file_type}")

@bot.tree.command(name="delete", description="Delete a file (Admin only)")
@app_commands.default_permissions(administrator=True)
async def slash_delete(interaction: discord.Interaction, file_name: str):
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user_id = interaction.user.id
    
    # Check if file exists
    files = user_files.get(user_id, [])
    file_exists = False
    for fname, ftype in files:
        if fname == file_name:
            file_exists = True
            break
    
    if not file_exists:
        embed = discord.Embed(title="❌ FILE NOT FOUND", description=f"File `{file_name}` not found.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return
    
    # Stop if running
    if is_bot_running(user_id, file_name):
        script_key = f"{user_id}_{file_name}"
        if script_key in bot_scripts:
            kill_process_tree(bot_scripts[script_key])
            del bot_scripts[script_key]
    
    # Delete file
    user_folder = get_user_folder(user_id)
    file_path = os.path.join(user_folder, file_name)
    log_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
    
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(log_path):
        os.remove(log_path)
    
    remove_user_file_db(user_id, file_name)
    
    embed = discord.Embed(title="🗑️ FILE DELETED", description=f"File `{file_name}` has been deleted.", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="restartbot", description="Restart the bot (Admin only)")
@app_commands.default_permissions(administrator=True)
async def slash_restart_bot(interaction: discord.Interaction):
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="🔄 RESTARTING BOT", description="Bot will now restart...", color=discord.Color.orange())
    await interaction.response.send_message(embed=embed)
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.tree.command(name="reset", description="Reset all bot data (Admin only)")
@app_commands.default_permissions(administrator=True)
async def slash_reset(interaction: discord.Interaction):
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    class ResetView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
            self.confirmed = False
        
        @discord.ui.button(label="✅ Confirm Reset", style=discord.ButtonStyle.danger)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.confirmed = True
            await interaction.response.edit_message(content="🔄 **Resetting data...**", view=None)
            self.stop()
        
        @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.edit_message(content="❌ **Reset cancelled.**", view=None)
            self.stop()
    
    embed = discord.Embed(
        title="⚠️ WARNING: DATA RESET",
        description="This will delete **ALL** data including:\n"
                   "• All uploaded files\n"
                   "• All user data\n"
                   "• All running scripts\n\n"
                   "**This action cannot be undone!**",
        color=discord.Color.red()
    )
    
    view = ResetView()
    await interaction.response.send_message(embed=embed, view=view)
    await view.wait()
    
    if view.confirmed:
        try:
            # Stop all running scripts
            for key, info in list(bot_scripts.items()):
                try:
                    kill_process_tree(info)
                except:
                    pass
            bot_scripts.clear()
            
            # Delete data folders
            if os.path.exists(TITAN_DATA_DIR):
                shutil.rmtree(TITAN_DATA_DIR)
            if os.path.exists(UPLOAD_BOTS_DIR):
                shutil.rmtree(UPLOAD_BOTS_DIR)
            
            # Clear memory data
            user_files.clear()
            active_users.clear()
            
            # Recreate folders
            os.makedirs(TITAN_DATA_DIR, exist_ok=True)
            os.makedirs(UPLOAD_BOTS_DIR, exist_ok=True)
            
            # Reinitialize database
            init_db()
            load_data()
            
            embed = discord.Embed(
                title="✅ DATA RESET COMPLETE",
                description="All bot data has been successfully reset!",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ RESET ERROR",
                description=f"Failed to reset data: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)

# ================================
# BOT LIST FUNCTIONS
# ================================

async def show_bot_list(interaction):
    """Show bot list - reusable function"""
    if interaction.user.id not in ADMIN_IDS:
        embed = discord.Embed(title="⚠️ PERMISSION DENIED", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user_id = interaction.user.id
    files = user_files.get(user_id, [])
    
    if not files:
        embed = discord.Embed(
            title="📂 NO BOTS FOUND",
            description="You haven't uploaded any bots yet.\nUpload a .py, .js, or .zip file to get started!",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🤖 YOUR BOTS",
        description=f"Total: **{len(files)}** bots",
        color=discord.Color.blue()
    )
    
    online_count = 0
    offline_count = 0
    
    bot_list_text = ""
    for file_name, file_type in files:
        is_running = is_bot_running(user_id, file_name)
        if is_running:
            online_count += 1
            status = "🟢 **ONLINE**"
        else:
            offline_count += 1
            status = "🔴 **OFFLINE**"
        
        bot_list_text += f"📄 `{file_name}` ({file_type}) - {status}\n"
    
    embed.add_field(name="📊 Status", value=f"🟢 Online: {online_count}\n🔴 Offline: {offline_count}", inline=False)
    embed.add_field(name="📁 Files", value=bot_list_text or "No files", inline=False)
    embed.set_footer(text="Use the buttons below to control your bots")
    
    # Create buttons for each file
    view = discord.ui.View(timeout=120)
    
    for file_name, file_type in files:
        is_running = is_bot_running(user_id, file_name)
        status_emoji = "🟢" if is_running else "🔴"
        
        # Create a button for each bot
        button = discord.ui.Button(
            label=f"{status_emoji} {file_name[:20]}", 
            style=discord.ButtonStyle.primary if is_running else discord.ButtonStyle.secondary,
            custom_id=f"bot_{user_id}_{file_name}"
        )
        
        async def button_callback(interaction: discord.Interaction, fn=file_name, ft=file_type, uid=user_id):
            # Create control view for this specific bot
            control_view = BotControlView(uid, fn, ft)
            control_embed = discord.Embed(
                title=f"🤖 {fn}",
                description=f"Status: {'🟢 ONLINE' if is_bot_running(uid, fn) else '🔴 OFFLINE'}\nType: {ft}",
                color=discord.Color.green() if is_bot_running(uid, fn) else discord.Color.red()
            )
            await interaction.response.send_message(embed=control_embed, view=control_view, ephemeral=True)
        
        button.callback = button_callback
        view.add_item(button)
    
    # Add refresh button
    refresh_button = discord.ui.Button(label="🔄 Refresh", style=discord.ButtonStyle.success, custom_id="refresh_list")
    async def refresh_callback(interaction: discord.Interaction):
        await show_bot_list(interaction)
    refresh_button.callback = refresh_callback
    view.add_item(refresh_button)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="list", description="Show all your bots with status and controls")
@app_commands.default_permissions(administrator=True)
async def slash_list(interaction: discord.Interaction):
    await show_bot_list(interaction)

# ================================
# BOT CONTROL VIEW
# ================================

class BotControlView(discord.ui.View):
    def __init__(self, user_id, file_name, file_type):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.file_name = file_name
        self.file_type = file_type
        self.is_running = is_bot_running(user_id, file_name)
    
    @discord.ui.button(label="▶️ Start", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id and interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ You don't have permission to control this bot!", ephemeral=True)
            return
        
        if is_bot_running(self.user_id, self.file_name):
            await interaction.response.send_message(f"✅ `{self.file_name}` is already running!", ephemeral=True)
            return
        
        user_folder = get_user_folder(self.user_id)
        file_path = os.path.join(user_folder, self.file_name)
        
        if not os.path.exists(file_path):
            await interaction.response.send_message(f"❌ File `{self.file_name}` not found!", ephemeral=True)
            return
        
        await interaction.response.send_message(f"🔄 Starting `{self.file_name}`...", ephemeral=True)
        
        if self.file_type == 'py':
            threading.Thread(target=run_script_simple, args=(file_path, self.user_id, user_folder, self.file_name, interaction, False)).start()
        elif self.file_type == 'js':
            threading.Thread(target=run_js_script_simple, args=(file_path, self.user_id, user_folder, self.file_name, interaction, False)).start()
        
        # Update the view after a moment
        await asyncio.sleep(2)
        await show_bot_list(interaction)
    
    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id and interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ You don't have permission to control this bot!", ephemeral=True)
            return
        
        if not is_bot_running(self.user_id, self.file_name):
            await interaction.response.send_message(f"❌ `{self.file_name}` is not running!", ephemeral=True)
            return
        
        script_key = f"{self.user_id}_{self.file_name}"
        if script_key in bot_scripts:
            kill_process_tree(bot_scripts[script_key])
            del bot_scripts[script_key]
        
        await interaction.response.send_message(f"🛑 Stopped `{self.file_name}`", ephemeral=True)
        
        # Update the view after a moment
        await asyncio.sleep(1)
        await show_bot_list(interaction)
    
    @discord.ui.button(label="🔄 Restart", style=discord.ButtonStyle.primary)
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id and interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ You don't have permission to control this bot!", ephemeral=True)
            return
        
        user_folder = get_user_folder(self.user_id)
        file_path = os.path.join(user_folder, self.file_name)
        
        if not os.path.exists(file_path):
            await interaction.response.send_message(f"❌ File `{self.file_name}` not found!", ephemeral=True)
            return
        
        # Stop if running
        if is_bot_running(self.user_id, self.file_name):
            script_key = f"{self.user_id}_{self.file_name}"
            if script_key in bot_scripts:
                kill_process_tree(bot_scripts[script_key])
                del bot_scripts[script_key]
            await asyncio.sleep(1)
        
        await interaction.response.send_message(f"🔄 Restarting `{self.file_name}`...", ephemeral=True)
        
        if self.file_type == 'py':
            threading.Thread(target=run_script_simple, args=(file_path, self.user_id, user_folder, self.file_name, interaction, False)).start()
        elif self.file_type == 'js':
            threading.Thread(target=run_js_script_simple, args=(file_path, self.user_id, user_folder, self.file_name, interaction, False)).start()
        
        # Update the view after a moment
        await asyncio.sleep(2)
        await show_bot_list(interaction)
    
    @discord.ui.button(label="🗑️ Delete", style=discord.ButtonStyle.secondary)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id and interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ You don't have permission to delete this bot!", ephemeral=True)
            return
        
        # Stop if running
        if is_bot_running(self.user_id, self.file_name):
            script_key = f"{self.user_id}_{self.file_name}"
            if script_key in bot_scripts:
                kill_process_tree(bot_scripts[script_key])
                del bot_scripts[script_key]
        
        # Delete file
        user_folder = get_user_folder(self.user_id)
        file_path = os.path.join(user_folder, self.file_name)
        log_path = os.path.join(user_folder, f"{os.path.splitext(self.file_name)[0]}.log")
        
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(log_path):
            os.remove(log_path)
        
        remove_user_file_db(self.user_id, self.file_name)
        
        await interaction.response.send_message(f"🗑️ Deleted `{self.file_name}`", ephemeral=True)
        
        # Update the view after a moment
        await asyncio.sleep(1)
        await show_bot_list(interaction)

# ================================
# FILE UPLOAD HANDLER
# ================================
async def handle_file_upload(message):
    user_id = message.author.id
    
    if bot_locked and user_id not in ADMIN_IDS:
        embed = discord.Embed(
            title="🔒 BOT LOCKED",
            description="The bot is currently locked. No uploads are accepted.",
            color=discord.Color.red()
        )
        await message.reply(embed=embed)
        return
    
    for attachment in message.attachments:
        if not attachment.filename:
            continue
        
        file_ext = os.path.splitext(attachment.filename)[1].lower()
        if file_ext not in ['.py', '.js', '.zip']:
            embed = discord.Embed(
                title="⚠️ UNSUPPORTED FILE",
                description="Please upload .py, .js, or .zip files only.",
                color=discord.Color.orange()
            )
            await message.reply(embed=embed)
            continue
        
        try:
            file_content = await attachment.read()
            user_folder = get_user_folder(user_id)
            file_path = os.path.join(user_folder, attachment.filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            if file_ext == '.zip':
                await handle_zip_file(file_content, attachment.filename, user_id, user_folder, message)
            elif file_ext == '.py':
                # Install requirements if exists
                install_requirements(user_folder, message=message)
                
                save_user_file(user_id, attachment.filename, 'py')
                threading.Thread(target=run_script_simple, args=(file_path, user_id, user_folder, attachment.filename, message, True)).start()
                
                embed = discord.Embed(
                    title="📤 FILE UPLOADED",
                    description=f"✅ **{attachment.filename}** uploaded!\n🔄 **Starting script...**",
                    color=discord.Color.blue()
                )
                msg = await message.reply(embed=embed)
                
                await asyncio.sleep(1)
                embed = discord.Embed(
                    title="📤 FILE UPLOADED",
                    description=f"✅ **{attachment.filename}** uploaded!\n🟢 **Bot has started successfully!**",
                    color=discord.Color.green()
                )
                await msg.edit(embed=embed)
                
            elif file_ext == '.js':
                save_user_file(user_id, attachment.filename, 'js')
                threading.Thread(target=run_js_script_simple, args=(file_path, user_id, user_folder, attachment.filename, message, False)).start()
                
                embed = discord.Embed(
                    title="📤 FILE UPLOADED",
                    description=f"✅ **{attachment.filename}** uploaded!\n🔄 **Starting script...**",
                    color=discord.Color.blue()
                )
                msg = await message.reply(embed=embed)
                
                await asyncio.sleep(1)
                embed = discord.Embed(
                    title="📤 FILE UPLOADED",
                    description=f"✅ **{attachment.filename}** uploaded!\n🟢 **Bot has started successfully!**",
                    color=discord.Color.green()
                )
                await msg.edit(embed=embed)
                
        except Exception as e:
            logger.error(f"❌ File upload error: {e}")
            embed = discord.Embed(
                title="❌ UPLOAD ERROR",
                description=f"Failed to upload: {str(e)[:200]}",
                color=discord.Color.red()
            )
            await message.reply(embed=embed)

def run_script_simple(script_path, user_id, user_folder, file_name, message, skip_requirements=False):
    try:
        if not os.path.exists(script_path):
            return
        
        # Install requirements if exists and not skipped
        if not skip_requirements:
            install_requirements(user_folder, message=message)
        
        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=user_folder,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8',
            errors='ignore'
        )
        
        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'py',
            'script_key': script_key
        }
        
        logger.info(f"✅ Python script started: {file_name} (PID: {process.pid})")
        
    except Exception as e:
        logger.error(f"❌ Error starting script {file_name}: {e}")

def run_js_script_simple(script_path, user_id, user_folder, file_name, message, skip_requirements=False):
    try:
        if not os.path.exists(script_path):
            return
        
        # Install npm dependencies if package.json exists
        if not skip_requirements:
            package_json = os.path.join(user_folder, 'package.json')
            if os.path.exists(package_json):
                try:
                    npm_result = subprocess.run(
                        ['npm', 'install'],
                        cwd=user_folder,
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    if npm_result.returncode == 0:
                        logger.info(f"✅ npm dependencies installed for {file_name}")
                    else:
                        logger.error(f"❌ npm install error: {npm_result.stderr[:200]}")
                except Exception as e:
                    logger.error(f"❌ npm install error: {e}")
        
        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            ['node', script_path],
            cwd=user_folder,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8',
            errors='ignore'
        )
        
        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'js',
            'script_key': script_key
        }
        
        logger.info(f"✅ JS script started: {file_name} (PID: {process.pid})")
        
    except Exception as e:
        logger.error(f"❌ Error starting JS script {file_name}: {e}")

async def handle_zip_file(file_content, file_name, user_id, user_folder, message):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, file_name)
        
        with open(zip_path, 'wb') as f:
            f.write(file_content)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        extracted_files = os.listdir(temp_dir)
        py_files = [f for f in extracted_files if f.endswith('.py')]
        js_files = [f for f in extracted_files if f.endswith('.js')]
        
        # ===== CHECK FOR REQUIREMENTS.TXT =====
        req_files = ['requirements.txt', 'requirement.txt']
        found_req = False
        requirements_installed = False
        
        # First, copy ALL files to user folder
        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = os.path.join(user_folder, item)
                
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        
        # NOW check for requirements and install ONLY ONCE
        for req_file in req_files:
            req_path = os.path.join(user_folder, req_file)
            if os.path.exists(req_path):
                found_req = True
                logger.info(f"📦 Found {req_file} in ZIP")
                
                # Install requirements ONLY ONCE
                req_installed = install_requirements(user_folder, message=message)
                if req_installed:
                    requirements_installed = True
                    await message.reply(f"✅ Installed requirements from `{req_file}`")
                break
        
        main_script = None
        file_type = None
        
        for name in ['main.py', 'bot.py', 'app.py']:
            if name in py_files:
                main_script = name
                file_type = 'py'
                break
        
        if not main_script and py_files:
            main_script = py_files[0]
            file_type = 'py'
        elif not main_script and js_files:
            for name in ['index.js', 'main.js', 'bot.js']:
                if name in js_files:
                    main_script = name
                    file_type = 'js'
                    break
            if not main_script and js_files:
                main_script = js_files[0]
                file_type = 'js'
        
        if not main_script:
            embed = discord.Embed(
                title="❌ ZIP ERROR",
                description="No .py or .js file found in ZIP.",
                color=discord.Color.red()
            )
            await message.reply(embed=embed)
            return
        
        save_user_file(user_id, main_script, file_type)
        main_script_path = os.path.join(user_folder, main_script)
        
        # Start the script (requirements already installed, so skip installation)
        if file_type == 'py':
            threading.Thread(target=run_script_simple, args=(main_script_path, user_id, user_folder, main_script, message, True)).start()
        else:
            threading.Thread(target=run_js_script_simple, args=(main_script_path, user_id, user_folder, main_script, message, True)).start()
        
        embed = discord.Embed(
            title="📦 ZIP EXTRACTED",
            description=f"✅ **{file_name}** extracted!\n📄 **Main:** `{main_script}`\n🔄 **Starting...**",
            color=discord.Color.blue()
        )
        
        if requirements_installed:
            embed.description += f"\n📦 **Requirements installed!**"
        
        msg = await message.reply(embed=embed)
        
        await asyncio.sleep(1)
        embed = discord.Embed(
            title="📦 ZIP EXTRACTED",
            description=f"✅ **{file_name}** extracted!\n📄 **Main:** `{main_script}`\n🟢 **Bot has started successfully!**",
            color=discord.Color.green()
        )
        
        if requirements_installed:
            embed.description += f"\n📦 **Requirements installed!**"
        
        await msg.edit(embed=embed)
        
    except Exception as e:
        logger.error(f"❌ ZIP error: {e}")
        embed = discord.Embed(
            title="❌ ZIP ERROR",
            description=f"Failed to process: {str(e)[:200]}",
            color=discord.Color.red()
        )
        await message.reply(embed=embed)
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# ================================
# CLEANUP
# ================================
def cleanup():
    logger.warning("🔴 Shutting down... Cleaning up")
    for script_key, script_info in list(bot_scripts.items()):
        try:
            kill_process_tree(script_info)
        except:
            pass
    logger.info("✅ Cleanup complete")

atexit.register(cleanup)

# ================================
# MAIN EXECUTION
# ================================
if __name__ == '__main__':
    logger.info("="*50)
    logger.info("🚀 TITAN HOSTING DISCORD BOT V3.2")
    logger.info(f"👑 Owner: {OWNER_ID}")
    logger.info(f"🛡️ Admins: {len(ADMIN_IDS)}")
    logger.info(f"👥 Users: {len(active_users)}")
    logger.info("="*50)
    
    keep_alive()
    
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        logger.info("👋 Bot shutting down...")
        cleanup()
    except Exception as e:
        logger.critical(f"💥 Fatal error: {e}", exc_info=True)