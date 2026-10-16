# It's ULTIMATE AGS x JOHIR

# =============================================================================
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                          ║
# ║         █████╗  ██████╗ ███████╗    ██╗  ██╗                            ║
# ║        ██╔══██╗██╔════╝ ██╔════╝    ╚██╗██╔╝                            ║
# ║        ███████║██║  ███╗███████╗     ╚███╔╝                             ║
# ║        ██╔══██║██║   ██║╚════██║     ██╔██╗                             ║
# ║        ██║  ██║╚██████╔╝███████║    ██╔╝ ██╗     ██╗ ██████╗ ██╗  ██╗   ║
# ║        ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝     ██║██╔═══██╗██║  ██║   ║
# ║                                                  ██║██║   ██║███████║   ║
# ║                                                  ██║██║   ██║██╔══██║   ║
# ║                                                  ██║╚██████╔╝██║  ██║   ║
# ║                                                  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ║
# ║                                                                          ║
# ║              AGS x JOHIR ULTIMATE GENERATOR v13.0                        ║
# ║              THE MOST ADVANCED ACCOUNT GENERATOR                         ║
# ║                    WITH ULTIMATE ADMIN CONTROL                           ║
# ║                                                                          ║
# ║                     CREDIT: AGS x JOHIR                                  ║
# ║              IG: https://www.instagram.com/ags_x_johir                   ║
# ║                  TELEGRAM: @ags_x_johir | @restricted_zu                     ║
# ║                                                                          ║
# ║         WATERMARKS: ULTIMATE_PROTECTION_v13 SA_GEN_2025                  ║
# ║            PROTECTED_BY_AGS_JOHIR ADMIN_CONTROL_SYSTEM                   ║
# ║                    OWNER_VERIFICATION OWNER MODE                         ║
# ║            OB55 FIELD-22 FIX + AGS ACTIVATOR API INTEGRATED              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

import os
import sys
import subprocess
import platform

try:
    import jwt as pyjwt
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyJWT", "--quiet"])
    import jwt as pyjwt

import hmac
import hashlib
import asyncio
import string
import random
import json
import codecs
import time
from datetime import datetime
import base64
import signal
import threading
import re
import struct
import gzip
import urllib.request
import urllib.error
import urllib.parse
import ssl
import concurrent.futures
from collections import deque
from typing import Optional, Dict, Any, List, Tuple

# =============================================================================
# 🔐 BUILT-IN KEYAUTH API ENGINE
# =============================================================================

class KeyAuthResponse:
    def __init__(self):
        self.success = False
        self.message = ""

class KeyAuthUser:
    def __init__(self):
        self.username = ""
        self.subscriptions = []
        self.expiry = 0

class KeyAuthApp:
    def __init__(self, name, ownerid, secret, version):
        self.name = name
        self.ownerid = ownerid
        self.secret = secret
        self.version = version
        self.sessionid = ""
        self.response = KeyAuthResponse()
        self.user_data = KeyAuthUser()

    def _get_hwid(self):
        try:
            unique_str = (
                f"{os.environ.get('USER', 'termux')}-"
                f"{platform.machine()}-"
                f"{platform.processor()}-"
                f"{os.environ.get('HOME', '')}-"
                f"{platform.node()}"
            )
            return hashlib.sha256(unique_str.encode()).hexdigest()[:24]
        except Exception:
            return "TERMUX-FIXED-DEVICE-LOCK-01"

    def _req(self, data):
        url = "https://keyauth.win/api/1.2/"
        enc_data = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(
            url, data=enc_data, method="POST",
            headers={"User-Agent": "KeyAuth", "Content-Type": "application/x-www-form-urlencoded"}
        )
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            return {"success": False, "message": str(e), "network_error": True}

    def init(self):
        data = {"type": "init", "name": self.name, "ownerid": self.ownerid, "ver": self.version}
        res = self._req(data)
        if res.get("success"):
            self.sessionid = res.get("sessionid", "")
            self.response.success = True
            return True
        else:
            self.response.success = False
            self.response.message = res.get("message", "Init failed")
            return False

    def _parse_expiry(self, info):
        exp_time = 0
        try:
            subs = info.get("subscriptions", [])
            raw_exp = None
            if isinstance(subs, list) and len(subs) > 0:
                raw_exp = subs[0].get("expiry")
            if not raw_exp and "expiry" in info:
                raw_exp = info.get("expiry")
            if raw_exp:
                if str(raw_exp).isdigit():
                    exp_time = int(raw_exp)
                else:
                    raw_str = str(raw_exp).strip()
                    try:
                        exp_time = int(datetime.strptime(raw_str.split(".")[0], "%Y-%m-%d %H:%M:%S").timestamp())
                    except Exception:
                        try:
                            exp_time = int(datetime.strptime(raw_str, "%m/%d/%Y, %I:%M %p").timestamp())
                        except Exception:
                            try:
                                exp_time = int(datetime.fromisoformat(raw_str).timestamp())
                            except Exception:
                                exp_time = 0
        except Exception:
            exp_time = 0
        return exp_time

    def license(self, key):
        hwid = self._get_hwid()
        data = {"type": "license", "key": key, "hwid": hwid, "sessionid": self.sessionid,
                "name": self.name, "ownerid": self.ownerid}
        res = self._req(data)
        if res.get("success"):
            self.response.success = True
            info = res.get("info", {})
            self.user_data.username = info.get("username", key)
            self.user_data.subscriptions = info.get("subscriptions", [])
            self.user_data.expiry = self._parse_expiry(info)
            return True
        else:
            self.response.success = False
            self.response.message = res.get("message", "Invalid License Key")
            return False

    def login(self, username, password):
        hwid = self._get_hwid()
        data = {"type": "login", "username": username, "pass": password, "hwid": hwid,
                "sessionid": self.sessionid, "name": self.name, "ownerid": self.ownerid}
        res = self._req(data)
        if res.get("success"):
            self.response.success = True
            info = res.get("info", {})
            self.user_data.username = info.get("username", username)
            self.user_data.subscriptions = info.get("subscriptions", [])
            self.user_data.expiry = self._parse_expiry(info)
            return True
        else:
            self.response.success = False
            self.response.message = res.get("message", "Invalid Username or Password")
            return False

def hard_kill_terminal(reason="TIME LIMIT OVER"):
    global shutdown_requested
    shutdown_requested.set()
    print(f"\n\n\033[38;5;196m\033[1m[!] KEYAUTH TERMINATION: {reason}! TERMINAL CLOSING NOW...\033[0m\n")
    sys.stdout.flush()
    time.sleep(0.5)
    try:
        os.kill(os.getpid(), signal.SIGKILL)
    except Exception:
        os._exit(1)

def start_key_expiry_monitor(app: KeyAuthApp):
    def _monitor():
        consecutive_server_fails = 0
        while True:
            time.sleep(2)
            try:
                if app.user_data.expiry and app.user_data.expiry > 0:
                    current_ts = int(time.time())
                    if current_ts >= app.user_data.expiry:
                        hard_kill_terminal("LICENSE / USER TIME LIMIT OVER")
                if int(time.time()) % 35 < 3:
                    chk = app._req({"type": "check", "sessionid": app.sessionid,
                                    "name": app.name, "ownerid": app.ownerid})
                    if chk.get("network_error"): continue
                    if not chk.get("success"):
                        msg = chk.get("message", "").lower()
                        if "expired" in msg or "invalid" in msg or "banned" in msg or "not found" in msg:
                            consecutive_server_fails += 1
                            if consecutive_server_fails >= 2:
                                hard_kill_terminal(chk.get('message', 'ACCOUNT EXPIRED').upper())
                    else:
                        consecutive_server_fails = 0
            except Exception:
                pass
    t = threading.Thread(target=_monitor, daemon=True)
    t.start()

# =============================================================================
# 🛡️ ULTIMATE ANTI-CREDIT & FILENAME PROTECTION SYSTEM
# =============================================================================

class SecurityShield:
    REQUIRED_FILENAME = "ags×johir.py"

    CREDIT_SIGNATURES = [
        "@restricted_zu", "AGS x JOHIR", "@ags_owner_atif", "@restricted_zu | @ags_owner_atif",
        "IG: https://www.instagram.com/restricted_johir", "atif",
        "ULTIMATE ADMIN CONTROL", "OWNER MODE"
    ]

    WATERMARKS = [
        "ULTIMATE_PROTECTION_v13", "SA_GEN_2025", "PROTECTED_BY_AGS×JOHIR",
        "ADMIN_CONTROL_SYSTEM", "OWNER_VERIFICATION"
    ]

    @classmethod
    def verify_filename(cls):
        current = os.path.basename(__file__)
        return current == cls.REQUIRED_FILENAME

    @classmethod
    def verify_credits(cls):
        try:
            with open(__file__, 'r', encoding='utf-8') as f:
                content = f.read()
            for sig in cls.CREDIT_SIGNATURES:
                if sig not in content:
                    return False, f"MISSING: {sig}"
            for mark in cls.WATERMARKS:
                if mark not in content:
                    return False, "WATERMARK MISSING"
            return True, "✓ INTEGRITY VERIFIED"
        except:
            return False, "VERIFICATION FAILED"

    @classmethod
    def show_breach(cls, reason):
        W = VisualMaster.get_term_width()
        BW = min(62, W - 2)
        INNER = BW - 2
        print(f"\n{C2['blood_red']}{C2['bold']}")
        print(VisualMaster.center_line(f"┏{'━' * INNER}┓"))
        print(VisualMaster.center_line(f"┃{_pad('🚨 SECURITY BREACH DETECTED 🚨', INNER, 'center')}┃"))
        print(VisualMaster.center_line(f"┣{'━' * INNER}┫"))
        print(VisualMaster.center_line(f"┃{_pad(reason, INNER, 'center')}┃"))
        print(VisualMaster.center_line(f"┣{'━' * INNER}┫"))
        print(VisualMaster.center_line(f"┃{_pad('THIS TOOL IS PROTECTED BY AGS x JOHIR', INNER, 'center')}┃"))
        print(VisualMaster.center_line(f"┃{_pad('TAMPERING OR RENAMING PROHIBITED', INNER, 'center')}┃"))
        print(VisualMaster.center_line(f"┗{'━' * INNER}┛"))
        print(f"{C2['reset']}")
        time.sleep(3)
        sys.exit(1)

