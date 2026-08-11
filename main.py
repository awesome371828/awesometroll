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
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
hide_console()

def get_master_key():
    data = (
        platform.node() +
        platform.processor() +
        platform.machine() +
        str(os.cpu_count()) +
        os.environ.get('COMPUTERNAME', '') +
        os.environ.get('PROCESSOR_IDENTIFIER', '')
    )
    return hashlib.sha256(data.encode()).hexdigest()[:10]

MASTER_KEY = get_master_key()

def get_encryption_key():
    return base64.urlsafe_b64encode(hashlib.sha512(MASTER_KEY.encode()).digest()[:32])

def encrypt(data):
    if data is None: return None
    try:
        if isinstance(data, str): data = data.encode('utf-8')
        elif not isinstance(data, bytes): data = str(data).encode('utf-8')
        return Fernet(get_encryption_key()).encrypt(data)
    except:
        return data

def decrypt(data):
    if data is None: return None
    try:
        if isinstance(data, str): data = data.encode('utf-8')
        return Fernet(get_encryption_key()).decrypt(data).decode('utf-8')
    except:
        return data

SUPABASE_URL = "https://yzhgcdnjuvfhcvwedgga.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6aGdjZG5qdXZmaGN3dmVkZ2dhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY0NjExNTgsImV4cCI6MjEwMjAzNzE1OH0.ccCiaKPnpwjg69PC90qtPDOIWn5PezGxKERJtdWUB_I"

class CloudDB:
    @classmethod
    def _request(cls, method, endpoint, data=None):
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        try:
            if method == "GET":
                r = requests.get(url, headers=headers)
            elif method == "POST":
                r = requests.post(url, headers=headers, json=data)
            elif method == "PATCH":
                r = requests.patch(url, headers=headers, json=data)
            return r.json() if r.ok else None
        except:
            return None
    
    @classmethod
    def get_all_users(cls):
        return cls._request("GET", "users?order=id.desc")
    
    @classmethod
    def insert_user(cls, username, hwid, expires_at, saved_key, is_owner=0, is_admin=0):
        return cls._request("POST", "users", {
            "username": username,
            "hwid": hwid,
            "is_owner": is_owner,
            "is_admin": is_admin,
            "expires_at": expires_at,
            "saved_key": saved_key
        })
    
    @classmethod
    def get_all_keys(cls):
        return cls._request("GET", "license_keys?order=id.desc")
    
    @classmethod
    def insert_key(cls, key_text, expires_at, owner_hwid):
        return cls._request("POST", "license_keys", {
            "key_text": key_text,
            "expires_at": expires_at,
            "owner_hwid": owner_hwid,
            "is_used": 0
        })
    
    @classmethod
    def activate_key_cloud(cls, key_text, used_by, used_hwid):
        return cls._request("PATCH", f"license_keys?key_text=eq.{key_text}", {
            "used_by": used_by,
            "used_hwid": used_hwid,
            "used_at": datetime.now().isoformat(),
            "is_used": 1
        })

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

