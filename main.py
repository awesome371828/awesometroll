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
# БАЗА ДАННЫХ
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
        
        encrypted_key = CryptoEngine.encrypt(key_upper)
        result = self.cursor.execute('''SELECT key_text, expires_at, is_used, used_hwid, owner_hwid 
            FROM license_keys WHERE key_text = ?''', (encrypted_key,)).fetchone()
        
        if not result:
            return False, "❌ НЕВЕРНЫЙ КЛЮЧ!"
        
        key_enc, expires_enc, is_used, used_hwid_enc, owner_hwid_enc = result
        expires_at = CryptoEngine.decrypt(expires_enc)
        used_hwid = CryptoEngine.decrypt(used_hwid_enc) if used_hwid_enc else None
        owner_hwid = CryptoEngine.decrypt(owner_hwid_enc) if owner_hwid_enc else None
        
        if owner_hwid and owner_hwid != hwid:
            return False, "❌ ЭТОТ КЛЮЧ НЕ ДЛЯ ТВОЕГО КОМПЬЮТЕРА!"
        
        if is_used and used_hwid and used_hwid != hwid:
            return False, "❌ КЛЮЧ УЖЕ АКТИВИРОВАН НА ДРУГОМ КОМПЬЮТЕРЕ!"
        
        if is_used and used_hwid == hwid:
            expiry = datetime.fromisoformat(expires_at)
            if datetime.now() > expiry:
                return False, f"❌ КЛЮЧ ИСТЕК {expiry.strftime('%d.%m.%Y')}!"
            return True, f"✅ ДОСТУП УЖЕ АКТИВИРОВАН ДО {expiry.strftime('%d.%m.%Y')}!"
        
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return False, f"❌ КЛЮЧ ИСТЕК {expiry.strftime('%d.%m.%Y')}!"
        
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
# ШАБЛОНЫ
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

# ============================================================
# АВТОСПАМ
# ============================================================

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
# ЗВЕЗДЫ НА ФОНЕ
# ============================================================

class StarBackground:
    def __init__(self, canvas, num_stars=100):
        self.canvas = canvas
        self.stars = []
        self.running = True
        
        for _ in range(num_stars):
            x = random.randint(0, canvas.winfo_reqwidth() or 800)
            y = random.randint(0, canvas.winfo_reqheight() or 600)
            size = random.randint(1, 3)
            speed = random.uniform(0.02, 0.08)
            brightness = random.randint(100, 255)
            self.stars.append({
                'x': x, 'y': y, 'size': size, 'speed': speed, 
                'brightness': brightness, 'phase': random.uniform(0, 6.28)
            })
    
    def update(self):
        if not self.running:
            return
        self.canvas.delete("star")
        for star in self.stars:
            star['phase'] += star['speed']
            star['x'] += random.uniform(-0.3, 0.3)
            star['y'] += random.uniform(-0.3, 0.3)
            
            width = self.canvas.winfo_reqwidth() or 800
            height = self.canvas.winfo_reqheight() or 600
            if star['x'] < 0: star['x'] = width
            if star['x'] > width: star['x'] = 0
            if star['y'] < 0: star['y'] = height
            if star['y'] > height: star['y'] = 0
            
            b = int(star['brightness'] * (0.5 + 0.5 * (star['phase'] % 1)))
            color = f"#{min(255, b):02x}{min(255, b//2):02x}{min(255, b):02x}"
            
            self.canvas.create_oval(
                star['x'] - star['size'], star['y'] - star['size'],
                star['x'] + star['size'], star['y'] + star['size'],
                fill=color, outline="", tags="star"
            )
        self.canvas.after(100, self.update)
    
    def stop(self):
        self.running = False

# ============================================================
# ОКНО АКТИВАЦИИ
# ============================================================

class ActivationWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"🔐 АКТИВАЦИЯ | {APP_NAME}")
        self.window.geometry("600x650")
        self.window.configure(bg=COLORS['bg'])
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", sys.exit)
        
        self.window.update_idletasks()
        width = 600
        height = 650
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.canvas = tk.Canvas(self.window, width=600, height=650, bg=COLORS['bg'], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.stars = StarBackground(self.canvas, 150)
        self.stars.update()
        
        shadow = tk.Frame(self.canvas, bg=COLORS['shadow'], width=580, height=600)
        shadow.place(x=10, y=25)
        
        main_frame = tk.Frame(self.canvas, bg=COLORS['bg2'], width=580, height=600)
        main_frame.place(x=10, y=25)
        
        grad = tk.Frame(main_frame, bg=COLORS['gradient_start'], height=4)
        grad.pack(fill=tk.X, padx=0, pady=0)
        
        header = tk.Frame(main_frame, bg=COLORS['bg2'])
        header.pack(fill=tk.X, padx=30, pady=(20,5))
        
        tk.Label(header, text=f"🔥 {APP_NAME}", font=("Segoe UI", 26, "bold"), bg=COLORS['bg2'], fg=COLORS['gold']).pack()
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
        
        tk.Label(contact_inner, text="🔥 @flidges