# =============================================================================
# 🎨 CRIMSON CYBERPUNK CENTER HUD ENGINE
# =============================================================================

class VisualMaster:
    @classmethod
    def clear(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def get_term_width(cls):
        try:
            w = os.get_terminal_size().columns
            return max(50, w)
        except Exception:
            return 80

    @classmethod
    def get_box_width(cls):
        w = cls.get_term_width()
        return min(62, w - 2)

    @classmethod
    def center_line(cls, line_str, width=None):
        w = width or cls.get_term_width()
        vis_len = _strip_len(line_str)
        if vis_len >= w:
            return line_str
        pad_left = (w - vis_len) // 2
        return (" " * pad_left) + line_str

    COLORS = {
        'blood_red':    '\033[38;5;196m',
        'crimson_glow': '\033[38;5;203m',
        'deep_red':     '\033[38;5;160m',
        'gold':         '\033[38;5;220m',
        'cyber_cyan':   '\033[38;5;51m',
        'matrix_green': '\033[38;5;82m',
        'plasma_pink':  '\033[38;5;207m',
        'orange_fire':  '\033[38;5;208m',
        'pure_white':   '\033[38;5;255m',
        'dim':          '\033[38;5;242m',
        'reset':        '\033[0m',
        'bold':         '\033[1m',
        'italic':       '\033[3m',
    }

VISUAL = VisualMaster()
C2 = VISUAL.COLORS

def _strip_len(s):
    return len(re.sub(r'\033\[[0-9;]*m', '', s))

def _pad(s, width, align='left'):
    vl = _strip_len(s)
    if vl >= width: return s
    pad = width - vl
    if align == 'left':   return s + ' ' * pad
    if align == 'right':  return ' ' * pad + s
    return ' ' * (pad // 2) + s + ' ' * (pad - pad // 2)

def mask_password(pwd: str) -> str:
    if len(pwd) <= 12:
        return pwd[:3] + "•••" + pwd[-3:]
    return pwd[:6] + "••••••••" + pwd[-4:]

def animate_header(user_level="USER"):
    W = VisualMaster.get_term_width()
    banner_lines = [
        "██████╗ ██████╗ ███████╗ █████╗ ████████╗    ██╗ ██████╗ ██╗  ██╗██╗██████╗ ",
        "██╔════╝ ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝    ██║██╔═══██╗██║  ██║██║██╔══██╗",
        "██║  ███╗██████╔╝█████╗  ███████║   ██║       ██║██║   ██║███████║██║██████╔╝",
        "██║   ██║██╔══██╗██╔══╝  ██╔══██║   ██║  ██   ██║██║   ██║██╔══██║██║██╔══██╗",
        "╚██████╔╝██║  ██║███████╗██║  ██║   ██║  ╚█████╔╝╚██████╔╝██║  ██║██║██║  ██║",
        " ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
    ]
    gradient = [C2['blood_red'], C2['crimson_glow'], C2['orange_fire'],
                C2['gold'], C2['cyber_cyan'], C2['blood_red']]
    print()
    for i, line in enumerate(banner_lines):
        col = gradient[i % len(gradient)]
        print(f"{col}{C2['bold']}{VisualMaster.center_line(line)}{C2['reset']}")
    sub_border = "═" * min(42, W - 4)
    print(f"{C2['deep_red']}{VisualMaster.center_line(sub_border)}{C2['reset']}")
    if user_level == "OWNER":
        lv = f"{C2['blood_red']}{C2['bold']}👑 AGS x JOHIR :: OWNER CORE VERIFIED{C2['reset']}"
    elif user_level == "ADMIN":
        lv = f"{C2['crimson_glow']}{C2['bold']}⚡ AGS x JOHIR :: ROOT ADMIN ACCESS{C2['reset']}"
    else:
        lv = f"{C2['blood_red']}{C2['bold']}👤 AGS x JOHIR :: CLIENT ACTIVE{C2['reset']}"
    print(VisualMaster.center_line(lv))
    bar_w = 28
    for i in range(bar_w + 1):
        filled = "█" * i
        empty = " " * (bar_w - i)
        pct = int((i / bar_w) * 100)
        progress_str = f"{C2['blood_red']}❰{C2['crimson_glow']}{filled}{C2['dim']}{empty}{C2['blood_red']}❱ {C2['gold']}{pct:3d}%{C2['reset']}"
        sys.stdout.write(f"\r{VisualMaster.center_line(progress_str)}")
        sys.stdout.flush()
        time.sleep(0.007)
    print("\n")

# =============================================================================
# 🔑 KEYAUTH DETAILS & AUTHENTICATION PORTAL (KEYAUTH SERVER)
# =============================================================================

KEYAUTH_NAME     = "Great Zahir's Application"
KEYAUTH_OWNER_ID = "J6pVxs3xsc"
KEYAUTH_SECRET   = "7c5b3987c787e511ca55ad56cef091e8202c07e64f24049317be7694a3025b18"
KEYAUTH_VERSION  = "1.0"

keyauthapp = KeyAuthApp(
    name=KEYAUTH_NAME,
    ownerid=KEYAUTH_OWNER_ID,
    secret=KEYAUTH_SECRET,
    version=KEYAUTH_VERSION
)

def render_login_menu():
    VisualMaster.clear()
    W = VisualMaster.get_term_width()
    BW = VisualMaster.get_box_width()
    INNER = BW - 2
    owner_tag = C2['gold'] + "DEVELOPER: AGS x JOHIR | @restricted_zu | @ags_owner_atif" + C2['blood_red']
    print(f"{C2['blood_red']}{C2['bold']}")
    print(VisualMaster.center_line(f"┏{'━' * INNER}┓"))
    print(VisualMaster.center_line(f"┃{_pad('⚡ AGS x JOHIR SECURE VERIFICATION ⚡', INNER, 'center')}┃"))
    print(VisualMaster.center_line(f"┣{'━' * INNER}┫"))
    print(VisualMaster.center_line(f"┃{_pad(owner_tag, INNER, 'center')}┃"))
    print(VisualMaster.center_line(f"┣{'━' * INNER}┫"))
    print(VisualMaster.center_line(f"┃  {C2['cyber_cyan']}[1]{C2['reset']} License Key Login (AGS_JOHIR){_pad('', max(0, INNER - 45))} ┃"))
    print(VisualMaster.center_line(f"┃  {C2['cyber_cyan']}[2]{C2['reset']} Username & Password Login (AGS_JOHIR){_pad('', max(0, INNER - 45))} ┃"))
    print(VisualMaster.center_line(f"┗{'━' * INNER}┛"))
    print(f"{C2['reset']}")

def dual_login_system():
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            content = f.read()
            if "ags×johir" not in content or "AGS x JOHIR" not in content:
                print("\033[91m\033[1m" + "=" * 60)
                print("   🚫 CRITICAL ERROR: SCRIPT TAMPERED! 🚫")
                print("=" * 60 + "\033[0m")
                sys.exit(1)
    except Exception:
        pass

    render_login_menu()
    W = VisualMaster.get_term_width()
    BW = VisualMaster.get_box_width()
    indent = " " * ((W - BW) // 2 + 2)
    choice = input(f"{indent}{C2['orange_fire']}➤ {C2['pure_white']}Select Login Method (1-2) [Enter=1]: {C2['crimson_glow']}").strip() or "1"
    print(f"{C2['reset']}", end="")

    print(VisualMaster.center_line(f"{C2['cyber_cyan']}Connecting to AGS_JOHIR...{C2['reset']}"))
    if not keyauthapp.init():
        print(VisualMaster.center_line(f"{C2['blood_red']}KeyAuth Connection Error: {keyauthapp.response.message}{C2['reset']}"))
        time.sleep(2.5)
        sys.exit(1)

    if choice == "1":
        attempts = 3
        while attempts > 0:
            try:
                render_login_menu()
                raw_key = input(f"{indent}{C2['orange_fire']}🔑 {C2['pure_white']}License Key: {C2['crimson_glow']}").strip()
                print(f"{C2['reset']}", end="")
                if not raw_key:
                    continue
                final_key = raw_key if raw_key.upper().startswith("KEYAUTH-") else "KEYAUTH-" + raw_key
                print(VisualMaster.center_line(f"{C2['dim']}Authenticating key via AGS_JOHIR...{C2['reset']}"))
                if keyauthapp.license(final_key):
                    user_level = "USER"
                    try:
                        subs = [s.get("subscription", "").lower() for s in keyauthapp.user_data.subscriptions]
                        if "owner" in subs: user_level = "OWNER"
                        elif "admin" in subs: user_level = "ADMIN"
                    except Exception:
                        pass
                    start_key_expiry_monitor(keyauthapp)
                    animate_header(user_level)
                    return user_level
                else:
                    attempts -= 1
                    msg = keyauthapp.response.message or 'Invalid Key'
                    if attempts > 0:
                        print(VisualMaster.center_line(f"{C2['blood_red']}✘ {msg}! Retries remaining: {attempts}{C2['reset']}"))
                        time.sleep(1.8)
                    else:
                        print(VisualMaster.center_line(f"\n{C2['blood_red']}{C2['bold']}⛔ LOCKDOWN ACTIVE — TERMINATED{C2['reset']}\n"))
                        time.sleep(2)
                        sys.exit(1)
            except KeyboardInterrupt:
                print(VisualMaster.center_line(f"\n{C2['orange_fire']}Session Canceled.{C2['reset']}"))
                sys.exit(0)
    else:
        attempts = 3
        while attempts > 0:
            try:
                render_login_menu()
                u_in = input(f"{indent}{C2['orange_fire']}👤 {C2['pure_white']}Given Username: {C2['cyber_cyan']}").strip()
                p_in = input(f"{indent}{C2['orange_fire']}🔒 {C2['pure_white']}Given Password: {C2['crimson_glow']}").strip()
                print(f"{C2['reset']}", end="")
                if not u_in or not p_in:
                    continue
                print(VisualMaster.center_line(f"{C2['dim']}Authenticating user via AGS_JOHIR...{C2['reset']}"))
                if keyauthapp.login(u_in, p_in):
                    user_level = "USER"
                    try:
                        subs = [s.get("subscription", "").lower() for s in keyauthapp.user_data.subscriptions]
                        if "owner" in subs: user_level = "OWNER"
                        elif "admin" in subs: user_level = "ADMIN"
                    except Exception:
                        pass
                    start_key_expiry_monitor(keyauthapp)
                    animate_header(user_level)
                    return user_level
                else:
                    attempts -= 1
                    msg = keyauthapp.response.message or 'Invalid Credentials'
                    if attempts > 0:
                        print(VisualMaster.center_line(f"{C2['blood_red']}✘ {msg}! Retries remaining: {attempts}{C2['reset']}"))
                        time.sleep(1.8)
                    else:
                        print(VisualMaster.center_line(f"\n{C2['blood_red']}{C2['bold']}⛔ ACCESS DENIED — TERMINATED{C2['reset']}\n"))
                        time.sleep(2)
                        sys.exit(1)
            except KeyboardInterrupt:
                print(VisualMaster.center_line(f"\n{C2['orange_fire']}Session Canceled.{C2['reset']}"))
                sys.exit(0)

if not SecurityShield.verify_filename():
    SecurityShield.show_breach(f"INVALID FILENAME! REQUIRED: {SecurityShield.REQUIRED_FILENAME}")

credit_status, credit_msg = SecurityShield.verify_credits()
if not credit_status:
    SecurityShield.show_breach(credit_msg)

USER_LEVEL = dual_login_system()

# ─── SSL context ────────────────────────────────────────────────────────────
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

# =============================================================================
# TURBO & RATE LIMIT CONFIGURATION
# =============================================================================
HTTP_TIMEOUT_FAST    = 6
HTTP_TIMEOUT_NORMAL  = 8
MAX_WORKERS_HARD     = 50
REQUEST_DELAY        = 0.50
RETRY_TOKEN          = 3
RETRY_LOGIN          = 3
RETRY_LOGIN_DATA     = 4
RETRY_CREATE_ACCOUNT = 3
DD_REFRESH_INTERVAL  = 5

BASE_DIR  = "AGS_JOHIR"
RARE_DIR  = os.path.join(BASE_DIR, "Rare")
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(RARE_DIR, exist_ok=True)
PROXY_FILE = "proxies.txt"

# =============================================================================
# AES CIPHER
# =============================================================================
_SBOX = (
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
)
_INV_SBOX = [0] * 256
for _i, _v in enumerate(_SBOX):
    _INV_SBOX[_v] = _i
_RCON = (0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36)

def _xtime(a):
    return ((a << 1) ^ 0x1b) & 0xFF if a & 0x80 else (a << 1) & 0xFF

def _mix_single(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    return [
        a[0] ^ _xtime(a[0] ^ a[1]) ^ t,
        a[1] ^ _xtime(a[1] ^ a[2]) ^ t,
        a[2] ^ _xtime(a[2] ^ a[3]) ^ t,
        a[3] ^ _xtime(a[3] ^ u) ^ t,
    ]

def _aes_key_expansion(key):
    Nk, Nr = 4, 10
    w = [0] * (4 * (Nr + 1))
    for i in range(Nk):
        w[i] = (key[4*i] << 24) | (key[4*i+1] << 16) | (key[4*i+2] << 8) | key[4*i+3]
    for i in range(Nk, 4 * (Nr + 1)):
        t = w[i-1]
        if i % Nk == 0:
            t = ((_SBOX[(t >> 16) & 0xFF] << 24) | (_SBOX[(t >> 8) & 0xFF] << 16) |
                 (_SBOX[t & 0xFF] << 8) | _SBOX[(t >> 24) & 0xFF])
            t ^= _RCON[i // Nk - 1] << 24
        w[i] = w[i - Nk] ^ t
    rk = []
    for r in range(Nr + 1):
        k = bytearray(16)
        for j in range(4):
            v = w[r*4 + j]
            k[j*4]   = (v >> 24) & 0xFF
            k[j*4+1] = (v >> 16) & 0xFF
            k[j*4+2] = (v >> 8)  & 0xFF
            k[j*4+3] = v & 0xFF
        rk.append(bytes(k))
    return rk

def _aes_encrypt_block(block, round_keys):
    Nr = 10
    s = bytearray(b ^ k for b, k in zip(block, round_keys[0]))
    for rnd in range(1, Nr):
        s = bytearray(_SBOX[b] for b in s)
        s[1], s[5], s[9], s[13]   = s[5], s[9], s[13], s[1]
        s[2], s[6], s[10], s[14]  = s[10], s[14], s[2], s[6]
        s[3], s[7], s[11], s[15]  = s[15], s[3], s[7], s[11]
        for c in range(4):
            col = [s[c*4+r] for r in range(4)]
            mixed = _mix_single(col)
            for r in range(4):
                s[c*4+r] = mixed[r]
        s = bytearray(b ^ k for b, k in zip(s, round_keys[rnd]))
    s = bytearray(_SBOX[b] for b in s)
    s[1], s[5], s[9], s[13]   = s[5], s[9], s[13], s[1]
    s[2], s[6], s[10], s[14]  = s[10], s[14], s[2], s[6]
    s[3], s[7], s[11], s[15]  = s[15], s[3], s[7], s[11]
    s = bytearray(b ^ k for b, k in zip(s, round_keys[Nr]))
    return bytes(s)

def _aes_decrypt_block(block, round_keys):
    Nr = 10
    s = bytearray(b ^ k for b, k in zip(block, round_keys[Nr]))
    for rnd in range(Nr - 1, 0, -1):
        s[3], s[7], s[11], s[15]  = s[15], s[3], s[7], s[11]
        s[2], s[6], s[10], s[14]  = s[10], s[14], s[2], s[6]
        s[1], s[5], s[9], s[13]   = s[5], s[9], s[13], s[1]
        s = bytearray(_INV_SBOX[b] for b in s)
        s = bytearray(b ^ k for b, k in zip(s, round_keys[rnd]))
        for c in range(4):
            col = [s[c*4+r] for r in range(4)]
            u = _xtime(_xtime(col[0] ^ col[2]))
            v = _xtime(_xtime(col[1] ^ col[3]))
            col[0] ^= u; col[1] ^= v; col[2] ^= u; col[3] ^= v
            mixed = _mix_single(col)
            for r in range(4):
                s[c*4+r] = mixed[r]
    s[3], s[7], s[11], s[15]  = s[15], s[3], s[7], s[11]
    s[2], s[6], s[10], s[14]  = s[10], s[14], s[2], s[6]
    s[1], s[5], s[9], s[13]   = s[5], s[9], s[13], s[1]
    s = bytearray(_INV_SBOX[b] for b in s)
    s = bytearray(b ^ k for b, k in zip(s, round_keys[0]))
    return bytes(s)

def _pkcs7_pad(data, block_size=16):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def _aes_cbc_encrypt(data, key, iv):
    data = _pkcs7_pad(data)
    rk = _aes_key_expansion(key)
    out = bytearray()
    prev = iv
    for i in range(0, len(data), 16):
        block = bytes(d ^ p for d, p in zip(data[i:i+16], prev))
        out.extend(_aes_encrypt_block(block, rk))
        prev = out[-16:]
    return bytes(out)

def _aes_cbc_decrypt(data, key, iv):
    rk = _aes_key_expansion(key)
    out = bytearray()
    prev = iv
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        out.extend(_aes_decrypt_block(block, rk))
        prev = block
    if out and 1 <= out[-1] <= 16:
        out = out[:-out[-1]]
    return bytes(out)

AES_KEY = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
AES_IV  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])

def aes_encrypt(data: bytes) -> bytes:
    return _aes_cbc_encrypt(data, AES_KEY, AES_IV)

def aes_decrypt(data: bytes) -> bytes:
    return _aes_cbc_decrypt(data, AES_KEY, AES_IV)

def aes_encrypt_hex(hex_str: str) -> bytes:
    return aes_encrypt(bytes.fromhex(hex_str))

# =============================================================================
# NETWORK CONFIG & CONSTANTS
# =============================================================================
class RateLimitException(Exception): pass

io_lock   = threading.Lock()
print_lock= threading.Lock()
dd_lock   = threading.Lock()
shutdown_requested = threading.Event()

hex_key = ("326565343438313965396234353938383435313431303637623238313632313837"
           "34643064356437616639643866376530306331653534373135623764316533")
HMAC_KEY = bytes.fromhex(hex_key)

DATADOME_COOKIE = ("datadome=0TgYVopr1q2I7rZ~GdyOVhuiXeqIUgHZP_d4AJMgJReKDbPgb~"
                   "sqqu8DJ21FLoV6dGaH5DzXfEwE9nlqa_q4SmJEVwVNPx0sp~yeNRlTyJYTbYow87bBfqxn3e~Qf1mF")
USER_AGENT = "GarenaMSDK/4.0.41(SM-S908E ;Android 9;en;US;app 1.123.1 2019120270;)"

REGION_LANG = {
    "BD": "bn", "IND": "hi", "PK": "ur", "SG": "en",
    "ID": "id", "ME": "ar"
}
REGION_LOGIN = {
    "BD":  "https://loginbp.ppmainecoonghj.com/",
    "IND": "https://loginbp.ggblueshark.com/",
    "PK":  "https://loginbp.ggpolarbear.com/",
    "SG":  "https://loginbp.ggblueshark.com/",
    "ID":  "https://loginbp.ggpolarbear.com/",
    "ME":  "https://loginbp.ggpolarbear.com/",
}
REGION_CLIENT = {
    "BD":  "https://clientbp.ppmainecoonghj.com/",
    "IND": "https://clientbp.ggblueshark.com/",
    "PK":  "https://clientbp.ggpolarbear.com/",
    "SG":  "https://clientbp.ggblueshark.com/",
    "ID":  "https://clientbp.ggpolarbear.com/",
    "ME":  "https://clientbp.ggpolarbear.com/",
}

OB = "OB55"
VERSION = "1.132.6"

# 🔥 FIELD 22 — OB55 CLIENT SIGNATURE (from FixGen.txt)
FIELD22_HEX = (
    "474752450101010067020000a6a42db7bc5516876af3d1ba4adc337bac558af092eb3757d59d65c9323bba42"
    "c6593a48b74f33b2b5b3dc45cbd7ac02040db58f394045be4835213e12c35e5566445a5224f39d205fcf9"
    "1c0e6bec797e7b3968ac00e90d7500b5865828a9d6f2091c3070f5319a130748e407ed57e6638974670ac"
    "045631b3d08c310cf1256cebcf1aed2d97d177534603d1c95d9c5d698340e797e72aa7ecc67a33122e48"
    "b0dfda050a1649586aca5e979be1fd9d99f48cd8cf59630e0ff60f67d4ed2ec4e5e7475970449a6c0632"
    "9009ee0ce2567892587675781a31e4bb2774403b2f78e9811df2cb397fa602572266747704c625807791"
    "0902eb7420bcb4ab743d1610cddba9019e7867aaad3aa7ba9b04968064a409b66733f9f78c566a25ff4"
    "78cba37a2ffe23203d4b05bceef826f174b0be7912d19432cc759325251fa094d70693fb672d6f9e7992"
    "84081b3adb541dd8f27ef80dcf1e7f0ff30f2fd976659457ce41e175a2d6301b777981ccc16b9a8247a"
    "baab8de0867836c27de0146fe4d0e1fd39b86ba51f0b58601cfcbd7f6f3451fe4184b26ed44ac2f6f7bb"
    "4ce5d9a80f88c2cbfe7553e5ab97c8b028ae16b4f70f037753b8c229a6e5e9038fcbb9b4c2abb954894f"
    "8f2faf177bfdaab3b0ed537156633621d16b62d58ba4ebe518997c33e2304976ba6af9df7e7e34302c79"
    "10ae559c7e3d20a30d71c14f85c0e86f26291bbf18c2d9dfe9a908592eea4523e6c1e5d9bb5abfbebfccd"
    "5c4e136f9be777723e932b06c029df5125191000c90fde62a8e5f8fceb28648f0c69ec3037d09302b2a"
    "de908a20dbd42761ca449b2743fc362649e16235769d9fbd7f87cd64972b58d69c0441abb5d22ddc6ed05"
    "9f7ac1bdbfaef8c60e64631809c5e08c7cb4074c8ce6170d94b411604986be4ae163a"
)
FIELD22 = bytes.fromhex(FIELD22_HEX)

# 🔥 AGS ACTIVATOR API
ACTIVATOR_API_URL = "USE YOUR OWN API OR OUR ACTIVATOR FULL SRC"

WORKING_BIO_PACKET_HEX = (
    "cc79fefaa825864f1a7c01dc79efa59e4e04d5d0cb6c0d389f2d5409201a0deb"
    "a50aa8211639af718b8824d030e582fdfa28f60acba99ff0ec3841f67634a13f0"
    "ad07ce3966a6438dc0dd574d960834f28ff57951d7d13768a195428ba5c7db4e"
    "ab7b38f8c9ac8b4e2a04feb5571b422f47aa3b14e2b0c41f20260414c8fa8b3ca"
    "183e0d61dadc235a4599ac079451a877fd7fb920007e9bcb32404753c53d9b13f"
    "286b59a9ffd595bea8c903b484ce899b3cb7234c40879c209aaf047cb9a5f9628"
    "4b4b59d8ef179bf865110d11e43301c262e1aa0c525658919678194d01f860d4"
    "41308013801b558bcbfd5809f157"
)

CUSTOM_LONG_BIO_HEX = (
    "5b425d5b435d5b4646464646465d4652454520465b4646413530305d495b4646464646465d"
    "5245205b3030464643435d44455620544f4f4c532c2043594245522026205350412a4d494e"
    "4720455850415254455b4646303030305d20262050524f4752414d4d4552205b3030464630"
    "305d202620434f4e54524f4c4c45520a5b4646443730305d2049473a205b4646303046465d"
    "406167735f785f6a6f686972205b3030434346465d4d5920544720555345524e414d453a20"
    "5b4438314236305d406167735f6a6f686972"
)

# =============================================================================
# PROXY MANAGER & AUTO SCRAPER ENGINE
# =============================================================================
class ProxyManager:
    def __init__(self, path=PROXY_FILE):
        self.path = path
        self.proxies: List[str] = []
        self.index = 0
        self._lock = threading.Lock()

    def fetch_online_proxies(self, count=100) -> int:
        sources = [
            "https://raw.githubusercontent.com/databay-labs/free-proxy-list/master/http.txt",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        scraped = []
        for url in sources:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=8, context=_ssl_ctx) as r:
                    content = r.read().decode("utf-8", errors="ignore")
                    lines = [l.strip() for l in content.splitlines() if ":" in l and not l.startswith("#")]
                    scraped.extend(lines)
                    if len(scraped) >= count: break
            except Exception:
                continue
        valid = list(dict.fromkeys(scraped))[:count]
        if valid:
            with open(self.path, "w", encoding="utf-8") as f:
                for p in valid: f.write(p + "\n")
            self.load()
            return len(self.proxies)
        return 0

    def load(self):
        self.proxies.clear()
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    p = line.strip()
                    if p and not p.startswith("#"):
                        self.proxies.append(p)
        except FileNotFoundError: pass

    def get(self) -> Optional[str]:
        if not self.proxies: return None
        with self._lock:
            p = self.proxies[self.index % len(self.proxies)]
            self.index += 1
            return p

    def count(self) -> int: return len(self.proxies)

PROXY_MGR = ProxyManager()

def _build_opener(proxy: Optional[str]):
    handlers = [urllib.request.HTTPSHandler(context=_ssl_ctx)]
    if proxy:
        if not proxy.startswith("http"): proxy = "http://" + proxy
        handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    else:
        handlers.append(urllib.request.ProxyHandler({}))
    return urllib.request.build_opener(*handlers)

# =============================================================================
# UTILITY
# =============================================================================
def _enc_varint(n):
    buf = bytearray()
    while True:
        b = n & 0x7F; n >>= 7
        if n: b |= 0x80
        buf.append(b)
        if not n: break
    return bytes(buf)

def _dec_varint(data, pos):
    result = 0; shift = 0
    while pos < len(data):
        b = data[pos]; pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80): break
        shift += 7
    return result, pos

def _make_varint_field(n, v): return _enc_varint((n<<3)|0) + _enc_varint(v)
def _make_bytes_field(n, v):
    if isinstance(v, str): v = v.encode('utf-8')
    return _enc_varint((n<<3)|2) + _enc_varint(len(v)) + v
def _make_int32_field(n, v):
    if v < 0: v += 1<<64
    return _enc_varint((n<<3)|0) + _enc_varint(v)
def _make_int64_field(n, v):
    if v < 0: v += 1<<64
    return _enc_varint((n<<3)|0) + _enc_varint(v)

def _decode_proto(data):
    result = {}; pos = 0; length = len(data)
    while pos < length:
        try: tag, pos = _dec_varint(data, pos)
        except Exception: break
        fn, wt = tag>>3, tag&7
        if wt == 0:
            val, pos = _dec_varint(data, pos)
            result[str(fn)] = {"wire_type":"varint","data":val}
        elif wt == 2:
            vlen, pos = _dec_varint(data, pos)
            chunk = data[pos:pos+vlen]; pos += vlen
            try: s = chunk.decode('utf-8'); result[str(fn)] = {"wire_type":"string","data":s}
            except Exception: result[str(fn)] = {"wire_type":"bytes","data":chunk.hex()}
        elif wt == 1:
            val = struct.unpack_from('<Q', data, pos)[0]; pos += 8
            result[str(fn)] = {"wire_type":"64bit","data":val}
        elif wt == 5:
            val = struct.unpack_from('<I', data, pos)[0]; pos += 4
            result[str(fn)] = {"wire_type":"32bit","data":val}
        else: break
    return result

def _safe_int(value, default=0):
    if value is None or value == "": return default
    if isinstance(value, bool): return int(value)
    if isinstance(value, int): return value
    if isinstance(value, (bytes, bytearray)):
        try: return int.from_bytes(value, "big")
        except Exception: return default
    if isinstance(value, str):
        try: return int(value)
        except Exception: return default
    return default

def _get_field(parsed, *field_nums, default=None):
    if not isinstance(parsed, dict): return default
    for fn in field_nums:
        key = str(fn) if not isinstance(fn, str) else fn
        if key in parsed:
            val = parsed[key].get("data") if isinstance(parsed[key], dict) else None
            if val is not None and val != "": return val
    return default

def _build_major_register_proto(name, access_token, open_id, field14, lang="en"):
    """🔥 OB55 FIXED — includes field 20, 21, 22 (client signature)"""
    buf = bytearray()
    buf += _make_bytes_field(1, name)
    buf += _make_bytes_field(2, access_token)
    buf += _make_bytes_field(3, open_id)
    buf += _make_int64_field(5, 102000007)
    buf += _make_int32_field(6, 4)
    buf += _make_int32_field(7, 1)
    buf += _make_int32_field(13, 1)
    buf += _make_bytes_field(14, field14)
    buf += _make_bytes_field(15, lang)
    buf += _make_int32_field(16, 1)
    buf += _make_bytes_field(20, VERSION)     # OB55 client version (string)
    buf += _make_int32_field(21, 1)           # client flag
    buf += _make_bytes_field(22, FIELD22)     # 🔥 CLIENT SIGNATURE
    return bytes(buf)

def generate_name(prefix="AGJ"):
    symbols = [
        '◆','♣','☪','°','♛','「','ツ',
        '◉','অ','◊','웃','§','彡','★','ン',
        '•','乂','⍤','유','ッ','Ø','♪','Ж','⌂','シ','⊹',
        '·','∞','♡','✦','✧','◈','▪','§','অ','ৡ',
        'ʜ','ɪ','ᴋ','ᴍ','ʏ','ɚ','ɞ','『','「','」',
        '【','】','〔','〕','《','》','ッ','ジ','ュ','乂',
        '♣','♛','ⱨ','ҧ','ӡ','Ұ','ө','⋆','⋈',
    ]
    clean = re.sub(r'[^A-Za-z0-9]', '', prefix)[:5] or "AGJ"
    return clean + ''.join(random.choices(symbols, k=4))

# 🔥 Garena Default Hex Password Generator (Matches BD_accounts.json screenshot)
def generate_password():
    return os.urandom(32).hex().upper()

KEYSTREAM = [
    0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
    0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30
]
def encode_open_id(open_id: str) -> bytes:
    encoded = "".join(chr(ord(c) ^ KEYSTREAM[i % len(KEYSTREAM)]) for i, c in enumerate(open_id))
    esc = "".join(c if 32 <= ord(c) <= 126 else f"\\u{ord(c):04x}" for c in encoded)
    return codecs.decode(esc, "unicode_escape").encode("latin1")

def fetch_datadome_cookie():
    global DATADOME_COOKIE
    payload = {
        "cid": "r8MklXjdM4iDrouWrzdvCr0RxpuiQxl37cfUiRoLiwaJqQPjmalf7wgnzkYLbHA~nLtUJB4PwauRizIztlyqNJJfQ6BGdKlvqKDslrgFxPF3_MVkx659U5vdRR~TPgJK",
        "ddv": "1.13.9", "ddvc": "4.0.41",
        "ddk": "AE3F04AD3F0D3A462481A337485081",
        "request": "https://100067.connect.garena.com/api/v2/oauth/guest:register",
        "os": "Android", "osr": "9", "osn": "P", "osv": "28",
        "ua": "GarenaMSDK/4.0.41(SM-S908E ;Android 9;fr;FR;app 1.123.1 2019120270;)",
        "screen_x": "1600", "screen_y": "900", "screen_d": "240",
        "events": '[{"id":1,"message":"response validation","source":"sdk","date":1781377315862}]',
        "camera": '{"auth":"false","info":"{}"}',
        "mdl": "SM-S908E", "prd": "b0qxxx", "mnf": "samsung",
        "dev": "b0q", "hrd": "qcom",
        "fgp": "samsung/b0qxxx/b0q:9/TP1A.220624.014/S908EXXS2BWA2:user/release-keys",
        "tgs": "release-keys",
    }
    body = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api-sdk.datadome.co/sdk/", data=body, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Accept-Encoding": "gzip", "User-Agent": "okhttp/4.12.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=_ssl_ctx) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            j = json.loads(raw)
            cookie = j.get("cookie") or j.get("datadome") or j.get("dd_cookie")
            if cookie:
                if not cookie.startswith("datadome="): cookie = "datadome=" + cookie
                DATADOME_COOKIE = cookie
                return True
    except Exception: pass
    return False

def _http_post(url, data, headers, timeout=HTTP_TIMEOUT_FAST, proxy=None):
    if isinstance(data, str): data = data.encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    opener = _build_opener(proxy)
    try:
        resp = opener.open(req, timeout=timeout)
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            try: raw = gzip.decompress(raw)
            except Exception: pass
        return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read()
        if e.headers.get("Content-Encoding") == "gzip":
            try: raw = gzip.decompress(raw)
            except Exception: pass
        return e.code, raw
    except Exception as e:
        raise e

def _http_post_json(url, data, headers, timeout=HTTP_TIMEOUT_FAST, proxy=None):
    s, raw = _http_post(url, data, headers, timeout, proxy)
    try: j = json.loads(raw)
    except Exception: j = None
    return s, j

def garena_register(custom_pass="", proxy=None):
    password = custom_pass if custom_pass else generate_password()
    body = {"password": password, "client_type": 2, "source": 2, "app_id": 100067}
    json_data = json.dumps(body, separators=(",", ":"))
    sig = hmac.new(HMAC_KEY, json_data.encode("utf-8"), hashlib.sha256).hexdigest()
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": "Signature " + sig,
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "Connection": "close", "Accept-Encoding": "gzip",
        "Cookie": DATADOME_COOKIE,
    }
    status, j = _http_post_json(
        "https://100067.connect.garena.com/api/v2/oauth/guest:register",
        json_data, headers, timeout=HTTP_TIMEOUT_FAST, proxy=proxy
    )
    if j is None: return None, None
    if "url" in j and "captcha-delivery.com" in j.get("url", ""):
        raise RateLimitException("Datadome Captcha / Rate Limit Hit")
    if j.get("error") == "error_too_many_requests":
        raise RateLimitException("Too Many Requests")
    uid = j.get("data", {}).get("uid")
    if not uid: return None, None
    return uid, password

def garena_token(uid, password, retries=RETRY_TOKEN, proxy=None):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "100067.connect.garena.com",
        "Connection": "close", "Accept-Encoding": "gzip",
    }
    body = {
        "uid": uid, "password": password, "response_type": "token",
        "client_type": "2",
        "client_secret": HMAC_KEY.decode("utf-8"),
        "client_id": "100067",
    }
    json_data = json.dumps(body, separators=(",", ":"))
    url = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
    for attempt in range(retries):
        if shutdown_requested.is_set(): raise KeyboardInterrupt
        try:
            status, j = _http_post_json(url, json_data, headers, timeout=HTTP_TIMEOUT_FAST, proxy=proxy)
            if j is None: continue
            if "url" in j and "captcha-delivery.com" in j.get("url", ""):
                raise RateLimitException("Datadome Captcha in Token Grant")
            db = j.get("data", j)
            if "open_id" in db and "access_token" in db:
                return db["open_id"], db["access_token"]
        except RateLimitException: raise
        except Exception: pass
        time.sleep(0.3)
    raise Exception("garena_token failed after retries")

