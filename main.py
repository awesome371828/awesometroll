import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import keyboard
import time
import random
import re
import threading
import sys
import json
import os
import sqlite3
import hashlib
import uuid
import subprocess
import platform
from datetime import datetime, timedelta
import ctypes
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ============================================================
# СКРЫТИЕ КОНСОЛИ
# ============================================================

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

hide_console()

# ============================================================
# КОНСТАНТЫ
# ============================================================
DEVELOPER = "@flidges"
CREATOR_TEXT = "✨ Создатель: awesome / tg @flidges ✨"
VERSION = "3.0"
LOVE_TEXT = "💜 Сделано с любовью и матом 💜"
APP_NAME = "AWESOMETROLLING"
PRICE_TEXT = "💰 Цена - узнайте у @flidges"
MASTER_KEY = "awesminute"

COLORS = {
    'bg': '#0a0e27', 'bg2': '#111638', 'bg3': '#1a1f4a', 'bg4': '#222860',
    'bg5': '#2d3570', 'gradient_start': '#6c5ce7', 'gradient_end': '#fd79a8',
    'accent': '#6c5ce7', 'accent2': '#a29bfe', 'pink': '#fd79a8',
    'text': '#dfe6e9', 'text2': '#b2bec3', 'text3': '#636e72',
    'success': '#00b894', 'danger': '#e17055', 'warning': '#fdcb6e',
    'gold': '#ffd700', 'neon': '#00ff88', 'neon_orange': '#ff6b35',
    'neon_blue': '#4fc3f7', 'shadow': '#1a1f4a'
}

# ============================================================
# ШИФРОВАНИЕ
# ============================================================

class CryptoEngine:
    _SALT_B64 = b'YXdlc29tZXBsb2swMQ=='
    
    @classmethod
    def _get_salt(cls):
        return hashlib.sha256(base64.b64decode(cls._SALT_B64)).digest()[:16]
    
    @classmethod
    def _get_system_key(cls):
        parts = [platform.node(), platform.processor(), platform.machine(), str(os.cpu_count()), 
                os.environ.get('PROCESSOR_IDENTIFIER', ''), os.environ.get('COMPUTERNAME', '')]
        combined = '|'.join(parts) + base64.b64decode(cls._SALT_B64).decode()
        return hashlib.sha512(combined.encode()).hexdigest()
    
    @classmethod
    def _derive_master_key(cls):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=cls._get_salt(), iterations=300000)
        return base64.urlsafe_b64encode(kdf.derive(cls._get_system_key().encode()))
    
    @classmethod
    def encrypt(cls, data):
        if data is None: return None
        try:
            if isinstance(data, str): data = data.encode('utf-8')
            elif not isinstance(data, bytes): data = str(data).encode('utf-8')
            return Fernet(cls._derive_master_key()).encrypt(data)
        except:
            key = hashlib.sha512(cls._get_system_key().encode()).digest()
            result = bytearray()
            for i, byte in enumerate(data):
                result.append(byte ^ key[i % len(key)])
            return bytes(result)
    
    @classmethod
    def decrypt(cls, encrypted_data):
        if encrypted_data is None: return None
        try:
            if isinstance(encrypted_data, str): encrypted_data = encrypted_data.encode('utf-8')
            decrypted = Fernet(cls._derive_master_key()).decrypt(encrypted_data)
            try: return decrypted.decode('utf-8')
            except: return decrypted
        except:
            key = hashlib.sha512(cls._get_system_key().encode()).digest()
            result = bytearray()
            for i, byte in enumerate(encrypted_data):
                result.append(byte ^ key[i % len(key)])
            try: return result.decode('utf-8')
            except: return result

# ============================================================
# ПУТИ
# ============================================================

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

APP_DIR = get_app_dir()
DB_FILE = os.path.join(APP_DIR, "troll_users.db")
SETTINGS_FILE = os.path.join(APP_DIR, "troll_settings.json")
LICENSE_FILE = os.path.join(APP_DIR, "license.key")

# ============================================================
# HWID
# ============================================================

class ComputerID:
    @staticmethod
    def get_mac():
        try:
            mac = uuid.getnode()
            return ':'.join(('%012x' % mac)[i:i+2] for i in range(0, 12, 2))
        except:
            return "unknown_mac"
    
    @staticmethod
    def get_computer_name():
        try:
            return os.environ.get('COMPUTERNAME', 'unknown')
        except:
            return "unknown"
    
    @staticmethod
    def get_username():
        try:
            return os.environ.get('USERNAME', 'unknown')
        except:
            return "unknown"
    
    @staticmethod
    def get_disk_serial():
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['wmic', 'diskdrive', 'get', 'serialnumber'], capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    return lines[1].strip()
            return "unknown_disk"
        except:
            return "unknown_disk"
    
    @staticmethod
    def get_cpu_id():
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['wmic', 'cpu', 'get', 'processorid'], capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    return lines[1].strip()
            return "unknown_cpu"
        except:
            return "unknown_cpu"
    
    @staticmethod
    def get_full_hwid():
        data = (ComputerID.get_mac() + ComputerID.get_computer_name() + ComputerID.get_username() + 
                ComputerID.get_disk_serial() + ComputerID.get_cpu_id() + platform.processor() + platform.machine())
        encrypted = CryptoEngine.encrypt(data)
        return hashlib.sha512(encrypted).hexdigest()[:64]

# ============================================================
# БАЗА ДАННЫХ С ПРИВЯЗКОЙ К HWID
# ============================================================

class UserDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            hwid TEXT UNIQUE NOT NULL,
            mac TEXT, computer_name TEXT,
            is_owner INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            created_at TEXT, expires_at TEXT, last_active TEXT,
            saved_key TEXT
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS license_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_text TEXT UNIQUE NOT NULL,
            created_at TEXT, expires_at TEXT,
            used_by TEXT, 
            used_hwid TEXT,
            used_at TEXT,
            is_used INTEGER DEFAULT 0,
            owner_hwid TEXT
        )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT, action TEXT, timestamp TEXT
        )''')
        self.conn.commit()
    
    def _encrypt_field(self, value):
        if value is None: return None
        return CryptoEngine.encrypt(value)
    
    def _decrypt_field(self, value):
        if value is None: return None
        return CryptoEngine.decrypt(value)
    
    def get_hwid(self):
        return ComputerID.get_full_hwid()
    
    def check_master_key(self, key):
        return key.upper() == MASTER_KEY.upper()
    
    def is_owner(self):
        hwid = self.get_hwid()
        encrypted_hwid = CryptoEngine.encrypt(hwid)
        result = self.cursor.execute('SELECT is_owner FROM users WHERE hwid = ?', (encrypted_hwid,)).fetchone()
        return result and result[0] == 1
    
    def save_license(self, key):
        encrypted_key = CryptoEngine.encrypt(key)
        with open(LICENSE_FILE, 'w') as f:
            f.write(base64.b64encode(encrypted_key).decode('utf-8'))
    
    def load_license(self):
        if os.path.exists(LICENSE_FILE):
            try:
                with open(LICENSE_FILE, 'r') as f:
                    encrypted_key = base64.b64decode(f.read().strip().encode('utf-8'))
                return CryptoEngine.decrypt(encrypted_key)
            except:
                return None
        return None
    
    def delete_license(self):
        if os.path.exists(LICENSE_FILE):
            os.remove(LICENSE_FILE)
    
    def generate_key(self, months=1, custom_key=None):
        key = custom_key if custom_key else hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()[:12].upper()
        created_at = datetime.now().isoformat()
        expires_at = (datetime.now() + timedelta(days=30 * months)).isoformat()
        owner_hwid = self.get_hwid()
        
        try:
            self.cursor.execute('''INSERT INTO license_keys 
                (key_text, created_at, expires_at, is_used, owner_hwid) 
                VALUES (?, ?, ?, 0, ?)''', 
                (CryptoEngine.encrypt(key), CryptoEngine.encrypt(created_at), 
                 CryptoEngine.encrypt(expires_at), CryptoEngine.encrypt(owner_hwid)))
            self.conn.commit()
            return True, key
        except sqlite3.IntegrityError:
            return False, None
    
    def delete_key(self, key_text):
        self.cursor.execute('DELETE FROM license_keys WHERE key_text = ?', (CryptoEngine.encrypt(key_text),))
        self.conn.commit()
        return True
    
    def activate_key(self, key_text, save=True):
        hwid = self.get_hwid()
        username = ComputerID.get_username()
        key_upper = key_text.upper()
        
        # === МАСТЕР-КЛЮЧ ===
        if self.check_master_key(key_upper):
            encrypted_hwid = CryptoEngine.encrypt(hwid)
            encrypted_username = CryptoEngine.encrypt(username)
            encrypted_expires = CryptoEngine.encrypt("2099-12-31T23:59:59")
            encrypted_key = CryptoEngine.encrypt(key_upper)
            
            user = self.cursor.execute('SELECT * FROM users WHERE hwid = ?', (encrypted_hwid,)).fetchone()
            if user:
                self.cursor.execute('''UPDATE users SET 
                    username = ?, is_owner = 1, is_admin = 1, is_banned = 0, 
                    expires_at = ?, saved_key = ? WHERE hwid = ?''', 
                    (encrypted_username, encrypted_expires, encrypted_key, encrypted_hwid))
            else:
                self.cursor.execute('''INSERT INTO users 
                    (username, hwid, is_owner, is_admin, created_at, expires_at, saved_key) 
                    VALUES (?, ?, 1, 1, ?, ?, ?)''',
                    (encrypted_username, encrypted_hwid, 
                     CryptoEngine.encrypt(datetime.now().isoformat()), 
                     encrypted_expires, encrypted_key))
            self.conn.commit()
            if save:
                self.save_license(key_upper)
            return True, "👑 ДОБРО ПОЖАЛОВАТЬ, ОВНЕР!"
        
        # === ОБЫЧНЫЙ КЛЮЧ ===
        encrypted_key = CryptoEngine.encrypt(key_upper)
        result = self.cursor.execute('''SELECT key_text, expires_at, is_used, used_hwid, owner_hwid 
            FROM license_keys WHERE key_text = ?''', (encrypted_key,)).fetchone()
        
        if not result:
            return False, "❌ НЕВЕРНЫЙ КЛЮЧ!"
        
        key_enc, expires_enc, is_used, used_hwid_enc, owner_hwid_enc = result
        expires_at = CryptoEngine.decrypt(expires_enc)
        used_hwid = CryptoEngine.decrypt(used_hwid_enc) if used_hwid_enc else None
        owner_hwid = CryptoEngine.decrypt(owner_hwid_enc) if owner_hwid_enc else None
        
        # === ПРОВЕРКА ОВНЕРА ===
        if owner_hwid and owner_hwid != hwid:
            return False, "❌ ЭТОТ КЛЮЧ НЕ ДЛЯ ТВОЕГО КОМПЬЮТЕРА!"
        
        # === ПРОВЕРКА ИСПОЛЬЗОВАНИЯ ===
        if is_used and used_hwid and used_hwid != hwid:
            return False, "❌ КЛЮЧ УЖЕ АКТИВИРОВАН НА ДРУГОМ КОМПЬЮТЕРЕ!"
        
        if is_used and used_hwid == hwid:
            expiry = datetime.fromisoformat(expires_at)
            if datetime.now() > expiry:
                return False, f"❌ КЛЮЧ ИСТЕК {expiry.strftime('%d.%m.%Y')}!"
            return True, f"✅ ДОСТУП УЖЕ АКТИВИРОВАН ДО {expiry.strftime('%d.%m.%Y')}!"
        
        # === ПРОВЕРКА СРОКА ===
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return False, f"❌ КЛЮЧ ИСТЕК {expiry.strftime('%d.%m.%Y')}!"
        
        # === АКТИВАЦИЯ ===
        self.cursor.execute('''UPDATE license_keys SET 
            used_by = ?, used_hwid = ?, used_at = ?, is_used = 1 
            WHERE key_text = ?''',
            (CryptoEngine.encrypt(username), CryptoEngine.encrypt(hwid), 
             CryptoEngine.encrypt(datetime.now().isoformat()), encrypted_key))
        
        user = self.cursor.execute('SELECT * FROM users WHERE hwid = ?', (CryptoEngine.encrypt(hwid),)).fetchone()
        if user:
            self.cursor.execute('''UPDATE users SET 
                username = ?, expires_at = ?, is_banned = 0, saved_key = ? 
                WHERE hwid = ?''', 
                (CryptoEngine.encrypt(username), expires_enc, encrypted_key, CryptoEngine.encrypt(hwid)))
        else:
            self.cursor.execute('''INSERT INTO users 
                (username, hwid, created_at, expires_at, saved_key) 
                VALUES (?, ?, ?, ?, ?)''',
                (CryptoEngine.encrypt(username), CryptoEngine.encrypt(hwid), 
                 CryptoEngine.encrypt(datetime.now().isoformat()), expires_enc, encrypted_key))
        
        self.conn.commit()
        if save:
            self.save_license(key_upper)
        return True, f"✅ ВЕРНО! ДОСТУП ДО {expiry.strftime('%d.%m.%Y')}!"
    
    def check_access_auto(self):
        saved_key = self.load_license()
        if saved_key:
            success, msg = self.activate_key(saved_key, save=False)
            if success:
                return True, msg
        return False, None
    
    def check_access(self):
        hwid = self.get_hwid()
        encrypted_hwid = CryptoEngine.encrypt(hwid)
        result = self.cursor.execute('''SELECT username, is_owner, is_admin, is_banned, expires_at 
            FROM users WHERE hwid = ?''', (encrypted_hwid,)).fetchone()
        
        if not result:
            return False, "🔑 ТРЕБУЕТСЯ АКТИВАЦИЯ!"
        
        username_enc, is_owner, is_admin, is_banned, expires_enc = result
        username = CryptoEngine.decrypt(username_enc)
        expires_at = CryptoEngine.decrypt(expires_enc)
        
        if is_banned:
            return False, "🚫 ДОСТУП ЗАБЛОКИРОВАН!"
        
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return False, f"⏰ ПОДПИСКА ИСТЕКЛА {expiry.strftime('%d.%m.%Y')}!"
        
        self.cursor.execute('UPDATE users SET last_active = ? WHERE hwid = ?', 
                           (CryptoEngine.encrypt(datetime.now().isoformat()), encrypted_hwid))
        self.conn.commit()
        return True, username
    
    def logout(self):
        self.delete_license()
        return True
    
    def get_all_users(self):
        users = self.cursor.execute('''SELECT username, is_owner, is_admin, is_banned, 
            expires_at, hwid, saved_key FROM users ORDER BY is_owner DESC, is_admin DESC''').fetchall()
        decrypted_users = []
        for user in users:
            username_enc, is_owner, is_admin, is_banned, expires_enc, hwid_enc, saved_key_enc = user
            decrypted_users.append((
                CryptoEngine.decrypt(username_enc),
                is_owner,
                is_admin,
                is_banned,
                CryptoEngine.decrypt(expires_enc),
                CryptoEngine.decrypt(hwid_enc),
                CryptoEngine.decrypt(saved_key_enc) if saved_key_enc else None
            ))
        return decrypted_users
    
    def get_all_keys(self):
        keys = self.cursor.execute('''SELECT key_text, created_at, expires_at, 
            used_by, used_hwid, is_used, owner_hwid 
            FROM license_keys ORDER BY created_at DESC''').fetchall()
        decrypted_keys = []
        for key in keys:
            key_enc, created_enc, expires_enc, used_by_enc, used_hwid_enc, is_used, owner_hwid_enc = key
            decrypted_keys.append((
                CryptoEngine.decrypt(key_enc),
                CryptoEngine.decrypt(created_enc),
                CryptoEngine.decrypt(expires_enc),
                CryptoEngine.decrypt(used_by_enc) if used_by_enc else None,
                CryptoEngine.decrypt(used_hwid_enc) if used_hwid_enc else None,
                is_used,
                CryptoEngine.decrypt(owner_hwid_enc) if owner_hwid_enc else None
            ))
        return decrypted_keys
    
    def give_access(self, username, months=1):
        expires_at = (datetime.now() + timedelta(days=30 * months)).isoformat()
        encrypted_username = CryptoEngine.encrypt(username)
        encrypted_expires = CryptoEngine.encrypt(expires_at)
        
        user = self.cursor.execute('SELECT * FROM users WHERE username = ?', (encrypted_username,)).fetchone()
        if user:
            self.cursor.execute('UPDATE users SET expires_at = ?, is_banned = 0 WHERE username = ?', 
                               (encrypted_expires, encrypted_username))
        else:
            self.cursor.execute('INSERT INTO users (username, hwid, created_at, expires_at) VALUES (?, ?, ?, ?)',
                               (encrypted_username, CryptoEngine.encrypt(f"MANUAL_{uuid.uuid4().hex[:8]}"), 
                                CryptoEngine.encrypt(datetime.now().isoformat()), encrypted_expires))
        self.conn.commit()
        return True, f"✅ ДОСТУП ВЫДАН {username} НА {months} МЕСЯЦЕВ!"
    
    def revoke_access(self, username):
        self.cursor.execute('UPDATE users SET is_banned = 1 WHERE username = ?', (CryptoEngine.encrypt(username),))
        self.conn.commit()
        return True
    
    def restore_access(self, username):
        self.cursor.execute('UPDATE users SET is_banned = 0 WHERE username = ?', (CryptoEngine.encrypt(username),))
        self.conn.commit()
        return True
    
    def extend_access(self, username, months=1):
        result = self.cursor.execute('SELECT expires_at FROM users WHERE username = ?', (CryptoEngine.encrypt(username),)).fetchone()
        if result:
            expires_enc = result[0]
            expires_at = CryptoEngine.decrypt(expires_enc)
            new_expiry = datetime.fromisoformat(expires_at) + timedelta(days=30 * months)
            self.cursor.execute('UPDATE users SET expires_at = ? WHERE username = ?', 
                               (CryptoEngine.encrypt(new_expiry.isoformat()), CryptoEngine.encrypt(username)))
            self.conn.commit()
            return True, f"✅ ПРОДЛЕН ДО {new_expiry.strftime('%d.%m.%Y')}!"
        return False, "❌ ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН!"

db = UserDB()

# ============================================================
# ОСТАЛЬНОЙ КОД (Интерфейс, кнопки, спам и т.д.)
# ============================================================

INSULT_TEMPLATES = [
    "я твою мать в жопу ебал пока ты тут сопли свои распускал а ты сынок шлюхи на меня рот открыл",
    "я твою мать нахуй послал и она там осталась а ты гандон сраный тут мне перечить вздумал",
    "я твою мать расчленил нахуй и по кускам разбросал а ты чурка ебаный на меня пасть открываешь",
    "я твоего отца отпиздил ногами и хуем пронзил насквозь а ты хуесос ебаный тут мне пиздишь",
    "я твоего батю своим членом насадил как шашлык а ты сынок шалавы тут мне слова поперек сказать пытаешься",
    "я твоего отца в гробу перевернул своим хуем и он там от стыда сгорел а ты педик гнилой",
    "я твою сестру в жопу трахал пока ты тут пиздел а она сказала что ты хуже меня во всем",
    "я твою сестру за волосы таскал и в жопу ебал пока она не поняла кто тут главный",
    "я твою сестру нахуй выебал и она теперь моя потому что ты ничтожество полное",
    "я твою бабку своей залупой по стенке размазал и она теперь как картина висит",
    "я твою бабку в гробу трахнул и она там от стыда перевернулась два раза а ты хач ебаный",
    "я твою бабку нахуй послал и она там осталась потому что старой уже некуда деваться было",
    "я твою мать и сестру твою в жопу ебал а ты пидор конченный на моём хуе сидишь",
    "я твоего отца и деда твоего расчленил нахуй а ты сын шлюхи ебаный тут мне перечить вздумал",
    "я твою родню всю вырезал нахуй и по ветру развеял а ты уебан конченный на меня пасть открываешь",
    "я тебя своим хуем как битой стальной отпизжу так что ты молиться будешь чтоб я тебя больше не трогал",
    "я тебя просто нахуй прожгу насквозь своим божественным членом все твои хлипкие органы будут прогорать",
    "от моего хуя идет свет такой что даже твои очки тебя не защитят я тебя просто нахуй ослеплю",
    "ты как собака нахуй лаешь а я тебя как щенка за шкирку возьму и в окно выкину нахуй",
    "ты как свинья жирная тут хрюкаешь а я тебя на шашлык пущу и съем без соли",
    "ты как таракан ебаный ползаешь под моими ногами и я тебя раздавлю как букашку",
    "я бог а ты просто жалкий червяк я тебя ногтем раздавлю и даже не замечу этого",
    "мой хуй сияет ярче солнца и ты просто ослепнешь когда я его достану из штанов",
    "от моего хуя идет сила такая что ты просто рассыплешься в прах и тебя ветром развеет нахуй",
]

used_templates = []
template_pool = INSULT_TEMPLATES.copy()

def generate_insult():
    global used_templates, template_pool
    if not template_pool:
        template_pool = INSULT_TEMPLATES.copy()
        used_templates = []
    insult = random.choice(template_pool)
    template_pool.remove(insult)
    used_templates.append(insult)
    return insult

def generate_break_insult():
    insult = generate_insult()
    insult = re.sub(r'[.,!?;:()"\']', '', insult)
    words = insult.split()
    banned = settings.get('banned_words', [])
    words = [w for w in words if w not in banned]
    if not words:
        words = ['ты', 'хуесос', 'блять']
    return words

stop_spam = False
spam_thread = None
message_count = 0
is_paused = False
total_messages_sent = 0
start_time = None
app_instance = None
spam_speed = 0.035
settings = {}

def spam_words():
    global stop_spam, message_count, is_paused, spam_speed, total_messages_sent, start_time
    stop_spam = False
    message_count = 0
    total_messages_sent = 0
    start_time = time.time()
    while not stop_spam:
        if is_paused:
            time.sleep(0.1)
            continue
        words = generate_break_insult()
        for word in words:
            if stop_spam:
                return
            if is_paused:
                break
            try:
                keyboard.write(word)
                time.sleep(spam_speed)
                keyboard.press_and_release('enter')
                time.sleep(settings.get('pause_between_messages', 0.01))
                message_count += 1
                total_messages_sent += 1
                if app_instance:
                    app_instance.update_counters()
            except:
                pass

def start_spam():
    global stop_spam, spam_thread
    if spam_thread and spam_thread.is_alive():
        return
    stop_spam = False
    spam_thread = threading.Thread(target=spam_words)
    spam_thread.daemon = True
    spam_thread.start()
    if app_instance:
        app_instance.update_ui_state()

def stop_spamming():
    global stop_spam
    stop_spam = True
    if app_instance:
        app_instance.update_ui_state()

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if app_instance:
        app_instance.update_ui_state()
    return is_paused

class GlowButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(relief=tk.FLAT, borderwidth=0, font=("Segoe UI", 10, "bold"), cursor="hand2")
        self.default_bg = self['bg']
        self.default_fg = self['fg']
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
    
    def on_enter(self, e):
        self.config(bg=self['bg'], fg=self['fg'])
    
    def on_leave(self, e):
        self.config(bg=self.default_bg, fg=self.default_fg)
    
    def on_click(self, e):
        self.config(relief=tk.SUNKEN)
        self.after(100, lambda: self.config(relief=tk.FLAT))

# ============================================================
# ОКНО АКТИВАЦИИ
# ============================================================

class ActivationWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"🔐 АКТИВАЦИЯ | {APP_NAME}")
        self.window.geometry("600x580")
        self.window.configure(bg=COLORS['bg'])
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", sys.exit)
        
        self.window.update_idletasks()
        width = 600
        height = 580
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        shadow = tk.Frame(self.window, bg=COLORS['shadow'], width=580, height=560)
        shadow.place(x=10, y=10)
        
        main_frame = tk.Frame(self.window, bg=COLORS['bg2'], width=580, height=560)
        main_frame.place(x=10, y=10)
        
        grad = tk.Frame(main_frame, bg=COLORS['gradient_start'], height=4)
        grad.pack(fill=tk.X, padx=0, pady=0)
        
        header = tk.Frame(main_frame, bg=COLORS['bg2'])
        header.pack(fill=tk.X, padx=30, pady=(20,5))
        
        tk.Label(header, text=f"🔥 {APP_NAME}", font=("Segoe UI", 22, "bold"), bg=COLORS['bg2'], fg=COLORS['gold']).pack()
        tk.Label(header, text="🔐 АКТИВАЦИЯ ПРОГРАММЫ", font=("Segoe UI", 12), bg=COLORS['bg2'], fg=COLORS['text2']).pack()
        
        info_frame = tk.Frame(main_frame, bg=COLORS['bg3'])
        info_frame.pack(pady=10, padx=30, fill=tk.X)
        info_frame.config(height=80)
        info_frame.pack_propagate(False)
        
        info_inner = tk.Frame(info_frame, bg=COLORS['bg3'])
        info_inner.pack(fill=tk.BOTH, padx=15, pady=10)
        
        tk.Label(info_inner, text=f"💻 Компьютер: {ComputerID.get_username()}", bg=COLORS['bg3'], fg=COLORS['text'], font=("Segoe UI", 11)).pack(anchor='w')
        tk.Label(info_inner, text=f"🆔 HWID: {ComputerID.get_full_hwid()[:24]}...", bg=COLORS['bg3'], fg=COLORS['text2'], font=("Segoe UI", 9)).pack(anchor='w')
        
        center_frame = tk.Frame(main_frame, bg=COLORS['bg2'])
        center_frame.pack(pady=15, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(center_frame, text="⚡ КУПИ ДОСТУП ⚡", font=("Segoe UI", 20, "bold"), bg=COLORS['bg2'], fg=COLORS['neon_orange']).pack()
        tk.Label(center_frame, text="У ВЛАДЕЛЬЦА", font=("Segoe UI", 12), bg=COLORS['bg2'], fg=COLORS['text']).pack()
        
        contact_frame = tk.Frame(center_frame, bg=COLORS['bg4'])
        contact_frame.pack(pady=8, padx=20, fill=tk.X)
        contact_frame.config(height=50)
        contact_frame.pack_propagate(False)
        
        contact_inner = tk.Frame(contact_frame, bg=COLORS['bg4'])
        contact_inner.pack(fill=tk.BOTH, padx=10, pady=5)
        
        tk.Label(contact_inner, text="🔥 @flidges 🔥", font=("Segoe UI", 16, "bold"), bg=COLORS['bg4'], fg=COLORS['gold']).pack(side=tk.LEFT)
        tk.Label(contact_inner, text="📩 Telegram", font=("Segoe UI", 10), bg=COLORS['bg4'], fg=COLORS['neon_blue']).pack(side=tk.RIGHT)
        
        tk.Label(center_frame, text=PRICE_TEXT, font=("Segoe UI", 12, "bold"), bg=COLORS['bg2'], fg=COLORS['neon']).pack(pady=5)
        
        sep = tk.Frame(center_frame, bg=COLORS['text3'], height=1, width=300)
        sep.pack(pady=10)
        
        key_frame = tk.Frame(center_frame, bg=COLORS['bg2'])
        key_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(key_frame, text="Или введите ключ активации:", bg=COLORS['bg2'], fg=COLORS['text2'], font=("Segoe UI", 10)).pack(anchor='w')
        
        entry_frame = tk.Frame(key_frame, bg=COLORS['bg2'])
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.key_entry = tk.Entry(entry_frame, bg=COLORS['bg3'], fg=COLORS['neon'], font=("Segoe UI", 14), relief=tk.FLAT, borderwidth=2, insertbackground=COLORS['text'])
        self.key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
        self.key_entry.bind('<Return>', lambda e: self.activate())
        
        self.activate_btn = tk.Button(entry_frame, text="✅ АКТИВИРОВАТЬ", command=self.activate, bg=COLORS['gradient_start'], fg='white', font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=15, pady=8)
        self.activate_btn.pack(side=tk.RIGHT)
        
        self.status_frame = tk.Frame(center_frame, bg=COLORS['bg2'], height=50)
        self.status_frame.pack(fill=tk.X, pady=5)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame, text="", bg=COLORS['bg2'], fg=COLORS['danger'], font=("Segoe UI", 11, "bold"))
        self.status_label.pack(fill=tk.BOTH, expand=True)
        
        footer = tk.Frame(main_frame, bg=COLORS['bg2'])
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Label(footer, text=f"© 2026 {DEVELOPER} | Версия {VERSION}", bg=COLORS['bg2'], fg=COLORS['text3'], font=("Segoe UI", 8)).pack()
        
        self.window.mainloop()
    
    def activate(self):
        key = self.key_entry.get().strip()
        if not key:
            self.status_label.config(text="❌ ВВЕДИТЕ КЛЮЧ!", fg=COLORS['danger'])
            return
        
        success, msg = db.activate_key(key)
        if success:
            self.status_label.config(text="✅ " + msg, fg=COLORS['success'])
            self.activate_btn.config(bg=COLORS['success'], text="✅ АКТИВИРОВАНО!")
            self.window.after(1500, self.close_and_start)
        else:
            self.status_label.config(text="❌ " + msg, fg=COLORS['danger'])
    
    def close_and_start(self):
        self.window.destroy()
        start_program()

# ============================================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# ============================================================

def start_program():
    hide_console()
    root = tk.Tk()
    root.title(f"🔥 {APP_NAME} | {DEVELOPER}")
    root.geometry("800x650")
    root.configure(bg=COLORS['bg'])
    root.minsize(700, 550)
    root.resizable(True, True)
    
    root.update_idletasks()
    width = 800
    height = 650
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    app = InsultApp(root)
    root.mainloop()

class InsultApp:
    def __init__(self, root):
        global app_instance
        app_instance = self
        
        self.root = root
        self.root.title(f"🔥 {APP_NAME} | {DEVELOPER}")
        self.root.geometry("800x650")
        self.root.configure(bg=COLORS['bg'])
        self.root.minsize(700, 550)
        self.root.resizable(True, True)
        
        # Проверяем админа
        hwid = ComputerID.get_full_hwid()
        self.is_admin = False
        user = db.cursor.execute('SELECT is_admin, is_owner FROM users WHERE hwid = ?', (CryptoEngine.encrypt(hwid),)).fetchone()
        if user and (user[0] == 1 or user[1] == 1):
            self.is_admin = True
        
        self.admin_panel = AdminPanel(self.root, self.is_admin)
        self.fullscreen = False
        
        self.create_widgets()
        self.setup_hotkeys()
        self.update_stats()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title_frame = tk.Frame(main_frame, bg=COLORS['bg2'], height=90)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_inner = tk.Frame(title_frame, bg=COLORS['bg2'])
        title_inner.pack(fill=tk.BOTH, padx=20, pady=10)
        tk.Label(title_inner, text=f"🔥 {APP_NAME}", font=("Segoe UI", 28, "bold"), bg=COLORS['bg2'], fg=COLORS['gold']).pack()
        tk.Label(title_inner, text=CREATOR_TEXT, font=("Segoe UI", 11), bg=COLORS['bg2'], fg=COLORS['neon_orange']).pack()
        
        top_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        top_frame.pack(fill=tk.X, padx=0, pady=5)
        
        self.admin_btn = GlowButton(top_frame, text="⚙️ АДМИН-ПАНЕЛЬ (F6)", command=self.toggle_admin, bg=COLORS['accent'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), padx=14, pady=5)
        self.admin_btn.pack(side=tk.LEFT)
        
        self.fs_btn = GlowButton(top_frame, text="⛶ ПОЛНЫЙ ЭКРАН (F11)", command=self.toggle_fullscreen, bg=COLORS['bg4'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), padx=14, pady=5)
        self.fs_btn.pack(side=tk.RIGHT)
        
        self.logout_btn = GlowButton(top_frame, text="🚪 ВЫЙТИ ИЗ АККАУНТА", command=self.logout, bg=COLORS['danger'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), padx=14, pady=5)
        self.logout_btn.pack(side=tk.RIGHT, padx=5)
        
        stats_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        stats_frame.pack(pady=5)
        self.status_label = tk.Label(stats_frame, text="⏸️ Ожидание...", bg=COLORS['bg'], fg=COLORS['warning'], font=("Segoe UI", 13, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.count_label = tk.Label(stats_frame, text="📨 0", bg=COLORS['bg'], fg=COLORS['neon'], font=("Segoe UI", 13, "bold"))
        self.count_label.pack(side=tk.LEFT, padx=10)
        
        self.preview = scrolledtext.ScrolledText(main_frame, height=9, bg=COLORS['bg3'], fg=COLORS['text'], insertbackground='white', font=("Segoe UI", 10), relief=tk.FLAT, borderwidth=2, padx=15, pady=15)
        self.preview.pack(padx=0, pady=8, fill=tk.BOTH, expand=True)
        self.preview.insert("1.0", f"""🔥 {APP_NAME}

╔══════════════════════════════════════════════════════╗
║  🎯 F3 → СТАРТ    🛑 F4 → СТОП    ⏸️ F5 → ПАУЗА   ║
║  ⚙️ F6 → АДМИН-ПАНЕЛЬ    ⛶ F11 → ПОЛНЫЙ ЭКРАН    ║
║  ❌ F9 → ВЫХОД                                     ║
╚══════════════════════════════════════════════════════╝

✅ Каждое сообщение уникально
✅ Длинные связные предложения
✅ 60+ шаблонов
✅ Работает даже при свёрнутом окне
✅ Автовход по ключу
✅ {CREATOR_TEXT}
✅ {LOVE_TEXT}""")
        self.preview.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        btn_frame.pack(pady=8)
        self.start_btn = GlowButton(btn_frame, text="🤖 СТАРТ (F3)", command=self.start_spam, bg=COLORS['success'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), width=16, padx=5, pady=8)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = GlowButton(btn_frame, text="🛑 СТОП (F4)", command=self.stop_spam, bg=COLORS['danger'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), width=16, padx=5, pady=8)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.pause_btn = GlowButton(btn_frame, text="⏸️ ПАУЗА (F5)", command=self.toggle_pause, bg=COLORS['accent'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), width=16, padx=5, pady=8)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        bottom_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        bottom_frame.pack(pady=5)
        tk.Label(bottom_frame, text="F3-СТАРТ | F4-СТОП | F5-ПАУЗА | F6-АДМИН | F9-ВЫХОД | F11-ПОЛНЫЙ ЭКРАН", bg=COLORS['bg'], fg=COLORS['text2'], font=("Segoe UI", 9)).pack()
        tk.Label(bottom_frame, text=LOVE_TEXT, bg=COLORS['bg'], fg=COLORS['pink'], font=("Segoe UI", 10, "bold")).pack()
    
    def logout(self):
        if messagebox.askyesno("Выход из аккаунта", "Вы уверены, что хотите выйти из аккаунта?\nКлюч будет удалён, и вам нужно будет ввести его заново."):
            db.logout()
            self.root.destroy()
            show_activation()
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        if self.fullscreen:
            self.fs_btn.config(text="⛶ ОКОННЫЙ РЕЖИМ (F11)", bg=COLORS['warning'])
        else:
            self.fs_btn.config(text="⛶ ПОЛНЫЙ ЭКРАН (F11)", bg=COLORS['bg4'])
    
    def setup_hotkeys(self):
        try:
            keyboard.add_hotkey('f3', self.start_spam)
            keyboard.add_hotkey('f4', self.stop_spam)
            keyboard.add_hotkey('f5', self.toggle_pause)
            keyboard.add_hotkey('f6', self.toggle_admin)
            keyboard.add_hotkey('f9', self.exit_app)
            keyboard.add_hotkey('f11', self.toggle_fullscreen)
        except:
            pass
    
    def toggle_admin(self):
        self.admin_panel.toggle()
    
    def update_counters(self):
        try:
            self.count_label.config(text=f"📨 {message_count}")
        except:
            pass
    
    def update_ui_state(self):
        try:
            if is_paused:
                self.status_label.config(text="⏸️ ПАУЗА", fg=COLORS['warning'])
                self.pause_btn.config(text="▶️ ВОЗОБНОВИТЬ (F5)", bg=COLORS['warning'])
            elif not stop_spam and spam_thread and spam_thread.is_alive():
                self.status_label.config(text="🧠 ГЕНЕРАЦИЯ", fg=COLORS['success'])
                self.start_btn.config(bg=COLORS['bg4'], text="🧠 РАБОТАЕТ...")
                self.pause_btn.config(text="⏸️ ПАУЗА (F5)", bg=COLORS['accent'])
            else:
                self.status_label.config(text="⏸️ Остановлено", fg=COLORS['text2'])
                self.start_btn.config(bg=COLORS['success'], text="🤖 СТАРТ (F3)")
                self.pause_btn.config(text="⏸️ ПАУЗА (F5)", bg=COLORS['accent'])
        except:
            pass
    
    def update_stats(self):
        self.update_ui_state()
        self.count_label.config(text=f"📨 {message_count}")
        self.root.after(500, self.update_stats)
    
    def start_spam(self):
        start_spam()
        self.update_ui_state()
    
    def stop_spam(self):
        stop_spamming()
        self.update_ui_state()
    
    def toggle_pause(self):
        toggle_pause()
        self.update_ui_state()
    
    def exit_app(self):
        stop_spamming()
        self.root.quit()
        self.root.destroy()
        sys.exit()

class AdminPanel:
    def __init__(self, parent, is_admin=False):
        self.parent = parent
        self.is_admin = is_admin
        self.window = None
        self.is_open = False
        self._speed_update_timer = None
        self.create_panel()
    
    def create_panel(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"✨ АДМИН-ПАНЕЛЬ | {APP_NAME}")
        self.window.geometry("900x700")
        self.window.configure(bg=COLORS['bg'])
        self.window.minsize(800, 600)
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
        self.window.bind('<Escape>', lambda e: self.hide())
        self.window.withdraw()
        
        title_frame = tk.Frame(self.window, bg=COLORS['bg2'], height=70)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_inner = tk.Frame(title_frame, bg=COLORS['bg2'])
        title_inner.pack(fill=tk.BOTH, padx=30, pady=10)
        tk.Label(title_inner, text="✨ АДМИН-ПАНЕЛЬ", font=("Segoe UI", 24, "bold"), bg=COLORS['bg2'], fg=COLORS['gold']).pack(side=tk.LEFT)
        tk.Label(title_inner, text=f"⭐ {DEVELOPER}", font=("Segoe UI", 12), bg=COLORS['bg2'], fg=COLORS['neon_orange']).pack(side=tk.RIGHT)
        
        sep = tk.Frame(self.window, bg=COLORS['neon'], height=3)
        sep.pack(fill=tk.X, padx=0)
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=COLORS['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=COLORS['bg2'], foreground=COLORS['text'], padding=[20, 8], font=("Segoe UI", 10, "bold"))
        style.map('TNotebook.Tab', background=[('selected', COLORS['accent'])])
        
        # Для всех
        self.tab_main = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.notebook.add(self.tab_main, text="📊 Главная")
        self.create_main_tab()
        
        self.tab_about = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.notebook.add(self.tab_about, text="💜 О нас")
        self.create_about_tab()
        
        # Только для админов
        if self.is_admin:
            self.tab_users = tk.Frame(self.notebook, bg=COLORS['bg'])
            self.notebook.add(self.tab_users, text="👥 Пользователи")
            self.create_users_tab()
            
            self.tab_keys = tk.Frame(self.notebook, bg=COLORS['bg'])
            self.notebook.add(self.tab_keys, text="🔑 Ключи")
            self.create_keys_tab()
            
            self.tab_stats = tk.Frame(self.notebook, bg=COLORS['bg'])
            self.notebook.add(self.tab_stats, text="📈 Статистика")
            self.create_stats_tab()
        
        self.update_stats()
    
    def create_main_tab(self):
        tab = self.tab_main
        speed_frame = tk.Frame(tab, bg=COLORS['bg'])
        speed_frame.pack(pady=10, padx=20, fill=tk.X)
        tk.Label(speed_frame, text="🚀 Скорость отправки", font=("Segoe UI", 14, "bold"), bg=COLORS['bg'], fg=COLORS['accent2']).pack(anchor='w')
        
        speed_control = tk.Frame(speed_frame, bg=COLORS['bg'])
        speed_control.pack(fill=tk.X, pady=5)
        self.speed_slider = tk.Scale(speed_control, from_=0.001, to=0.45, resolution=0.001, orient=tk.HORIZONTAL, length=480,
                                      bg=COLORS['bg'], fg=COLORS['text'], troughcolor=COLORS['bg3'], sliderlength=22, highlightthickness=0)
        self.speed_slider.set(spam_speed)
        self.speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.speed_label = tk.Label(speed_control, text=f"{spam_speed:.3f}с", bg=COLORS['bg'], fg=COLORS['gold'], font=("Segoe UI", 18, "bold"), width=8)
        self.speed_label.pack(side=tk.LEFT, padx=10)
        
        def update_speed(val):
            val = float(val)
            self.speed_label.config(text=f"{val:.3f}с")
            if self._speed_update_timer:
                self.window.after_cancel(self._speed_update_timer)
            def apply_speed():
                global spam_speed
                spam_speed = val
                settings['spam_speed'] = val
                save_settings(settings)
            self._speed_update_timer = self.window.after(300, apply_speed)
        
        self.speed_slider.config(command=update_speed)
        
        preset_frame = tk.Frame(tab, bg=COLORS['bg'])
        preset_frame.pack(pady=5, padx=20, fill=tk.X)
        tk.Label(preset_frame, text="⚡ Быстрые пресеты", font=("Segoe UI", 11, "bold"), bg=COLORS['bg'], fg=COLORS['text2']).pack(anchor='w')
        preset_btns = tk.Frame(preset_frame, bg=COLORS['bg'])
        preset_btns.pack(fill=tk.X, pady=5)
        for name, speed in [("🐢 0.1с", 0.1), ("🚶 0.05с", 0.05), ("🏃 0.02с", 0.02), ("🚀 0.005с", 0.005), ("🔥 0.001с", 0.001)]:
            btn = GlowButton(preset_btns, text=name, command=lambda s=speed: self.apply_preset(s), bg=COLORS['bg4'], fg=COLORS['text'], font=("Segoe UI", 9, "bold"), padx=14, pady=6)
            btn.pack(side=tk.LEFT, padx=3)
        
        info_frame = tk.Frame(tab, bg=COLORS['bg'])
        info_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
        tk.Label(info_frame, text="📊 Живая статистика", font=("Segoe UI", 14, "bold"), bg=COLORS['bg'], fg=COLORS['neon']).pack(anchor='w')
        self.info_text = tk.Text(info_frame, height=9, bg=COLORS['bg2'], fg=COLORS['text'], font=("Consolas", 10), relief=tk.FLAT, borderwidth=2, padx=15, pady=12)
        self.info_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.info_text.insert("1.0", "⏳ Ожидание запуска...")
        self.info_text.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(tab, bg=COLORS['bg'])
        btn_frame.pack(pady=10)
        for text, cmd in [("🔄 Обновить", self.update_info), ("🧹 Сбросить счётчик", self.reset_counters)]:
            btn = GlowButton(btn_frame, text=text, command=cmd, bg=COLORS['bg3'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), padx=18, pady=6)
            btn.pack(side=tk.LEFT, padx=5)
    
    def create_users_tab(self):
        if not self.is_admin:
            return
        tab = self.tab_users
        control_frame = tk.Frame(tab, bg=COLORS['bg'])
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        tk.Label(control_frame, text="👥 Управление пользователями", font=("Segoe UI", 14, "bold"), bg=COLORS['bg'], fg=COLORS['gold']).pack(anchor='w')
        
        input_frame = tk.Frame(control_frame, bg=COLORS['bg'])
        input_frame.pack(fill=tk.X, pady=5)
        self.user_entry = tk.Entry(input_frame, bg=COLORS['bg3'], fg=COLORS['text'], font=("Segoe UI", 11), relief=tk.FLAT, borderwidth=2, width=20)
        self.user_entry.pack(side=tk.LEFT, padx=5)
        self.user_entry.insert(0, "Имя пользователя")
        self.user_entry.bind('<FocusIn>', lambda e: self.user_entry.delete(0, tk.END))
        
        months_var = tk.StringVar(value="1")
        months_menu = ttk.Combobox(input_frame, textvariable=months_var, values=["1", "3", "6", "12", "24"], width=5, state="readonly")
        months_menu.pack(side=tk.LEFT, padx=5)
        tk.Label(input_frame, text="мес.", bg=COLORS['bg'], fg=COLORS['text2']).pack(side=tk.LEFT)
        
        tk.Button(input_frame, text="✅ ВЫДАТЬ", command=lambda: self.give_access(months_var.get()), bg=COLORS['success'], fg='white', font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="🚫 ЗАБРАТЬ", command=self.revoke_access, bg=COLORS['danger'], fg='white', font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="🔄 ПРОДЛИТЬ", command=lambda: self.extend_access(months_var.get()), bg=COLORS['accent'], fg='white', font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        list_frame = tk.Frame(tab, bg=COLORS['bg'])
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        columns = ("Имя", "Статус", "Бан", "До", "Ключ", "HWID")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column("HWID", width=120)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(tab, text="💡 Двойной клик по пользователю → бан/разбан", bg=COLORS['bg'], fg=COLORS['text3'], font=("Segoe UI", 9)).pack(pady=5)
        self.refresh_users()
    
    def create_keys_tab(self):
        if not self.is_admin:
            return
        tab = self.tab_keys
        control_frame = tk.Frame(tab, bg=COLORS['bg'])
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        tk.Label(control_frame, text="🔑 Управление ключами", font=("Segoe UI", 14, "bold"), bg=COLORS['bg'], fg=COLORS['gold']).pack(anchor='w')
        
        add_frame = tk.Frame(control_frame, bg=COLORS['bg'])
        add_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(add_frame, text="Ключ:", bg=COLORS['bg'], fg=COLORS['text'], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.key_entry = tk.Entry(add_frame, bg=COLORS['bg3'], fg=COLORS['text'], font=("Segoe UI", 11), relief=tk.FLAT, borderwidth=2, width=20)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.insert(0, "Введите ключ")
        self.key_entry.bind('<FocusIn>', lambda e: self.key_entry.delete(0, tk.END) if self.key_entry.get() == "Введите ключ" else None)
        
        tk.Label(add_frame, text="мес:", bg=COLORS['bg'], fg=COLORS['text'], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.key_months = ttk.Combobox(add_frame, values=["1", "3", "6", "12", "24"], width=5, state="readonly")
        self.key_months.set("1")
        self.key_months.pack(side=tk.LEFT, padx=5)
        
        tk.Button(add_frame, text="➕ ДОБАВИТЬ КЛЮЧ", command=self.add_key, bg=COLORS['success'], fg='white', font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(add_frame, text="🎲 СГЕНЕРИРОВАТЬ", command=self.generate_key, bg=COLORS['accent'], fg='white', font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        list_frame = tk.Frame(tab, bg=COLORS['bg'])
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        columns = ("Ключ", "Создан", "До", "Использован", "Кем", "HWID")
        self.keys_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.keys_tree.heading(col, text=col)
            self.keys_tree.column(col, width=100)
        self.keys_tree.column("HWID", width=100)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.keys_tree.yview)
        self.keys_tree.configure(yscrollcommand=scrollbar.set)
        self.keys_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        del_frame = tk.Frame(tab, bg=COLORS['bg'])
        del_frame.pack(pady=5, padx=20, fill=tk.X)
        tk.Button(del_frame, text="🗑 УДАЛИТЬ ВЫБРАННЫЙ КЛЮЧ", command=self.delete_key, bg=COLORS['danger'], fg='white', font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2", padx=10, pady=5).pack(side=tk.LEFT)
        tk.Label(del_frame, text="💡 Выберите ключ в списке и нажмите УДАЛИТЬ", bg=COLORS['bg'], fg=COLORS['text3'], font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10)
        
        self.refresh_keys()
    
    def create_stats_tab(self):
        if not self.is_admin:
            return
        tab = self.tab_stats
        stats_frame = tk.Frame(tab, bg=COLORS['bg'])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(stats_frame, text="📈 ДЕТАЛЬНАЯ СТАТИСТИКА", font=("Segoe UI", 18, "bold"), bg=COLORS['bg'], fg=COLORS['gold']).pack(pady=10)
        self.stats_text = tk.Text(stats_frame, height=15, bg=COLORS['bg2'], fg=COLORS['text'], font=("Consolas", 11), relief=tk.FLAT, borderwidth=2, padx=20, pady=15)
        self.stats_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.stats_text.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(stats_frame, bg=COLORS['bg'])
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="🔄 ОБНОВИТЬ", command=self.update_stats_display, bg=COLORS['accent'], fg='white', font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=8).pack()
        self.update_stats_display()
    
    def create_about_tab(self):
        tab = self.tab_about
        about_frame = tk.Frame(tab, bg=COLORS['bg'])
        about_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        tk.Label(about_frame, text="🔥", font=("Segoe UI", 80), bg=COLORS['bg']).pack(pady=5)
        tk.Label(about_frame, text=APP_NAME, font=("Segoe UI", 28, "bold"), bg=COLORS['bg'], fg=COLORS['gold']).pack(pady=5)
        tk.Label(about_frame, text=f"✨ Версия {VERSION} ✨", font=("Segoe UI", 14), bg=COLORS['bg'], fg=COLORS['text2']).pack(pady=5)
        
        sep = tk.Frame(about_frame, bg=COLORS['neon'], height=2, width=350)
        sep.pack(pady=15)
        
        tk.Label(about_frame, text="👨‍💻 РАЗРАБОТЧИК", font=("Segoe UI", 13, "bold"), bg=COLORS['bg'], fg=COLORS['text']).pack()
        tk.Label(about_frame, text=DEVELOPER, font=("Segoe UI", 22, "bold"), bg=COLORS['bg'], fg=COLORS['pink']).pack(pady=3)
        tk.Label(about_frame, text=CREATOR_TEXT, font=("Segoe UI", 13), bg=COLORS['bg'], fg=COLORS['gold']).pack(pady=5)
        tk.Label(about_frame, text=PRICE_TEXT, font=("Segoe UI", 12, "bold"), bg=COLORS['bg'], fg=COLORS['neon']).pack(pady=5)
        
        sep2 = tk.Frame(about_frame, bg=COLORS['accent'], height=1, width=250)
        sep2.pack(pady=10)
        
        for feat in ["🔥 Каждое сообщение уникально", "💎 Длинные связные предложения", "📚 60+ шаблонов", "⚡ Работает при свёрнутом окне", "🔒 Защита HWID", "💾 Автосохранение ключа"]:
            tk.Label(about_frame, text=feat, font=("Segoe UI", 11), bg=COLORS['bg'], fg=COLORS['neon']).pack(pady=2)
        
        sep3 = tk.Frame(about_frame, bg=COLORS['accent'], height=1, width=200)
        sep3.pack(pady=10)
        tk.Label(about_frame, text=LOVE_TEXT, font=("Segoe UI", 14, "bold"), bg=COLORS['bg'], fg=COLORS['pink']).pack(pady=5)
        tk.Label(about_frame, text="© 2026 Все права защищены 🚀", font=("Segoe UI", 9), bg=COLORS['bg'], fg=COLORS['text3']).pack(pady=5)
    
    def apply_preset(self, speed):
        global spam_speed
        spam_speed = speed
        self.speed_slider.set(speed)
        self.speed_label.config(text=f"{speed:.3f}с")
        settings['spam_speed'] = speed
        save_settings(settings)
    
    def give_access(self, months):
        if not self.is_admin:
            messagebox.showwarning("Доступ запрещен", "Только для администраторов!")
            return
        username = self.user_entry.get().strip()
        if not username or username == "Имя пользователя":
            messagebox.showerror("Ошибка", "Введите имя пользователя!")
            return
        success, msg = db.give_access(username, int(months))
        if success:
            messagebox.showinfo("Успех", msg)
            self.refresh_users()
        else:
            messagebox.showerror("Ошибка", msg)
    
    def revoke_access(self):
        if not self.is_admin:
            messagebox.showwarning("Доступ запрещен", "Только для администраторов!")
            return
        username = self.user_entry.get().strip()
        if not username or username == "Имя пользователя":
            messagebox.showerror("Ошибка", "Введите имя пользователя!")
            return
        if messagebox.askyesno("Подтверждение", f"Забрать доступ у {username}?"):
            db.revoke_access(username)
            messagebox.showinfo("Успех", f"Доступ у {username} забран!")
            self.refresh_users()
    
    def extend_access(self, months):
        if not self.is_admin:
            messagebox.showwarning("Доступ запрещен", "Только для администраторов!")
            return
        username = self.user_entry.get().strip()
        if not username or username == "Имя пользователя":
            messagebox.showerror("Ошибка", "Введите имя пользователя!")
            return
        success, msg = db.extend_access(username, int(months))
        if success:
            messagebox.showinfo("Успех", msg)
            self.refresh_users()
        else:
            messagebox.showerror("Ошибка", msg)
    
    def add_key(self):
        if not self.is_admin:
            messagebox.showwarning("Доступ запрещен", "Только для администраторов!")
            return
        key = self.key_entry.get().strip().upper()
        months = int(self.key_months.get())
        if not key or key == "ВВЕДИТЕ КЛЮЧ":
            messagebox.showerror("Ошибка", "Введите ключ!")
            return
        success, result = db.generate_key(months, key)
        if success:
            messagebox.showinfo("Успех", f"🔑 Ключ {key} добавлен на {months} месяцев!")
            self.refresh_keys()
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, "Введите ключ")
        else:
            messagebox.showerror("Ошибка", "Такой ключ уже существует!")
    
    def generate_key(self):
        if not self.is_admin:
            messagebox.showwarning("Доступ запрещен", "Только для администраторов!")
            return
        months = int(self.key_months.get())
        success, key = db.generate_key(months)
        if success:
            messagebox.showinfo("Ключ сгенерирован", f"🔑 Ключ: {key}\n📅 Действует: {months} месяцев\n📩 Отправь его покупателю!\n⚠️ Ключ привяжется к первому компьютеру!")
            self.refresh_keys()
    
    def delete_key(self):
        if not self.is_admin:
            messagebox.showwarning("Доступ запрещен", "Только для администраторов!")
            return
        selection = self.keys_tree.selection()
        if not selection:
            messagebox.showerror("Ошибка", "Выберите ключ для удаления!")
            return
        item = selection[0]
        values = self.keys_tree.item(item, 'values')
        key_text = values[0]
        if messagebox.askyesno("Подтверждение", f"Удалить ключ {key_text}?"):
            db.delete_key(key_text)
            messagebox.showinfo("Успех", f"Ключ {key_text} удален!")
            self.refresh_keys()
    
    def refresh_users(self):
        if not self.is_admin:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        users = db.get_all_users()
        for user in users:
            username, is_owner, is_admin, is_banned, expires_at, hwid, saved_key = user
            if expires_at:
                try:
                    expiry = datetime.fromisoformat(expires_at).strftime('%d.%m.%Y')
                except:
                    expiry = "Ошибка"
            else:
                expiry = "-"
            status_text = "👑" if is_owner else ("⭐" if is_admin else "👤")
            banned_text = "🚫" if is_banned else "✅"
            hwid_short = hwid[:12] + "..." if hwid else "-"
            key_short = saved_key[:8] + "..." if saved_key else "-"
            self.tree.insert("", tk.END, values=(username, status_text, banned_text, expiry, key_short, hwid_short), tags=(username, is_banned))
        self.tree.bind('<Double-Button-1>', self.on_user_click)
    
    def on_user_click(self, event):
        if not self.is_admin:
            return
        selection = self.tree.selection()
        if not selection:
            return
        item = selection[0]
        values = self.tree.item(item, 'values')
        username = values[0]
        is_banned = values[2] == "🚫"
        is_owner = values[1] == "👑"
        if is_owner:
            messagebox.showinfo("Инфо", "Нельзя изменять овнера!")
            return
        if is_banned:
            if messagebox.askyesno("Восстановить", f"Разбанить {username}?"):
                db.restore_access(username)
                messagebox.showinfo("Успех", f"{username} разбанен!")
                self.refresh_users()
        else:
            if messagebox.askyesno("Забанить", f"Забанить {username}?"):
                db.revoke_access(username)
                messagebox.showinfo("Успех", f"{username} забанен!")
                self.refresh_users()
    
    def refresh_keys(self):
        if not self.is_admin:
            return
        for item in self.keys_tree.get_children():
            self.keys_tree.delete(item)
        keys = db.get_all_keys()
        for key in keys:
            key_text, created_at, expires_at, used_by, used_hwid, is_used, owner_hwid = key
            try:
                created = datetime.fromisoformat(created_at).strftime('%d.%m') if created_at else "-"
            except:
                created = "-"
            try:
                expires = datetime.fromisoformat(expires_at).strftime('%d.%m.%Y') if expires_at else "-"
            except:
                expires = "-"
            status = "✅" if is_used else "🔓"
            used_by_text = used_by if used_by else "-"
            used_hwid_short = used_hwid[:12] + "..." if used_hwid else "-"
            self.keys_tree.insert("", tk.END, values=(key_text, created, expires, status, used_by_text, used_hwid_short))
    
    def update_stats_display(self):
        if not self.is_admin:
            return
        users = db.get_all_users()
        keys = db.get_all_keys()
        text = f"""
╔══════════════════════════════════════════════════════════════╗
║                      📊 СТАТИСТИКА                          ║
╠══════════════════════════════════════════════════════════════╣
║  👥 Всего пользователей: {len(users):>4}                                     ║
║  👑 Овнеров:             {sum(1 for u in users if u[1]):>4}                                     ║
║  ⭐ Админов:             {sum(1 for u in users if u[2]):>4}                                     ║
║  🚫 Забаненных:          {sum(1 for u in users if u[3]):>4}                                     ║
║  ✅ Активных:            {sum(1 for u in users if not u[3]):>4}                                     ║
╠══════════════════════════════════════════════════════════════╣
║  🔑 Всего ключей:        {len(keys):>4}                                     ║
║  ✅ Использованных:      {sum(1 for k in keys if k[5]):>4}                                     ║
║  🔓 Свободных:           {len(keys) - sum(1 for k in keys if k[5]):>4}                                     ║
╚══════════════════════════════════════════════════════════════╝
"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", text)
        self.stats_text.config(state=tk.DISABLED)
    
    def update_info(self):
        global message_count, total_messages_sent, start_time
        uptime = "0с"
        if start_time:
            seconds = int(time.time() - start_time)
            minutes = seconds // 60
            seconds = seconds % 60
            hours = minutes // 60
            minutes = minutes % 60
            if hours > 0:
                uptime = f"{hours}ч {minutes}м {seconds}с"
            elif minutes > 0:
                uptime = f"{minutes}м {seconds}с"
            else:
                uptime = f"{seconds}с"
        status = "⏸️ Остановлено"
        if not stop_spam and spam_thread and spam_thread.is_alive():
            if is_paused:
                status = "⏸️ ПАУЗА"
            else:
                status = "🧠 АКТИВЕН"
        info = f"""
╔══════════════════════════════════════════════════════╗
║  📊 СТАТИСТИКА              Статус: {status:<10} ║
╠══════════════════════════════════════════════════════╣
║  📨 За сессию: {message_count:>6}                                  ║
║  📨 Всего:      {total_messages_sent:>6}                                  ║
║  ⏱ Время:      {uptime:>10}                              ║
║  🚀 Скорость:  {spam_speed:.3f}с                                   ║
║  📝 Шаблонов:  {len(INSULT_TEMPLATES):>6}                                  ║
║  🚫 Забанено:  {len(settings.get('banned_words', [])):>6}                                  ║
║  ⭐ Dev:       {DEVELOPER}                              ║
╚══════════════════════════════════════════════════════╝
        """
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", info)
        self.info_text.config(state=tk.DISABLED)
    
    def reset_counters(self):
        global message_count, total_messages_sent
        message_count = 0
        total_messages_sent = 0
        self.update_info()
        messagebox.showinfo("✅ Сброшено", "Счётчики обнулены!")
    
    def update_stats(self):
        self.update_info()
        self.window.after(2000, self.update_stats)
    
    def show(self):
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.is_open = True
            self.update_stats()
    
    def hide(self):
        if self.window:
            self.window.withdraw()
            self.is_open = False
    
    def toggle(self):
        if self.is_open:
            self.hide()
        else:
            self.show()

# ============================================================
# НАСТРОЙКИ
# ============================================================

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                encrypted_data = json.load(f)
                decrypted = {}
                for key, value in encrypted_data.items():
                    if isinstance(value, str):
                        try:
                            decrypted[key] = CryptoEngine.decrypt(value)
                        except:
                            decrypted[key] = value
                    else:
                        decrypted[key] = value
                return decrypted
        except:
            return default_settings.copy()
    return default_settings.copy()

def save_settings(settings_data):
    try:
        encrypted_data = {}
        for key, value in settings_data.items():
            if isinstance(value, (str, int, float, bool)):
                encrypted_data[key] = CryptoEngine.encrypt(str(value))
            else:
                encrypted_data[key] = value
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(encrypted_data, f, ensure_ascii=False, indent=2)
    except:
        pass

default_settings = {
    "spam_speed": 0.035,
    "pause_between_messages": 0.01,
    "banned_words": [],
    "max_words_per_message": 50,
    "min_words_per_message": 15
}

settings = load_settings()
spam_speed = float(settings.get('spam_speed', 0.035))

def show_activation():
    hide_console()
    ActivationWindow()

if __name__ == "__main__":
    hide_console()
    
    access, msg = db.check_access_auto()
    if access:
        start_program()
    else:
        access, msg = db.check_access()
        if access:
            start_program()
        else:
            show_activation()
