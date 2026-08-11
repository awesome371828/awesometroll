import base64
import zlib
import random
import hashlib
import sys
import os
import time
import json
import sqlite3
import uuid
import subprocess
import platform
import threading
import re
import ctypes
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ============================================================
# ШИФРОВАНИЕ СТРОК
# ============================================================

class CryptoStrings:
    _cache = {}
    _salt = b'\x7f\x8e\x9a\x1b\x2c\x3d\x4e\x5f\x6a\x7b\x8c\x9d\xae\xbf\xc1\xd2'
    
    @classmethod
    def _get_key(cls, seed):
        if seed not in cls._cache:
            kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=cls._salt, iterations=500000)
            cls._cache[seed] = base64.urlsafe_b64encode(kdf.derive(str(seed).encode()))
        return cls._cache[seed]
    
    @classmethod
    def encode(cls, text, seed=None):
        if seed is None:
            seed = random.randint(100000, 999999)
        compressed = zlib.compress(text.encode('utf-8'), level=9)
        fernet = Fernet(cls._get_key(seed))
        encrypted = fernet.encrypt(compressed)
        b64 = base64.b64encode(encrypted).decode('ascii')
        chars = list(b64)
        for i in range(len(chars) - 1, 0, -1):
            if random.random() > 0.7:
                chars.insert(i, random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/='))
        obfuscated = ''.join(chars)
        checksum = hashlib.md5(f"{seed}:{b64}".encode()).hexdigest()[:8]
        return f"__{checksum}__{seed}__{obfuscated}"
    
    @classmethod
    def decode(cls, encoded):
        try:
            parts = encoded.split('__')
            if len(parts) < 4:
                return encoded
            checksum = parts[1]
            seed = int(parts[2])
            obfuscated = parts[3]
            b64 = ''
            for char in obfuscated:
                if char in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/=':
                    b64 += char
            if hashlib.md5(f"{seed}:{b64}".encode()).hexdigest()[:8] != checksum:
                return encoded
            encrypted = base64.b64decode(b64)
            fernet = Fernet(cls._get_key(seed))
            decrypted = fernet.decrypt(encrypted)
            return zlib.decompress(decrypted).decode('utf-8')
        except:
            return encoded

# ============================================================
# ЗАЩИЩЕННЫЕ ДАННЫЕ (МАСТЕР-КЛЮЧ ЗАШИФРОВАН)
# ============================================================

class SecureData:
    _data = None
    
    @classmethod
    def _get_data(cls):
        if cls._data is None:
            cls._data = {
                'dev': CryptoStrings.encode('@flidges'),
                'creator': CryptoStrings.encode('👁️ Создатель: awesome / tg @flidges 👀'),
                'version': CryptoStrings.encode('3.0'),
                'love': CryptoStrings.encode('❤️ Сделано с любовью и матом 💖'),
                'app': CryptoStrings.encode('AWESOMETROLLING'),
                'price': CryptoStrings.encode('😍 Цена - узнайте у @flidges'),
                'master': CryptoStrings.encode('awesminute'),
            }
        return cls._data
    
    @classmethod
    def get(cls, key):
        try:
            return CryptoStrings.decode(cls._get_data().get(key, ''))
        except:
            return ""

# ============================================================
# КОНСТАНТЫ
# ============================================================

DEVELOPER = SecureData.get('dev')
CREATOR_TEXT = SecureData.get('creator')
VERSION = SecureData.get('version')
LOVE_TEXT = SecureData.get('love')
APP_NAME = SecureData.get('app')
PRICE_TEXT = SecureData.get('price')
MASTER_KEY = SecureData.get('master')

# ============================================================
# ШИФРОВАНИЕ ДАННЫХ
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
            is_admin INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            created_at TEXT, expires_at TEXT, last_active TEXT,
            saved_key TEXT
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS license_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_text TEXT UNIQUE NOT NULL,
            created_at TEXT, expires_at TEXT,
            used_by TEXT, used_hwid TEXT, used_at TEXT,
            is_used INTEGER DEFAULT 0
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
        try:
            self.cursor.execute('INSERT INTO license_keys (key_text, created_at, expires_at, is_used) VALUES (?, ?, ?, 0)', 
                               (CryptoEngine.encrypt(key), CryptoEngine.encrypt(created_at), CryptoEngine.encrypt(expires_at)))
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
                self.cursor.execute('UPDATE users SET username = ?, is_admin = 1, is_banned = 0, expires_at = ?, saved_key = ? WHERE hwid = ?', 
                                   (encrypted_username, encrypted_expires, encrypted_key, encrypted_hwid))
            else:
                self.cursor.execute('INSERT INTO users (username, hwid, is_admin, created_at, expires_at, saved_key) VALUES (?, ?, 1, ?, ?, ?)',
                                   (encrypted_username, encrypted_hwid, CryptoEngine.encrypt(datetime.now().isoformat()), encrypted_expires, encrypted_key))
            self.conn.commit()
            if save:
                self.save_license(key_upper)
            return True, "👑 ДОБРО ПОЖАЛОВАТЬ, ВЛАДЕЛЕЦ!"
        
        encrypted_key = CryptoEngine.encrypt(key_upper)
        result = self.cursor.execute('SELECT key_text, expires_at, is_used, used_hwid FROM license_keys WHERE key_text = ?', 
                                     (encrypted_key,)).fetchone()
        if not result:
            return False, "❌ НЕВЕРНЫЙ КЛЮЧ!"
        
        key_enc, expires_enc, is_used, used_hwid_enc = result
        expires_at = CryptoEngine.decrypt(expires_enc)
        used_hwid = CryptoEngine.decrypt(used_hwid_enc) if used_hwid_enc else None
        
        if is_used and used_hwid != hwid:
            return False, "❌ КЛЮЧ УЖЕ ИСПОЛЬЗОВАН НА ДРУГОМ КОМПЬЮТЕРЕ!"
        if is_used and used_hwid == hwid:
            return True, "✅ ДОСТУП УЖЕ АКТИВИРОВАН НА ЭТОМ КОМПЬЮТЕРЕ!"
        
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return False, f"❌ КЛЮЧ ИСТЕК {expiry.strftime('%d.%m.%Y')}!"
        
        self.cursor.execute('UPDATE license_keys SET used_by = ?, used_hwid = ?, used_at = ?, is_used = 1 WHERE key_text = ?',
                           (CryptoEngine.encrypt(username), CryptoEngine.encrypt(hwid), CryptoEngine.encrypt(datetime.now().isoformat()), encrypted_key))
        
        user = self.cursor.execute('SELECT * FROM users WHERE hwid = ?', (CryptoEngine.encrypt(hwid),)).fetchone()
        if user:
            self.cursor.execute('UPDATE users SET username = ?, expires_at = ?, is_banned = 0, saved_key = ? WHERE hwid = ?', 
                               (CryptoEngine.encrypt(username), expires_enc, encrypted_key, CryptoEngine.encrypt(hwid)))
        else:
            self.cursor.execute('INSERT INTO users (username, hwid, created_at, expires_at, saved_key) VALUES (?, ?, ?, ?, ?)',
                               (CryptoEngine.encrypt(username), CryptoEngine.encrypt(hwid), CryptoEngine.encrypt(datetime.now().isoformat()), expires_enc, encrypted_key))
        
        self.conn.commit()
        if save:
            self.save_license(key_upper)
        return True, f"✅ ВЕРНО! ДОСТУП РАЗРЕШЁН ДО {expiry.strftime('%d.%m.%Y')}!"
    
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
        result = self.cursor.execute('SELECT username, is_admin, is_banned, expires_at FROM users WHERE hwid = ?', 
                                     (encrypted_hwid,)).fetchone()
        if not result:
            return False, "🔑 ТРЕБУЕТСЯ АКТИВАЦИЯ!"
        username_enc, is_admin, is_banned, expires_enc = result
        username = CryptoEngine.decrypt(username_enc)
        expires_at = CryptoEngine.decrypt(expires_enc)
        
        if is_banned:
            return False, "🚫 ДОСТУП ЗАБЛОКИРОВАН!"
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return False, f"⏰ ПОДПИСКА ИСТЕКЛА {expiry.strftime('%d.%m.%Y')}!"
        
        self.cursor.execute('UPDATE users SET last_active = ? WHERE hwid = ?', (CryptoEngine.encrypt(datetime.now().isoformat()), encrypted_hwid))
        self.conn.commit()
        return True, username
    
    def logout(self):
        self.delete_license()
        return True
    
    def get_all_users(self):
        users = self.cursor.execute('SELECT username, is_admin, is_banned, expires_at, hwid, saved_key FROM users ORDER BY is_admin DESC').fetchall()
        decrypted_users = []
        for user in users:
            username_enc, is_admin, is_banned, expires_enc, hwid_enc, saved_key_enc = user
            decrypted_users.append((CryptoEngine.decrypt(username_enc), is_admin, is_banned, CryptoEngine.decrypt(expires_enc), CryptoEngine.decrypt(hwid_enc), CryptoEngine.decrypt(saved_key_enc) if saved_key_enc else None))
        return decrypted_users
    
    def get_all_keys(self):
        keys = self.cursor.execute('SELECT key_text, created_at, expires_at, used_by, used_hwid, is_used FROM license_keys ORDER BY created_at DESC').fetchall()
        decrypted_keys = []
        for key in keys:
            key_enc, created_enc, expires_enc, used_by_enc, used_hwid_enc, is_used = key
            decrypted_keys.append((CryptoEngine.decrypt(key_enc), CryptoEngine.decrypt(created_enc), CryptoEngine.decrypt(expires_enc), CryptoEngine.decrypt(used_by_enc) if used_by_enc else None, CryptoEngine.decrypt(used_hwid_enc) if used_hwid_enc else None, is_used))
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
                               (encrypted_username, CryptoEngine.encrypt(f"MANUAL_{uuid.uuid4().hex[:8]}"), CryptoEngine.encrypt(datetime.now().isoformat()), encrypted_expires))
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
# АВТОМАТИЧЕСКАЯ АКТИВАЦИЯ ДЛЯ GITHUB ACTIONS
# ============================================================