def major_register(access_token, open_id, field14, name, region="BD", proxy=None):
    login_base = REGION_LOGIN.get(region, REGION_LOGIN["BD"])
    headers = {
        "Accept-Encoding": "gzip", "Authorization": "Bearer",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "ReleaseVersion": OB,
        "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "X-GA": "v1 1", "X-Unity-Version": "2022.3.47f1",
    }
    proto_bytes = _build_major_register_proto(name, access_token, open_id, field14)
    raw = aes_encrypt(proto_bytes)
    status, content = _http_post(login_base + "MajorRegister", raw, headers, HTTP_TIMEOUT_FAST, proxy=proxy)
    return content, status

# =============================================================================
# 🔥 AGS ACTIVATOR API — USE YOUR OWN OR OUR ACTIVATOR SRC
# =============================================================================
def call_activator_api(uid, password, open_id, access_token, game_uid=0, region="BD", proxy=None):
    """Call the AGS Activator API to activate the account server-side."""
    payload = {
        "uid": str(uid),
        "password": str(password),
        "open_id": str(open_id),
        "access_token": str(access_token),
        "game_uid": str(game_uid) if game_uid else "",
        "region": str(region),
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
        "Connection": "close",
    }
    try:
        status, raw = _http_post(ACTIVATOR_API_URL, json.dumps(payload),
                                 headers, timeout=20, proxy=proxy)
        body_text = ""
        try:
            body_text = raw.decode("utf-8", errors="replace")
        except Exception:
            body_text = raw.hex()

        if status == 200:
            try:
                j = json.loads(body_text)
                return {"success": True, "response": j, "status": status, "raw": body_text}
            except Exception:
                return {"success": True, "response": body_text, "status": status, "raw": body_text}
        else:
            return {"success": False, "error": f"HTTP {status}: {body_text[:200]}",
                    "status": status, "raw": body_text}
    except Exception as e:
        return {"success": False, "error": str(e), "status": 0}