APP_DIR = get_app_dir()
DB_FILE = os.path.join(APP_DIR, "troll_users.db")
SETTINGS_FILE = os.path.join(APP_DIR, "troll_settings.json")
LICENSE_FILE = os.path.join(APP_DIR, "license.key")

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
        encrypted = encrypt(data)
        return hashlib.sha512(encrypted).hexdigest()[:64]

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
    
    def get_hwid(self):
        return ComputerID.get_full_hwid()
    
    def check_master_key(self, key):
        return key.upper() == MASTER_KEY.upper()
    
    def save_license(self, key):
        encrypted_key = encrypt(key)
        with open(LICENSE_FILE, 'w') as f:
            f.write(base64.b64encode(encrypted_key).decode('utf-8'))
    
    def load_license(self):
        if os.path.exists(LICENSE_FILE):
            try:
                with open(LICENSE_FILE, 'r') as f:
                    encrypted_key = base64.b64decode(f.read().strip().encode('utf-8'))
                return decrypt(encrypted_key)
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
                (encrypt(key), encrypt(created_at), 
                 encrypt(expires_at), encrypt(owner_hwid)))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return False, None
        
        try:
            CloudDB.insert_key(key, expires_at, owner_hwid)
        except:
            pass
        
        return True, key
    
    def delete_key(self, key_text):
        self.cursor.execute('DELETE FROM license_keys WHERE key_text = ?', (encrypt(key_text),))
        self.conn.commit()
        return True
    
    def activate_key(self, key_text, save=True):
        hwid = self.get_hwid()
        username = ComputerID.get_username()
        key_upper = key_text.upper()
        
        if self.check_master_key(key_upper):
            encrypted_hwid = encrypt(hwid)
            encrypted_username = encrypt(username)
            encrypted_expires = encrypt("2099-12-31T23:59:59")
            encrypted_key = encrypt(key_upper)
            
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
                     encrypt(datetime.now().isoformat()), 
                     encrypted_expires, encrypted_key))
            self.conn.commit()
            if save:
                self.save_license(key_upper)
            
            try:
                CloudDB.insert_user(username, hwid, "2099-12-31T23:59:59", key_upper, 1, 1)
            except:
                pass
            
            return True, "👑 ДОБРО ПОЖАЛОВАТЬ, ОВНЕР!"
        
        encrypted_key = encrypt(key_upper)
        result = self.cursor.execute('''SELECT key_text, expires_at, is_used, used_hwid, owner_hwid 
            FROM license_keys WHERE key_text = ?''', (encrypted_key,)).fetchone()
        
        if not result:
            return False, "❌ НЕВЕРНЫЙ КЛЮЧ!"
        
        key_enc, expires_enc, is_used, used_hwid_enc, owner_hwid_enc = result
        expires_at = decrypt(expires_enc)
        used_hwid = decrypt(used_hwid_enc) if used_hwid_enc else None
        owner_hwid = decrypt(owner_hwid_enc) if owner_hwid_enc else None
        
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
            (encrypt(username), encrypt(hwid), 
             encrypt(datetime.now().isoformat()), encrypted_key))
        
        user = self.cursor.execute('SELECT * FROM users WHERE hwid = ?', (encrypt(hwid),)).fetchone()
        if user:
            self.cursor.execute('''UPDATE users SET 
                username = ?, expires_at = ?, is_banned = 0, saved_key = ? 
                WHERE hwid = ?''', 
                (encrypt(username), expires_enc, encrypted_key, encrypt(hwid)))
        else:
            self.cursor.execute('''INSERT INTO users 
                (username, hwid, created_at, expires_at, saved_key) 
                VALUES (?, ?, ?, ?, ?)''',
                (encrypt(username), encrypt(hwid), 
                 encrypt(datetime.now().isoformat()), expires_enc, encrypted_key))
        
        self.conn.commit()
        if save:
            self.save_license(key_upper)
        
        try:
            CloudDB.insert_user(username, hwid, expires_at, key_upper, 0, 0)
            CloudDB.activate_key_cloud(key_upper, username, hwid)
        except:
            pass
        
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
        encrypted_hwid = encrypt(hwid)
        result = self.cursor.execute('''SELECT username, is_owner, is_admin, is_banned, expires_at 
            FROM users WHERE hwid = ?''', (encrypted_hwid,)).fetchone()
        
        if not result:
            return False, "🔑 ТРЕБУЕТСЯ АКТИВАЦИЯ!"
        
        username_enc, is_owner, is_admin, is_banned, expires_enc = result
        username = decrypt(username_enc)
        expires_at = decrypt(expires_enc)
        
        if is_banned:
            return False, "🚫 ДОСТУП ЗАБЛОКИРОВАН!"
        
        expiry = datetime.fromisoformat(expires_at)
        if datetime.now() > expiry:
            return False, f"⏰ ПОДПИСКА ИСТЕКЛА {expiry.strftime('%d.%m.%Y')}!"
        
        self.cursor.execute('UPDATE users SET last_active = ? WHERE hwid = ?', 
                           (encrypt(datetime.now().isoformat()), encrypted_hwid))
        self.conn.commit()
        return True, username
    
    def logout(self):
        self.delete_license()
        return True
    
    def get_all_users(self):
        try:
            cloud_users = CloudDB.get_all_users()
            if cloud_users:
                decrypted_users = []
                for u in cloud_users:
                    decrypted_users.append((
                        u.get('username', ''),
                        u.get('is_owner', 0),
                        u.get('is_admin', 0),
                        u.get('is_banned', 0),
                        u.get('expires_at', ''),
                        u.get('hwid', ''),
                        u.get('saved_key', '')
                    ))
                return decrypted_users
        except:
            pass
        
        users = self.cursor.execute('''SELECT username, is_owner, is_admin, is_banned, 
            expires_at, hwid, saved_key FROM users ORDER BY is_owner DESC, is_admin DESC''').fetchall()
        decrypted_users = []
        for user in users:
            username_enc, is_owner, is_admin, is_banned, expires_enc, hwid_enc, saved_key_enc = user
            decrypted_users.append((
                decrypt(username_enc),
                is_owner,
                is_admin,
                is_banned,
                decrypt(expires_enc),
                decrypt(hwid_enc),
                decrypt(saved_key_enc) if saved_key_enc else None
            ))
        return decrypted_users
    
    def get_all_keys(self):
        try:
            cloud_keys = CloudDB.get_all_keys()
            if cloud_keys:
                decrypted_keys = []
                for k in cloud_keys:
                    decrypted_keys.append((
                        k.get('key_text', ''),
                        k.get('created_at', ''),
                        k.get('expires_at', ''),
                        k.get('used_by', ''),
                        k.get('used_hwid', ''),
                        k.get('is_used', 0),
                        k.get('owner_hwid', '')
                    ))
                return decrypted_keys
        except:
            pass
        
        keys = self.cursor.execute('''SELECT key_text, created_at, expires_at, 
            used_by, used_hwid, is_used, owner_hwid 
            FROM license_keys ORDER BY created_at DESC''').fetchall()
        decrypted_keys = []
        for key in keys:
            key_enc, created_enc, expires_enc, used_by_enc, used_hwid_enc, is_used, owner_hwid_enc = key
            decrypted_keys.append((
                decrypt(key_enc),
                decrypt(created_enc),
                decrypt(expires_enc),
                decrypt(used_by_enc) if used_by_enc else None,
                decrypt(used_hwid_enc) if used_hwid_enc else None,
                is_used,
                decrypt(owner_hwid_enc) if owner_hwid_enc else None
            ))
        return decrypted_keys
    
    def give_access(self, username, months=1):
        expires_at = (datetime.now() + timedelta(days=30 * months)).isoformat()
        encrypted_username = encrypt(username)
        encrypted_expires = encrypt(expires_at)
        
        user = self.cursor.execute('SELECT * FROM users WHERE username = ?', (encrypted_username,)).fetchone()
        if user:
            self.cursor.execute('UPDATE users SET expires_at = ?, is_banned = 0 WHERE username = ?', 
                               (encrypted_expires, encrypted_username))
        else:
            self.cursor.execute('INSERT INTO users (username, hwid, created_at, expires_at) VALUES (?, ?, ?, ?)',
                               (encrypted_username, encrypt(f"MANUAL_{uuid.uuid4().hex[:8]}"), 
                                encrypt(datetime.now().isoformat()), encrypted_expires))
        self.conn.commit()
        return True, f"✅ ДОСТУП ВЫДАН {username} НА {months} МЕСЯЦЕВ!"
    
    def revoke_access(self, username):
        self.cursor.execute('UPDATE users SET is_banned = 1 WHERE username = ?', (encrypt(username),))
        self.conn.commit()
        return True
    
    def restore_access(self, username):
        self.cursor.execute('UPDATE users SET is_banned = 0 WHERE username = ?', (encrypt(username),))
        self.conn.commit()
        return True
    
    def extend_access(self, username, months=1):
        result = self.cursor.execute('SELECT expires_at FROM users WHERE username = ?', (encrypt(username),)).fetchone()
        if result:
            expires_enc = result[0]
            expires_at = decrypt(expires_enc)
            new_expiry = datetime.fromisoformat(expires_at) + timedelta(days=30 * months)
            self.cursor.execute('UPDATE users SET expires_at = ? WHERE username = ?', 
                               (encrypt(new_expiry.isoformat()), encrypt(username)))
            self.conn.commit()
            return True, f"✅ ПРОДЛЕН ДО {new_expiry.strftime('%d.%m.%Y')}!"
        return False, "❌ ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН!"

