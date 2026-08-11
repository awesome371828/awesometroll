import sys
import os
import traceback

# ============================================================
# ОТЛАДКА - ЛОГИРОВАНИЕ ОШИБОК
# ============================================================

def log_error(error_msg):
    """Запись ошибок в файл"""
    try:
        with open('error_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now()}: {error_msg}\n")
    except:
        pass

try:
    import base64, zlib, random, hashlib, sys, os, time, json, sqlite3, uuid, subprocess, platform, threading, re, ctypes
    from datetime import datetime, timedelta
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import tkinter as tk
    from tkinter import scrolledtext, ttk, messagebox
except Exception as e:
    # Если библиотеки не установлены - выводим сообщение
    try:
        import tkinter as tk
        root = tk.Tk()
        tk.messagebox.showerror("Ошибка", f"Не удалось загрузить библиотеки:\n{e}\n\nУстановите: pip install cryptography keyboard")
        root.destroy()
    except:
        pass
    sys.exit(1)

# ============================================================
# ОБФУСКАЦИЯ СТРОК
# ============================================================

class Obfuscator:
    _key_cache = {}
    _salt = b'\x7f\x8e\x9a\x1b\x2c\x3d\x4e\x5f\x6a\x7b\x8c\x9d\xae\xbf\xc1\xd2'
    
    @classmethod
    def _get_key(cls, seed):
        if seed not in cls._key_cache:
            try:
                kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=cls._salt, iterations=500000)
                cls._key_cache[seed] = base64.urlsafe_b64encode(kdf.derive(str(seed).encode()))
            except Exception as e:
                log_error(f"Ошибка генерации ключа: {e}")
                cls._key_cache[seed] = hashlib.sha512(str(seed).encode()).digest()[:32]
        return cls._key_cache[seed]
    
    @classmethod
    def encode(cls, text, seed=None):
        if seed is None:
            seed = random.randint(100000, 999999)
        try:
            compressed = zlib.compress(text.encode('utf-8'), level=9)
            f = Fernet(cls._get_key(seed))
            encrypted = f.encrypt(compressed)
            b64 = base64.b64encode(encrypted).decode('ascii')
            chars = list(b64)
            for i in range(len(chars) - 1, 0, -1):
                if random.random() > 0.7:
                    chars.insert(i, random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/='))
            obfuscated = ''.join(chars)
            checksum = hashlib.md5(f"{seed}:{b64}".encode()).hexdigest()[:8]
            return f"__{checksum}__{seed}__{obfuscated}"
        except Exception as e:
            log_error(f"Ошибка кодирования: {e}")
            return text
    
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
            f = Fernet(cls._get_key(seed))
            decrypted = f.decrypt(encrypted)
            return zlib.decompress(decrypted).decode('utf-8')
        except Exception as e:
            log_error(f"Ошибка декодирования: {e}")
            return encoded

# ============================================================
# КЛАСС ДЛЯ ЗАЩИЩЕННЫХ ДАННЫХ
# ============================================================

class X:
    _data = None
    
    @classmethod
    def _get_data(cls):
        if cls._data is None:
            cls._data = {
                'a1': Obfuscator.encode('@flidges'),
                'a2': Obfuscator.encode('✨ Создатель: awesome / tg @flidges ✨'),
                'a3': Obfuscator.encode('3.0'),
                'a4': Obfuscator.encode('💜 Сделано с любовью и матом 💜'),
                'a5': Obfuscator.encode('AWESOMETROLLING'),
                'a6': Obfuscator.encode('💰 Цена - узнайте у @flidges'),
                'a7': Obfuscator.encode('AWESPREMI'),
            }
        return cls._data
    
    @classmethod
    def get(cls, key):
        try:
            return Obfuscator.decode(cls._get_data().get(key, ''))
        except:
            return ""

# ============================================================
# ШИФРОВАНИЕ ДАННЫХ
# ============================================================

class CryptoEngine:
    _SALT_B64 = b'YXdlc29tZXBsb2swMQ=='
    
    @classmethod
    def _get_salt(cls):
        try:
            return hashlib.sha256(base64.b64decode(cls._SALT_B64)).digest()[:16]
        except:
            return b'\x00' * 16
    
    @classmethod
    def _get_system_key(cls):
        try:
            parts = [platform.node(), platform.processor(), platform.machine(), str(os.cpu_count()), 
                    os.environ.get('PROCESSOR_IDENTIFIER', ''), os.environ.get('COMPUTERNAME', '')]
            combined = '|'.join(parts) + base64.b64decode(cls._SALT_B64).decode()
            return hashlib.sha512(combined.encode()).hexdigest()
        except:
            return hashlib.sha512("fallback_key".encode()).hexdigest()
    
    @classmethod
    def _derive_master_key(cls):
        try:
            kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=cls._get_salt(), iterations=300000)
            return base64.urlsafe_b64encode(kdf.derive(cls._get_system_key().encode()))
        except:
            return base64.b64encode(hashlib.sha512(cls._get_system_key().encode()).digest()[:32])
    
    @classmethod
    def encrypt(cls, data):
        if data is None:
            return None
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            elif not isinstance(data, bytes):
                data = str(data).encode('utf-8')
            return Fernet(cls._derive_master_key()).encrypt(data)
        except Exception as e:
            log_error(f"Encrypt error: {e}")
            key = hashlib.sha512(cls._get_system_key().encode()).digest()
            result = bytearray()
            for i, byte in enumerate(data):
                result.append(byte ^ key[i % len(key)])
            return bytes(result)
    
    @classmethod
    def decrypt(cls, encrypted_data):
        if encrypted_data is None:
            return None
        try:
            if isinstance(encrypted_data, str):
                encrypted_data = encrypted_data.encode('utf-8')
            decrypted = Fernet(cls._derive_master_key()).decrypt(encrypted_data)
            try:
                return decrypted.decode('utf-8')
            except:
                return decrypted
        except Exception as e:
            log_error(f"Decrypt error: {e}")
            key = hashlib.sha512(cls._get_system_key().encode()).digest()
            result = bytearray()
            for i, byte in enumerate(encrypted_data):
                result.append(byte ^ key[i % len(key)])
            try:
                return result.decode('utf-8')
            except:
                return result