# =============================================================================
# HANDSHAKE & PROFILE
# =============================================================================
HEADER_SKIP = 64

def _act_strip_header(raw, n=HEADER_SKIP):
    if len(raw) <= n: return b""
    return raw[n:]

def _act_enc_proto(payload_dict):
    def _enc_varint(n):
        buf = bytearray()
        while True:
            b = n & 0x7F; n >>= 7
            if n: b |= 0x80
            buf.append(b)
            if not n: break
        return bytes(buf)
    def _make_varint(fn, v): return _enc_varint((fn << 3) | 0) + _enc_varint(v)
    def _make_bytes(fn, v):
        if isinstance(v, str): v = v.encode()
        return _enc_varint((fn << 3) | 2) + _enc_varint(len(v)) + v
    buf = bytearray()
    for f, v in payload_dict.items():
        if isinstance(v, dict): buf += _make_bytes(f, _act_enc_proto(v))
        elif isinstance(v, int): buf += _make_varint(f, v)
        elif isinstance(v, (str, bytes)): buf += _make_bytes(f, v)
    return _aes_cbc_encrypt(bytes(buf), AES_KEY, AES_IV)

def _act_build_login_payload(open_id, access_token, lang, region="BD"):
    verr = "2.132.5"
    payload = {
        3: str(datetime.now())[:-7],
        4: "free fire", 5: 1, 7: verr,
        8: "Android OS 15 / API-35 (AP3A.240905.015.A2/180019)",
        9: "Handheld", 10: "TUNTEL", 11: "WIFI",
        12: 1600, 13: 720, 14: "247",
        15: "ARM64 FP ASIMD AES | 1820 | 8",
        16: 2798, 17: "Mali-G57",
        18: "OpenGL ES 3.2 v1.r49p1-04eac0.2848c17a2fd4e9340e06555168eaa3c9",
        19: "Google|f744e396-5694-4e65-995d-97a958f2bd1f",
        20: "102.156.188.156", 21: lang, 22: open_id,
        23: "3", 24: "Handheld", 25: "INFINIX Infinix X6725",
        26: region, 29: access_token, 30: 1,
        41: "TUNTEL", 42: "WIFI",
        57: "7428b253defc164018c604a1ebbfebdf",
        60: 49973, 61: 3720, 62: 854, 64: 3848, 65: 49973, 66: 3848, 67: 49973,
        73: 2,
        74: "/data/app/~~eSPQu--bhSQDx0qVSCantw==/com.dts.freefireth-vZx-FXAnMdmzzvXGsuWZyw==/lib/arm64",
        76: 1,
        77: "1f74b435e72dfb267bce75a21d10074a|/data/app/~~eSPQu--bhSQDx0qVSCantw==/com.dts.freefireth-vZx-FXAnMdmzzvXGsuWZyw==/base.apk",
        78: 3, 79: 2, 81: "64", 83: "2019121040", 85: 3, 86: "OpenGLES2",
        87: 8191, 88: 3, 92: 14877, 93: "android",
        94: "KqsHTw/Pu89bWLI8IrlnJmIiCY6YqpSbCBdWNnQDYxboZ7JeQcOVP5M6uEbk+DUIl9ktJRhEFg6NjoW9Tvl1ZAh6R/8=",
        95: 111207,
        96: '{"cur_rate":[60,90,120],"support_etc2":false}',
        97: 1, 99: "4", 100: "4",
        102: "\u0011VA\u0014\u0002]\t\u0000c",
        104: 52882, 105: 1
    }
    return _act_enc_proto(payload)

