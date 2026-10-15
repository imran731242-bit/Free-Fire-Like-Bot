#!/usr/bin/env python3
"""
Simple Telegram bot with /start and /ping commands.
Clean, minimal, no obfuscation.
"""

import os
import sys
import time
import logging

import telebot

# ─── Logging ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)

# ─── Config ───────────────────────────────────────────────
BOT_TOKEN = "8643426514:AAHnMtialwe8t8fuvW5BTlGzm45huTQe9Bg"

if not BOT_TOKEN:
    log.error("BOT_TOKEN environment variable is not set.")
    log.error("Set it with:  export BOT_TOKEN='123:ABC...'")
    sys.exit(1)

# ─── Bot ──────────────────────────────────────────────────
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")


# ─── /start ───────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(message):
    user = message.from_user
    name = user.first_name or "there"
    text = (
        f"👋 *Hello, {name}!*\n\n"
        f"I'm a simple bot.\n\n"
        f"Available commands:\n"
        f"• /start — Show this message\n"
        f"• /ping  — Check bot latency\n"
    )
    bot.reply_to(message, text)
    log.info(f"/start from {user.id} ({user.username})")


# ─── /ping ────────────────────────────────────────────────
@bot.message_handler(commands=["ping"])
def cmd_ping(message):
    # Measure round-trip latency to Telegram's API
    t0 = time.perf_counter()
    sent = bot.reply_to(message, "🏓 Pinging...")
    t1 = time.perf_counter()

    api_ms = (t1 - t0) * 1000

    # Optional: measure a second round trip
    t2 = time.perf_counter()
    bot.get_me()
    t3 = time.perf_counter()
    api2_ms = (t3 - t2) * 1000

    avg = (api_ms + api2_ms) / 2

    if avg < 200:
        quality = "🟢 Excellent"
    elif avg < 500:
        quality = "🟡 Good"
    elif avg < 1000:
        quality = "🟠 Okay"
    else:
        quality = "🔴 Slow"

    text = (
        f"🏓 *Pong!*\n\n"
        f"📡 *Telegram API latency:*\n"
        f"• First round-trip:  `{api_ms:.0f} ms`\n"
        f"• Second round-trip: `{api2_ms:.0f} ms`\n"
        f"• Average:           `{avg:.0f} ms`\n\n"
        f"*Quality:* {quality}\n"
    )
    try:
        bot.edit_message_text(
            chat_id=sent.chat.id,
            message_id=sent.message_id,
            text=text,
        )
    except Exception as e:
        log.warning(f"edit_message_text failed: {e}")
        bot.reply_to(message, text)

    log.info(f"/ping from {message.from_user.id} → avg {avg:.0f} ms")


# ─── Fallback — ignore everything else ────────────────────
@bot.message_handler(func=lambda m: True)
def cmd_fallback(message):
    # Silently ignore unknown messages (no reply).
    pass


# ─── Entry point ──────────────────────────────────────────
def main():
    # Remove any old webhook so long polling works
    try:
        bot.remove_webhook()
    except Exception as e:
        log.warning(f"remove_webhook failed: {e}")

    me = bot.get_me()
    log.info(f"Bot started: @{me.username} (id={me.id})")
    log.info("Listening for updates... Press Ctrl+C to stop.")

    bot.infinity_polling(timeout=30, long_polling_timeout=25)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Stopped by user.")
    except Exception as e:
        log.exception(f"Fatal error: {e}")
        sys.exit(1)