# ============================================================
# ИНИЦИАЛИЗАЦИЯ КОНСТАНТ
# ============================================================

DEVELOPER = X.get('a1')
CREATOR_TEXT = X.get('a2')
VERSION = X.get('a3')
LOVE_TEXT = X.get('a4')
APP_NAME = X.get('a5')
PRICE_TEXT = X.get('a6')
MASTER_KEY = X.get('a7')

COLORS = {
    'bg': '#0a0e27', 'bg2': '#111638', 'bg3': '#1a1f4a', 'bg4': '#222860',
    'bg5': '#2d3570', 'gradient_start': '#6c5ce7', 'gradient_end': '#fd79a8',
    'accent': '#6c5ce7', 'accent2': '#a29bfe', 'pink': '#fd79a8',
    'text': '#dfe6e9', 'text2': '#b2bec3', 'text3': '#636e72',
    'success': '#00b894', 'danger': '#e17055', 'warning': '#fdcb6e',
    'gold': '#ffd700', 'neon': '#00ff88', 'neon_orange': '#ff6b35',
    'neon_blue': '#4fc3f7', 'shadow': '#1a1f4a'
}

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
# ОСТАЛЬНОЙ КОД (все функции из предыдущей версии)
# ============================================================

# [ЗДЕСЬ ВСТАВЬТЕ ВЕСЬ ОСТАЛЬНОЙ КОД ИЗ ПРЕДЫДУЩЕЙ ВЕРСИИ]
# Включая ComputerID, UserDB, InsultStorage, все функции, AdminPanel, InsultApp и т.д.