def _act_major_login_for_jwt(access_token, open_id, lang="bn", region="BD", proxy=None):
    login_base = REGION_LOGIN.get(region, REGION_LOGIN["BD"])
    headers = {
        "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Accept": "*/*", "Accept-Encoding": "deflate, gzip",
        "X-GA-SV": str(int(time.time())),
        "Authorization": "Bearer", "X-GA": "v1 1",
        "ReleaseVersion": "OB55",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.12f1"
    }
    payload = _act_build_login_payload(open_id, access_token, lang, region)
    for attempt in range(3):
        if shutdown_requested.is_set(): raise KeyboardInterrupt
        try:
            status, content = _http_post(login_base + "MajorLogin", payload, headers, HTTP_TIMEOUT_NORMAL, proxy=proxy)
            if status != 200 or len(content) < 10:
                time.sleep(0.2); continue
            parsed = _decode_proto(_act_strip_header(content, HEADER_SKIP))
            jwt_token = _get_field(parsed, 8)
            if jwt_token: return jwt_token
        except Exception: pass
        time.sleep(0.2)
    return None

def _act_choose_newbie(jwt_token, game_uid, region="BD", proxy=None):
    login_base = REGION_LOGIN.get(region, REGION_LOGIN["BD"])
    url = login_base + "ChooseNewbieChoice"
    buf = bytearray()
    buf += _make_int64_field(1, _safe_int(game_uid))
    buf += _make_int32_field(2, 1)
    buf += _make_int32_field(3, 3)
    enc = aes_encrypt(bytes(buf))
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
        "Connection": "close", "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {jwt_token}", "X-Unity-Version": "2022.3.47f1",
        "X-GA": "v1 1", "ReleaseVersion": OB
    }
    try: _http_post(url, enc, headers, timeout=HTTP_TIMEOUT_FAST, proxy=proxy)
    except Exception: pass