def auto_activate():
    """Автоматическая активация через переменную окружения или мастер-ключ"""
    
    # 1. Пробуем через переменную окружения
    env_key = os.environ.get('ACTIVATION_KEY', '')
    if env_key:
        print(f"🔑 Использую ключ из переменной окружения")
        success, msg = db.activate_key(env_key)
        if success:
            print(f"✅ {msg}")
            return True
        else:
            print(f"❌ {msg}")
    
    # 2. Пробуем мастер-ключ
    print(f"🔑 Пробую мастер-ключ: {MASTER_KEY}")
    success, msg = db.activate_key(MASTER_KEY)
    if success:
        print(f"✅ {msg}")
        return True
    
    # 3. Пробуем загруженную лицензию
    success, msg = db.check_access_auto()
    if success:
        print(f"✅ {msg}")
        return True
    
    print(f"❌ Не удалось активировать программу!")
    print(f"ℹ️ {msg}")
    return False

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    print("="*50)
    print(f"🔥 {APP_NAME} v{VERSION}")
    print(f"{CREATOR_TEXT}")
    print("="*50)
    
    # Автоматическая активация
    if auto_activate():
        print("✅ Программа успешно активирована!")
        print("="*50)
        print("📊 Статистика:")
        users = db.get_all_users()
        keys = db.get_all_keys()
        print(f"👥 Пользователей: {len(users)}")
        print(f"🔑 Ключей: {len(keys)}")
        print("="*50)
        
        # Проверяем доступ
        access, username = db.check_access()
        if access:
            print(f"✅ Доступ разрешен для: {username}")
        else:
            print(f"❌ {username}")
    else:
        print("❌ Активация не удалась!")
        sys.exit(1)