# ============================================================
# ГЛАВНАЯ ФУНКЦИЯ С ОТЛАДКОЙ
# ============================================================

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def show_activation():
    try:
        hide_console()
        root = tk.Tk()
        root.title(f"🔐 АКТИВАЦИЯ | {APP_NAME}")
        root.geometry("400x300")
        root.configure(bg=COLORS['bg'])
        
        tk.Label(root, text=f"🔥 {APP_NAME}", font=("Segoe UI", 20, "bold"), 
                bg=COLORS['bg'], fg=COLORS['gold']).pack(pady=20)
        
        tk.Label(root, text="Введите ключ активации:", 
                bg=COLORS['bg'], fg=COLORS['text']).pack()
        
        entry = tk.Entry(root, font=("Segoe UI", 14), bg=COLORS['bg3'], 
                        fg=COLORS['neon'], relief=tk.FLAT, borderwidth=2)
        entry.pack(pady=10, padx=20, fill=tk.X)
        entry.focus()
        
        status_label = tk.Label(root, text="", bg=COLORS['bg'], fg=COLORS['danger'], 
                               font=("Segoe UI", 10))
        status_label.pack()
        
        def activate():
            key = entry.get().strip()
            if not key:
                status_label.config(text="❌ ВВЕДИТЕ КЛЮЧ!", fg=COLORS['danger'])
                return
            
            if key.upper() == MASTER_KEY:
                status_label.config(text="✅ ДОБРО ПОЖАЛОВАТЬ, ВЛАДЕЛЕЦ!", fg=COLORS['success'])
                root.after(1000, lambda: [root.destroy(), start_program()])
            else:
                status_label.config(text="❌ НЕВЕРНЫЙ КЛЮЧ!", fg=COLORS['danger'])
        
        tk.Button(root, text="АКТИВИРОВАТЬ", command=activate,
                 bg=COLORS['gradient_start'], fg='white', font=("Segoe UI", 12, "bold"),
                 relief=tk.FLAT, cursor="hand2", padx=20, pady=10).pack(pady=10)
        
        root.bind('<Return>', lambda e: activate())
        root.mainloop()
    except Exception as e:
        log_error(f"Ошибка в окне активации: {e}")
        messagebox.showerror("Ошибка", f"Ошибка: {e}\n\nПроверьте error_log.txt")

def start_program():
    try:
        hide_console()
        root = tk.Tk()
        root.title(f"🔥 {APP_NAME} | {DEVELOPER}")
        root.geometry("800x650")
        root.configure(bg=COLORS['bg'])
        root.minsize(700, 550)
        root.resizable(True, True)
        
        # Простое окно для проверки
        tk.Label(root, text=f"🔥 {APP_NAME}", font=("Segoe UI", 40, "bold"),
                bg=COLORS['bg'], fg=COLORS['gold']).pack(pady=50)
        tk.Label(root, text=CREATOR_TEXT, font=("Segoe UI", 16),
                bg=COLORS['bg'], fg=COLORS['neon_orange']).pack()
        tk.Label(root, text=LOVE_TEXT, font=("Segoe UI", 14),
                bg=COLORS['bg'], fg=COLORS['pink']).pack(pady=20)
        tk.Label(root, text=f"Версия: {VERSION}", font=("Segoe UI", 12),
                bg=COLORS['bg'], fg=COLORS['text2']).pack()
        
        tk.Button(root, text="Выход", command=root.quit,
                 bg=COLORS['danger'], fg='white', font=("Segoe UI", 10, "bold"),
                 relief=tk.FLAT, cursor="hand2", padx=20, pady=10).pack(pady=30)
        
        root.mainloop()
    except Exception as e:
        log_error(f"Ошибка в start_program: {e}")
        messagebox.showerror("Ошибка", f"Ошибка: {e}\n\nПроверьте error_log.txt")

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    try:
        # Проверяем установку библиотек
        import keyboard
        import cryptography
    except ImportError as e:
        try:
            root = tk.Tk()
            messagebox.showerror("Ошибка", f"Не установлены библиотеки:\n{e}\n\nУстановите:\npip install keyboard cryptography")
            root.destroy()
        except:
            pass
        sys.exit(1)
    
    # Запускаем
    try:
        show_activation()
    except Exception as e:
        log_error(f"Критическая ошибка: {e}")
        try:
            root = tk.Tk()
            messagebox.showerror("Ошибка", f"Критическая ошибка:\n{e}\n\nПроверьте error_log.txt")
            root.destroy()
        except:
            pass