def _act_choose_region(jwt_token, region_code, proxy=None):
    login_base = REGION_LOGIN.get(region_code, REGION_LOGIN["BD"])
    url = login_base + "ChooseRegion"
    buf = bytearray()
    buf += _make_bytes_field(1, region_code)
    buf += _make_int32_field(2, 1)
    enc = aes_encrypt(bytes(buf))
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
        "Connection": "close", "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {jwt_token}", "X-Unity-Version": "2022.3.47f1",
        "X-GA": "v1 1", "ReleaseVersion": OB
    }
    try: _http_post(url, enc, headers, timeout=HTTP_TIMEOUT_FAST, proxy=proxy)
    except Exception: pass

def _act_ping(token="", proxy=None):
    url = "https://clientbp.ppmainecoonghj.com/Ping"
    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {token}" if token else "Bearer",
        "Connection": "close", "Content-Type": "application/x-www-form-urlencoded",
        "ReleaseVersion": OB, "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1", "X-Unity-Version": "2022.3.47f1",
    }
    enc = bytes.fromhex("1a725b2c56ec52ba7d09623454c0a003")
    try: _http_post(url, enc, headers, timeout=HTTP_TIMEOUT_FAST, proxy=proxy)
    except Exception: pass

def set_account_bio(jwt_token, region="BD", proxy=None):
    if not jwt_token: return False
    base = REGION_CLIENT.get(region.upper(), "https://clientbp.ppmainecoonghj.com/")
    url = base + "UpdateSocialBasicInfo"
    headers = {
        "Expect": "100-continue",
        "X-Unity-Version": "2022.3.47f1",
        "X-GA": "v1 1",
        "ReleaseVersion": OB,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A505F Build/RP1A.200720.012)",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {jwt_token}"
    }
    try:
        bio_payload = bytes.fromhex(WORKING_BIO_PACKET_HEX)
        status, raw = _http_post(url, bio_payload, headers, timeout=HTTP_TIMEOUT_FAST, proxy=proxy)
        if status == 200: return True
    except Exception: pass
    try:
        raw_bio_bytes = bytes.fromhex(CUSTOM_LONG_BIO_HEX)
        pb = bytearray()
        pb += _make_bytes_field(1, raw_bio_bytes)
        enc_payload = aes_encrypt(bytes(pb))
        status, raw = _http_post(url, enc_payload, headers, timeout=HTTP_TIMEOUT_FAST, proxy=proxy)
        if status == 200: return True
    except Exception: pass
    return False

def activate_account(access_token, open_id, uid, password, reg_raw, region="BD", proxy=None):
    result = {"success": False, "game_uid": None, "details": {}}
    try:
        lang = REGION_LANG.get(region, "en")
        parsed_reg = _decode_proto(reg_raw) if isinstance(reg_raw, (bytes, bytearray)) else None
        account_uid = _safe_int(_get_field(parsed_reg, 3, 1, default=0)) if parsed_reg else 0
        jwt_token = _get_field(parsed_reg, 8) if parsed_reg else None

        if not jwt_token:
            jwt_token = _act_major_login_for_jwt(access_token, open_id, lang, region, proxy=proxy)
        if not jwt_token:
            result["details"]["error"] = "MajorLogin failed — no JWT"
            return result

        if account_uid:
            _act_choose_newbie(jwt_token, account_uid, region=region, proxy=proxy)
        _act_choose_region(jwt_token, region, proxy=proxy)
        _act_ping(jwt_token, proxy=proxy)

        jwt_token_final = _act_major_login_for_jwt(access_token, open_id, lang, region, proxy=proxy)
        if jwt_token_final:
            jwt_token = jwt_token_final

        result["success"] = True
        result["game_uid"] = account_uid or uid

        bio_ok = set_account_bio(jwt_token, region=region, proxy=proxy)
        result["details"]["bio_set"] = bio_ok

        return result
    except Exception as e:
        result["details"]["error"] = str(e)
        return result

# =============================================================================
# CORE ENGINE
# =============================================================================
def create_account(region="BD", custom_name_prefix="AGS_JOHIR", custom_pass="", use_proxy=False):
    if shutdown_requested.is_set(): return None

    for attempt in range(RETRY_CREATE_ACCOUNT):
        if shutdown_requested.is_set(): return None
        proxy = PROXY_MGR.get() if use_proxy else None
        try:
            uid, password = garena_register(custom_pass, proxy=proxy)
            if not uid:
                time.sleep(0.08); continue

            try:
                open_id, access_token = garena_token(uid, password, proxy=proxy)
            except RateLimitException: raise
            except Exception:
                time.sleep(0.08); continue

            name = generate_name(custom_name_prefix or "AGJ")
            field14 = encode_open_id(open_id)
            reg_raw, reg_status = major_register(access_token, open_id, field14, name, region, proxy=proxy)
            del field14

            if reg_status != 200:
                continue

            # parse account_id from MajorRegister response
            parsed_reg = _decode_proto(reg_raw) if isinstance(reg_raw, (bytes, bytearray)) else {}
            account_id_from_reg = _safe_int(_get_field(parsed_reg, 3, 1, default=0))

            # local activation
            activation = activate_account(access_token, open_id, uid, password, reg_raw, region, proxy=proxy)

            # 🔥 CALL AGS ACTIVATOR API
            activator = call_activator_api(
                uid=uid,
                password=password,
                open_id=open_id,
                access_token=access_token,
                game_uid=account_id_from_reg,
                region=region,
                proxy=proxy
            )

            real_game_uid = (activation.get("game_uid") or account_id_from_reg or uid)
            open_id_captured = bool(open_id and len(str(open_id)) > 5)
            active_ok = activation.get("success", False)
            bio_ok = activation.get("details", {}).get("bio_set", False)
            activator_ok = activator.get("success", False)

            res = {
                "access_token": access_token,
                "open_id": open_id,
                "uid": uid,
                "password": password,
                "name": name,
                "region": region,
                "account_id": real_game_uid,
                "open_id_status": "CAPTURED" if open_id_captured else "FAILED",
                "active_status": "SUCCESS" if active_ok else "FAILED",
                "bio_status": "SUCCESS" if bio_ok else "FAILED",
                "activator_status": "SUCCESS" if activator_ok else "FAILED",
                "activator_response": activator.get("response", activator.get("error", "")),
            }

            if active_ok and activator_ok:
                return res
            elif active_ok:
                # partial success — activator failed but local worked
                return res
            elif activator_ok:
                # activator succeeded but local failed — still return
                return res
        except RateLimitException: raise
        except Exception:
            time.sleep(0.08)
    return None