db = UserDB()

def start_program():
    root = tk.Tk()
    root.title("🔥 AWESOMETROLLING")
    root.geometry("500x400")
    root.configure(bg='#0a0e27')
    
    tk.Label(root, text="🔥 AWESOMETROLLING", font=("Segoe UI", 30, "bold"), 
             bg='#0a0e27', fg='#ffd700').pack(pady=30)
    tk.Label(root, text="✅ Программа активирована!", font=("Segoe UI", 14), 
             bg='#0a0e27', fg='#00ff88').pack()
    tk.Label(root, text=f"🔑 Мастер-ключ: {MASTER_KEY}", font=("Segoe UI", 12), 
             bg='#0a0e27', fg='#ff6b35').pack(pady=10)
    tk.Button(root, text="ВЫХОД", command=root.quit, 
              bg='#e17055', fg='white', font=("Segoe UI", 10, "bold"), 
              relief=tk.FLAT, cursor="hand2", padx=20, pady=10).pack(pady=20)
    
    root.mainloop()

def show_activation():
    hide_console()
    root = tk.Tk()
    root.title("🔐 АКТИВАЦИЯ")
    root.geometry("450x350")
    root.configure(bg='#0a0e27')
    
    tk.Label(root, text="🔥 AWESOMETROLLING", font=("Segoe UI", 24, "bold"), 
             bg='#0a0e27', fg='#ffd700').pack(pady=20)
    tk.Label(root, text="🔑 ВВЕДИТЕ КЛЮЧ", font=("Segoe UI", 14), 
             bg='#0a0e27', fg='#dfe6e9').pack(pady=5)
    
    entry = tk.Entry(root, font=("Segoe UI", 14), bg='#1a1f4a', 
                     fg='#00ff88', relief=tk.FLAT, borderwidth=2)
    entry.pack(pady=10, padx=40, fill=tk.X)
    entry.focus()
    
    status_label = tk.Label(root, text="", bg='#0a0e27', fg='#e17055')
    status_label.pack()
    
    def activate():
        key = entry.get().strip()
        if not key:
            status_label.config(text="❌ ВВЕДИТЕ КЛЮЧ!", fg='#e17055')
            return
        
        success, msg = db.activate_key(key)
        if success:
            status_label.config(text="✅ " + msg, fg='#00b894')
            root.after(1500, lambda: [root.destroy(), start_program()])
        else:
            status_label.config(text="❌ " + msg, fg='#e17055')
    
    tk.Button(root, text="АКТИВИРОВАТЬ", command=activate, 
              bg='#6c5ce7', fg='white', font=("Segoe UI", 10, "bold"), 
              relief=tk.FLAT, cursor="hand2", padx=20, pady=10).pack(pady=10)
    
    root.bind('<Return>', lambda e: activate())
    root.mainloop()

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