# =============================================================================
# RARITY & PERSISTENCE
# =============================================================================
ACCOUNT_RARITY_PATTERNS = {
    "REPEATED_DIGITS_4":       [r"(\d)\1{3,}", 3],
    "REPEATED_DIGITS_3":       [r"(\d)\1\1(\d)\2\2", 2],
    "SEQUENTIAL_5":            [r"(1234567|23456789)", 4],
    "SEQUENTIAL_4":            [r"(0123456|1234567|23456789)", 3],
    "PALINDROME_6":            [r"^(\d)(\d)(\d)\3\2\1$", 5],
    "PALINDROME_4":            [r"^(\d)(\d)\2\1$", 3],
    "SPECIAL_COMBINATIONS_HIGH":[r"(69696969|0000007)", 4],
    "SPECIAL_COMBINATIONS_MED": [r"(100000|200000|300000|400000|500000|666666|777777|888888|999999|017296)", 2],
    "QUADRUPLE_DIGITS":        [r"(111111|222222|333333|444444|555555|666666|777777|888888|999999|000000)", 4],
    "MIRROR_PATTERN_HIGH":     [r"^(\d{2,3})\1$", 3],
    "MIRROR_PATTERN_MED":      [r"(\d{2})0\1", 2],
    "GOLDEN_RATIO":            [r"16171819|55555", 3],
}

def check_account_rarity(account_id):
    account_id = str(account_id)
    if account_id == "N/A" or not account_id: return False, 0, []
    rarity_score = 0
    detected_patterns = []
    for rarity_type, pattern_data in ACCOUNT_RARITY_PATTERNS.items():
        if re.search(pattern_data[0], account_id):
            rarity_score += pattern_data[1]
            detected_patterns.append(rarity_type)
    digits = [int(d) for d in account_id if d.isdigit()]
    if len(digits) >= 4:
        if len(set(digits)) == 1:
            rarity_score += 5; detected_patterns.append("UNIFORM_DIGITS")
        diffs = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
        if len(set(diffs)) == 1:
            rarity_score += 4; detected_patterns.append("ARITHMETIC_SEQUENCE")
    if len(account_id) <= 8 and account_id.isdigit() and int(account_id) < 1000000:
        rarity_score += 3; detected_patterns.append("LOW_ACCOUNT_ID")
    return (rarity_score >= 3), rarity_score, detected_patterns

def save_result(result):
    is_rare, score, patterns = check_account_rarity(result["account_id"])
    region = result.get("region", "BD")

    entry = {
        "access_token": result["access_token"],
        "open_id":      result["open_id"],
        "uid":          result["uid"],
        "password":     result["password"],
        "name":         result.get("name", ""),
        "region":       region,
        "account_id":   result["account_id"],
        "online": "",
        "account": "",
        "active_status":    result.get("active_status", "FAILED"),
        "bio_status":       result.get("bio_status", "FAILED"),
        "activator_status": result.get("activator_status", "FAILED"),
        "created_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "credit":       "@restricted_zu | @ags_owner_atif"
    }

    with io_lock:
        with open(os.path.join(BASE_DIR, f"{region}_results.txt"), "a", encoding="utf-8") as f:
            f.write(f"{result['uid']}:{result['password']}\n")

        json_file = os.path.join(BASE_DIR, f"{region}_accounts.json")
        data = []
        if os.path.exists(json_file):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, list): data = []
            except Exception: data = []
        data.append(entry)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        if is_rare:
            rare_entry = entry.copy()
            rare_entry["rarity_score"] = score
            rare_entry["detected_patterns"] = patterns

            with open(os.path.join(RARE_DIR, f"rare_{region}.txt"), "a", encoding="utf-8") as f:
                f.write(f"{result['uid']}:{result['password']}:{result['account_id']}:{result.get('name','')} (Patterns: {patterns})\n")

            rare_json_file = os.path.join(RARE_DIR, f"rare_{region}.json")
            rare_data = []
            if os.path.exists(rare_json_file):
                try:
                    with open(rare_json_file, "r", encoding="utf-8") as f:
                        rare_data = json.load(f)
                    if not isinstance(rare_data, list): rare_data = []
                except Exception: rare_data = []
            rare_data.append(rare_entry)
            with open(rare_json_file, "w", encoding="utf-8") as f:
                json.dump(rare_data, f, indent=4, ensure_ascii=False)

    return is_rare

# =============================================================================
# 🎨 CRIMSON RED CENTERED TERMINAL UI
# =============================================================================
def banner():
    VisualMaster.clear()
    W = VisualMaster.get_term_width()
    banner_lines = [
        "██████╗ ██████╗ ███████╗ █████╗ ████████╗    ██╗ ██████╗ ██╗  ██╗██╗██████╗ ",
        "██╔════╝ ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝    ██║██╔═══██╗██║  ██║██║██╔══██╗",
        "██║  ███╗██████╔╝█████╗  ███████║   ██║       ██║██║   ██║███████║██║██████╔╝",
        "██║   ██║██╔══██╗██╔══╝  ██╔══██║   ██║  ██   ██║██║   ██║██╔══██║██║██╔══██╗",
        "╚██████╔╝██║  ██║███████╗██║  ██║   ██║  ╚█████╔╝╚██████╔╝██║  ██║██║██║  ██║",
        " ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
    ]
    gradient = [C2['blood_red'], C2['crimson_glow'], C2['orange_fire'],
                C2['gold'], C2['cyber_cyan'], C2['blood_red']]
    print()
    for i, line in enumerate(banner_lines):
        col = gradient[i % len(gradient)]
        print(f"{col}{C2['bold']}{VisualMaster.center_line(line)}{C2['reset']}")
    sub_border = "✦ " + "═" * min(38, W - 8) + " ✦"
    print(f"{C2['deep_red']}{VisualMaster.center_line(sub_border)}{C2['reset']}")
    print(f"{C2['blood_red']}{C2['bold']}{VisualMaster.center_line('⚡ AGS x JOHIR ULTIMATE MULTI-GEN v13.0 ⚡')}{C2['reset']}")
    print(f"{C2['crimson_glow']}{VisualMaster.center_line('◈ HIGH-SPEED CRIMSON PROTOCOL ◈ AES-128 ENCRYPTION ◈')}{C2['reset']}")
    print(f"{C2['deep_red']}{VisualMaster.center_line('═' * min(62, W - 2))}{C2['reset']}\n")

def print_account_box(idx, total, res, is_rare=False):
    BW = VisualMaster.get_box_width()
    INNER = BW - 2

    name    = str(res.get('name', ''))[:20]
    uid     = str(res.get('uid', ''))[:20]
    raw_pwd = str(res.get('password', ''))
    pwd     = mask_password(raw_pwd)[:24]
    acc_id  = str(res.get('account_id', ''))[:20]
    open_id = res.get('open_id_status', 'FAILED')
    region  = str(res.get('region', 'BD'))
    active_s= res.get('active_status', 'FAILED')
    bio_s   = res.get('bio_status', 'FAILED')
    act_s   = res.get('activator_status', 'FAILED')

    box_col = C2['blood_red']
    if is_rare:
        tag = f"💎 [RARE] [ AGS x JOHIR ] :: {idx}/{total}"
        head_bg = f"{C2['gold']}{C2['bold']}"
    else:
        tag = f"⚡ [SUCCESS] [ AGS x JOHIR ] :: {idx}/{total}"
        head_bg = f"{C2['crimson_glow']}{C2['bold']}"

    top_line = f"╔═[ AGS x JOHIR ]{'═' * max(0, INNER - 18)}╗"
    head_line = f"║ {_pad(head_bg + tag + C2['reset'], INNER - 2, 'center')} ║"
    mid_line = f"╠{'═' * INNER}╣"

    print(f"\n{box_col}" + VisualMaster.center_line(top_line) + f"{C2['reset']}")
    print(f"{box_col}" + VisualMaster.center_line(head_line) + f"{C2['reset']}")
    print(f"{box_col}" + VisualMaster.center_line(mid_line) + f"{C2['reset']}")

    def line_row(label, val, val_col):
        tag_str = f" {C2['blood_red']}▶{C2['reset']} {C2['pure_white']}{label:<12}{C2['reset']}: {val_col}{C2['bold']}{val}{C2['reset']}"
        row = f"║{_pad(tag_str, INNER)}║"
        print(f"{box_col}" + VisualMaster.center_line(row) + f"{C2['reset']}")

    line_row("PLAYER NAME",   name, C2['plasma_pink'])
    line_row("USER UID",      uid, C2['cyber_cyan'])
    line_row("PASS (MASK)",   pwd, C2['orange_fire'])
    line_row("ACCOUNT ID",    acc_id, C2['gold'])
    line_row("SERVER ZONE",   region, C2['crimson_glow'])

    st_open = f"{C2['matrix_green']}CAPTURED [VERIFIED]" if open_id == 'CAPTURED' else f"{C2['blood_red']}FAILED"
    st_bio  = f"{C2['matrix_green']}INJECTED [OB55]" if bio_s == 'SUCCESS' else f"{C2['blood_red']}MISSED"
    st_act  = f"{C2['matrix_green']}ONLINE [PERFECT]" if active_s == 'SUCCESS' else f"{C2['blood_red']}ERROR"
    st_avt  = f"{C2['matrix_green']}ACTIVATED [AGS]" if act_s == 'SUCCESS' else f"{C2['blood_red']}FAILED"

    line_row("OPEN-ID",       st_open, C2['reset'])
    line_row("LOCAL ACT",     st_act, C2['reset'])
    line_row("ACTIVATOR",     st_avt, C2['reset'])
    line_row("BIO INJECT",    st_bio, C2['reset'])
    line_row("CIPHER MODE",   "ENCRYPTED (AES-128)", C2['dim'])

    bot_line = f"╚{'═' * max(0, INNER - 17)}[ AGS x JOHIR ]═╝"
    print(f"{box_col}" + VisualMaster.center_line(bot_line) + f"{C2['reset']}")

def print_summary(success, rare_count, total, elapsed, base_dir, region):
    BW = VisualMaster.get_box_width()
    INNER = BW - 2
    border = C2['blood_red']

    top_line = f"╔═[ REPORT ]{'═' * max(0, INNER - 11)}╗"
    head_line = f"║ {_pad(C2['crimson_glow'] + C2['bold'] + '⚡ AGS x JOHIR PERFORMANCE REPORT ⚡' + C2['reset'], INNER - 2, 'center')} ║"
    mid_line = f"╠{'═' * INNER}╣"

    print(f"\n{border}" + VisualMaster.center_line(top_line) + f"{C2['reset']}")
    print(f"{border}" + VisualMaster.center_line(head_line) + f"{C2['reset']}")
    print(f"{border}" + VisualMaster.center_line(mid_line) + f"{C2['reset']}")

    def stat_row(k, v, color=C2['pure_white']):
        row_str = f" {C2['blood_red']}◆{C2['reset']} {C2['pure_white']}{k:<18}{C2['reset']}: {color}{C2['bold']}{v}{C2['reset']}"
        row = f"║{_pad(row_str, INNER)}║"
        print(f"{border}" + VisualMaster.center_line(row) + f"{C2['reset']}")

    speed_val = round(success / elapsed, 2) if elapsed else 0
    stat_row("Total Success",     f"{success} of {total} accounts", C2['cyber_cyan'])
    stat_row("Special Rares",     f"{rare_count} items detected", C2['gold'])
    stat_row("Server Gateway",    f"{region} (Garena BP Cluster)", C2['crimson_glow'])
    stat_row("Total Runtime",     f"{elapsed} seconds", C2['orange_fire'])
    stat_row("Creation Speed",    f"{speed_val} acc/sec (Turbo)", C2['matrix_green'])
    stat_row("File Location",     base_dir + "/", C2['cyber_cyan'])
    stat_row("Master Creator",    "AGS x JOHIR (@restricted_zu)", C2['plasma_pink'])

    bot_line = f"╚{'═' * max(0, INNER - 17)}[ AGS x JOHIR ]═╝"
    print(f"{border}" + VisualMaster.center_line(bot_line) + f"{C2['reset']}\n")

# =============================================================================
# CONTROLLER
# =============================================================================
def _install_signal_handlers():
    def _handler(signum, frame):
        if not shutdown_requested.is_set():
            shutdown_requested.set()
            print(VisualMaster.center_line(f"\n{C2['orange_fire']}{C2['bold']}⚠️  Stopping engine — completing workers…{C2['reset']}"))
        else:
            print(VisualMaster.center_line(f"\n{C2['blood_red']}{C2['bold']}Force Terminated.{C2['reset']}"))
            os.kill(os.getpid(), signal.SIGKILL)
    try:
        signal.signal(signal.SIGINT,  _handler)
        signal.signal(signal.SIGTERM, _handler)
    except (ValueError, OSError): pass

def main():
    _install_signal_handlers()
    banner()

    W = VisualMaster.get_term_width()
    BW = VisualMaster.get_box_width()
    INNER = BW - 2
    bc = C2['blood_red']

    # ---------------- PROXY SELECTION MENU ----------------
    top_pxy = f"╔═[ PROXY NETWORK ROUTING ]{'═' * max(0, INNER - 25)}╗"
    head_pxy = f"║ {_pad(C2['crimson_glow'] + C2['bold'] + '★ SELECT PROXY PREFERENCE ★' + C2['reset'], INNER - 2, 'center')} ║"
    mid_pxy = f"╠{'═' * INNER}╣"
    p1 = f"║  {C2['cyber_cyan']}[1]{C2['reset']} Auto-Fetch Free Online Proxies (Anti-Ban proxies.txt){_pad('', max(0, INNER - 56))} ║"
    p2 = f"║  {C2['cyber_cyan']}[2]{C2['reset']} Direct Connection (No Proxy - Fastest Mode){_pad('', max(0, INNER - 47))} ║"
    bot_pxy = f"╚{'═' * INNER}╝"

    print(f"{bc}" + VisualMaster.center_line(top_pxy) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(head_pxy) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(mid_pxy) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(p1) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(p2) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(bot_pxy) + f"{C2['reset']}\n")

    indent = " " * ((W - BW) // 2 + 2)
    proxy_choice = input(f"{indent}{C2['orange_fire']}➤ {C2['pure_white']}Network Mode (1-2) [Enter=1]: {C2['crimson_glow']}").strip() or "1"
    print(C2['reset'], end="")

    use_proxy = False
    if proxy_choice == "1":
        print(VisualMaster.center_line(f"{C2['cyber_cyan']}⚡ Fetching fresh public proxies into proxies.txt...{C2['reset']}"))
        p_count = PROXY_MGR.fetch_online_proxies(count=100)
        if p_count > 0:
            use_proxy = True
            print(VisualMaster.center_line(f"{C2['matrix_green']}✔ Proxy Chain Active: Loaded {p_count} online proxies!{C2['reset']}\n"))
        else:
            print(VisualMaster.center_line(f"{C2['orange_fire']}⚠ Failed to fetch online proxies — Falling back to Direct Route{C2['reset']}\n"))
    else:
        print(VisualMaster.center_line(f"{C2['orange_fire']}⚡ Direct Network Active: High-speed connection enabled{C2['reset']}\n"))

    # ---------------- REGION SELECT ----------------
    top_line = f"╔═[ REGION SELECT ]{'═' * max(0, INNER - 18)}╗"
    head_line = f"║ {_pad(C2['crimson_glow'] + C2['bold'] + '★ SELECT TARGET SERVER GATEWAY ★' + C2['reset'], INNER - 2, 'center')} ║"
    mid_line = f"╠{'═' * INNER}╣"
    r1 = f"║  {C2['cyber_cyan']}[1]{C2['reset']} Bangladesh (BD)   {C2['cyber_cyan']}[2]{C2['reset']} India (IND)      {_pad('', max(0, INNER - 38))} ║"
    r2 = f"║  {C2['cyber_cyan']}[3]{C2['reset']} Pakistan (PK)     {C2['cyber_cyan']}[4]{C2['reset']} Singapore (SG)   {_pad('', max(0, INNER - 38))} ║"
    r3 = f"║  {C2['cyber_cyan']}[5]{C2['reset']} Indonesia (ID)    {C2['cyber_cyan']}[6]{C2['reset']} Middle East (ME) {_pad('', max(0, INNER - 38))} ║"
    bot_line = f"╚{'═' * INNER}╝"

    print(f"{bc}" + VisualMaster.center_line(top_line) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(head_line) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(mid_line) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(r1) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(r2) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(r3) + f"{C2['reset']}")
    print(f"{bc}" + VisualMaster.center_line(bot_line) + f"{C2['reset']}\n")

    region_map = {"1": "BD", "2": "IND", "3": "PK", "4": "SG", "5": "ID", "6": "ME"}
    choice = input(f"{indent}{C2['orange_fire']}➤ {C2['pure_white']}Cluster Gateway (1-6) [Enter=1]: {C2['crimson_glow']}").strip() or "1"
    print(C2['reset'], end="")
    region = region_map.get(choice, "BD")

    try:
        total_inp = input(f"{indent}{C2['orange_fire']}➤ {C2['pure_white']}Target Count [Enter=1]: {C2['crimson_glow']}").strip()
        print(C2['reset'], end="")
        total = int(total_inp) if total_inp else 1
    except ValueError: total = 1

    user_name = input(f"{indent}{C2['orange_fire']}➤ {C2['pure_white']}Player Tag Prefix [ENTER=AGJ]: {C2['crimson_glow']}").strip() or "AGJ"
    print(C2['reset'])

    print(VisualMaster.center_line(f"{C2['cyber_cyan']}⚡ Connecting to Datadome Cloud Service...{C2['reset']}"))
    fetch_datadome_cookie()
    print(VisualMaster.center_line(f"{C2['matrix_green']}✔ Handshake verified — Token initialized!{C2['reset']}\n"))

    max_workers = min(MAX_WORKERS_HARD, max(total, 1))
    print(VisualMaster.center_line(f"{C2['crimson_glow']}⚡ Spawning {max_workers} Workers for Region: {region}...{C2['reset']}"))
    print(VisualMaster.center_line(f"{C2['blood_red']}{'═' * BW}{C2['reset']}\n"))

    accounts: list = []
    success    = 0
    rare_count = 0
    lock       = threading.Lock()
    dd_counter = [0]
    fail_counter = [0]
    start_time = time.time()

    def creator():
        nonlocal success, rare_count
        while not shutdown_requested.is_set():
            with lock:
                if success >= total: break
                dd_counter[0] += 1
                should_refresh = (dd_counter[0] % DD_REFRESH_INTERVAL == 0)
            if should_refresh:
                with dd_lock: fetch_datadome_cookie()
            try:
                res = create_account(region, user_name, "", use_proxy=use_proxy)
                if res and (res.get("active_status") == "SUCCESS" or res.get("activator_status") == "SUCCESS"):
                    with lock:
                        if success >= total or shutdown_requested.is_set(): break
                        is_rare = save_result(res)
                        accounts.append(res)
                        success += 1
                        if is_rare: rare_count += 1
                        current_num = success
                    with print_lock:
                        print_account_box(current_num, total, res, is_rare)
                    time.sleep(REQUEST_DELAY)
                else:
                    with lock: fail_counter[0] += 1
                    time.sleep(0.15)
            except RateLimitException:
                with dd_lock:
                    fetch_datadome_cookie()
                time.sleep(2.5)
            except KeyboardInterrupt: break
            except Exception:
                time.sleep(0.2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = [ex.submit(creator) for _ in range(max_workers)]
        for f in futs:
            try: f.result()
            except Exception: pass

    elapsed_time = round(time.time() - start_time, 2)
    print_summary(success, rare_count, total, elapsed_time, BASE_DIR, region)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        shutdown_requested.set()
        print(VisualMaster.center_line(f"\n{C2['orange_fire']}Execution safely halted by user.{C2['reset']}"))
        os.kill(os.getpid(), signal.SIGKILL)
