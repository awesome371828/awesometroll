import base64 as a, zlib as b, random as c, hashlib as d, sys as e, os as f, time as g, json as h, sqlite3 as i, uuid as j, subprocess as k, platform as l, threading as m, re as n, ctypes as o
from datetime import datetime as p, timedelta as q
from cryptography.fernet import Fernet as r
from cryptography.hazmat.primitives import hashes as s
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as t
import tkinter as u
from tkinter import scrolledtext as v, ttk as w, messagebox as x

class _:
    _a = {}
    _b = b'\x7f\x8e\x9a\x1b\x2c\x3d\x4e\x5f\x6a\x7b\x8c\x9d\xae\xbf\xc1\xd2'
    @classmethod
    def _(cls, c):
        if c not in cls._a:
            _ = t(algorithm=s.SHA512(), length=32, salt=cls._b, iterations=500000)
            cls._a[c] = a.urlsafe_b64encode(_.derive(str(c).encode()))
        return cls._a[c]
    @classmethod
    def __(cls, ___, ____=None):
        if ____ is None: ____ = c.randint(100000, 999999)
        _ = b.compress(___.encode('utf-8'), level=9)
        __ = r(cls._(____)).encrypt(_)
        ___ = a.b64encode(__).decode('ascii')
        ____ = list(___)
        for _____ in range(len(____) - 1, 0, -1):
            if c.random() > 0.7:
                ____.insert(_____, c.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/='))
        _____ = ''.join(____)
        ______ = d.md5(f"{____}:{___}".encode()).hexdigest()[:8]
        return f"__{______}__{____}__{_____}"
    @classmethod
    def ___(cls, ________):
        try:
            ___ = ________.split('__')
            if len(___) < 4: return ________
            ____ = ___[1]; _____ = int(___[2]); ______ = ___[3]
            _______ = ''
            for ________ in ______:
                if ________ in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/=':
                    _______ += ________
            if d.md5(f"{_____}:{_______}".encode()).hexdigest()[:8] != ____: return ________
            ________ = a.b64decode(_______)
            _________ = r(cls._(_____)).decrypt(________)
            return b.decompress(_________).decode('utf-8')
        except: return ________

class __:
    _ = None
    @classmethod
    def _(cls):
        if cls._ is None:
            cls._ = {
                'a': _.__('@flidges'),
                'b': _.__('👁️ Создатель: awesome / tg @flidges 👀'),
                'c': _.__('3.0'),
                'd': _.__('❤️ Сделано с любовью и матом 💖'),
                'e': _.__('AWESOMETROLLING'),
                'f': _.__('😍 Цена - узнайте у @flidges'),
                'g': _.__('awesome'),
            }
        return cls._
    @classmethod
    def __(cls, k):
        try: return _.___(cls._().get(k, ''))
        except: return ""

___ = __.__('a')
____ = __.__('b')
_____ = __.__('c')
______ = __.__('d')
_______ = __.__('e')
________ = __.__('f')
_________ = __.__('g')

COLORS = {
    'bg': _.__('#0a0e27'),
    'bg2': _.__('#111638'),
    'bg3': _.__('#1a1f4a'),
    'bg4': _.__('#222860'),
    'bg5': _.__('#2d3570'),
    'gradient_start': _.__('#6c5ce7'),
    'gradient_end': _.__('#fd79a8'),
    'accent': _.__('#6c5ce7'),
    'accent2': _.__('#a29bfe'),
    'pink': _.__('#fd79a8'),
    'text': _.__('#dfe6e9'),
    'text2': _.__('#b2bec3'),
    'text3': _.__('#636e72'),
    'success': _.__('#00b894'),
    'danger': _.__('#e17055'),
    'warning': _.__('#fdcb6e'),
    'gold': _.__('#ffd700'),
    'neon': _.__('#00ff88'),
    'neon_orange': _.__('#ff6b35'),
    'neon_blue': _.__('#4fc3f7'),
    'shadow': _.__('#1a1f4a')
}

class ___:
    _ = b'YXdlc29tZXBsb2swMQ=='
    @classmethod
    def _(cls):
        return d.sha256(a.b64decode(cls._)).digest()[:16]
    @classmethod
    def __(cls):
        _ = [l.node(), l.processor(), l.machine(), str(f.cpu_count()), f.environ.get('PROCESSOR_IDENTIFIER', ''), f.environ.get('COMPUTERNAME', '')]
        __ = '|'.join(_) + a.b64decode(cls._).decode()
        return d.sha512(__.encode()).hexdigest()
    @classmethod
    def ___(cls):
        _ = t(algorithm=s.SHA512(), length=32, salt=cls._(), iterations=300000)
        return a.urlsafe_b64encode(_.derive(cls.__().encode()))
    @classmethod
    def ____(cls, _):
        if _ is None: return None
        try:
            if isinstance(_, str): _ = _.encode('utf-8')
            elif not isinstance(_, bytes): _ = str(_).encode('utf-8')
            return r(cls.___()).encrypt(_)
        except:
            __ = d.sha512(cls.__().encode()).digest()
            ___ = bytearray()
            for ____, _____ in enumerate(_):
                ___.append(_____ ^ __[____ % len(__)])
            return bytes(___)
    @classmethod
    def _____(cls, _):
        if _ is None: return None
        try:
            if isinstance(_, str): _ = _.encode('utf-8')
            __ = r(cls.___()).decrypt(_)
            try: return __.decode('utf-8')
            except: return __
        except:
            __ = d.sha512(cls.__().encode()).digest()
            ___ = bytearray()
            for ____, _____ in enumerate(_):
                ___.append(_____ ^ __[____ % len(__)])
            try: return ___.decode('utf-8')
            except: return ___

def ____():
    if getattr(e, 'frozen', False):
        return f.dirname(e.executable)
    else:
        return f.dirname(f.abspath(__file__))

_____ = ____()
______ = f.join(_____, "troll_users.db")
_______ = f.join(_____, "troll_settings.json")
________ = f.join(_____, "license.key")

class _____:
    @staticmethod
    def _():
        try:
            _ = j.getnode()
            return ':'.join(('%012x' % _)[_: _+2] for _ in range(0, 12, 2))
        except: return "unknown_mac"
    @staticmethod
    def __():
        try: return f.environ.get('COMPUTERNAME', 'unknown')
        except: return "unknown"
    @staticmethod
    def ___():
        try: return f.environ.get('USERNAME', 'unknown')
        except: return "unknown"
    @staticmethod
    def ____():
        try:
            if l.system() == 'Windows':
                _ = k.run(['wmic', 'diskdrive', 'get', 'serialnumber'], capture_output=True, text=True)
                __ = _.stdout.strip().split('\n')
                if len(__) > 1: return __[1].strip()
            return "unknown_disk"
        except: return "unknown_disk"
    @staticmethod
    def _____():
        try:
            if l.system() == 'Windows':
                _ = k.run(['wmic', 'cpu', 'get', 'processorid'], capture_output=True, text=True)
                __ = _.stdout.strip().split('\n')
                if len(__) > 1: return __[1].strip()
            return "unknown_cpu"
        except: return "unknown_cpu"
    @staticmethod
    def ______():
        _ = (_____._() + _____.__() + _____.___() + _____.____() + _____._____() + l.processor() + l.machine())
        __ = ___ .____(_.encode())
        return d.sha512(__).hexdigest()[:64]

class ______:
    def __init__(self):
        self._ = i.connect(______)
        self.__ = self._.cursor()
        self.___()
    def ___ (self):
        self.__.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, hwid TEXT UNIQUE NOT NULL, mac TEXT, computer_name TEXT, is_admin INTEGER DEFAULT 0, is_banned INTEGER DEFAULT 0, created_at TEXT, expires_at TEXT, last_active TEXT, saved_key TEXT)')
        self.__.execute('CREATE TABLE IF NOT EXISTS license_keys (id INTEGER PRIMARY KEY AUTOINCREMENT, key_text TEXT UNIQUE NOT NULL, created_at TEXT, expires_at TEXT, used_by TEXT, used_hwid TEXT, used_at TEXT, is_used INTEGER DEFAULT 0)')
        self.__.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, timestamp TEXT)')
        self._.commit()
    def ____(self, _):
        if _ is None: return None
        return ___ .____(_)
    def _____(self, _):
        if _ is None: return None
        return ___ ._____(_)
    def ______(self):
        return _____.______()
    def _______(self, _):
        return _.upper() == _________.upper()
    def ________(self, _):
        __ = ___ .____(_)
        with open(________, 'w') as ___:
            ___.write(a.b64encode(__).decode('utf-8'))
    def _________(self):
        if f.exists(________):
            try:
                with open(________, 'r') as _:
                    __ = a.b64decode(_.read().strip().encode('utf-8'))
                return ___ ._____(__)
            except: return None
        return None
    def __________ (self):
        if f.exists(________): f.remove(________)
    def ___________(self, _=1, __=None):
        ___ = __ if __ else d.sha256(f"{j.uuid4()}{g.time()}".encode()).hexdigest()[:12].upper()
        ____ = p.now().isoformat()
        _____ = (p.now() + q(days=30 * _)).isoformat()
        try:
            self.__.execute('INSERT INTO license_keys (key_text, created_at, expires_at, is_used) VALUES (?, ?, ?, 0)', 
                           (___ .____(___), ___ .____(____), ___ .____(_____)))
            self._.commit()
            return True, ___
        except i.IntegrityError:
            return False, None
    def ____________(self, _):
        self.__.execute('DELETE FROM license_keys WHERE key_text = ?', (___ .____(_),))
        self._.commit()
        return True
    def _____________(self, _, __=True):
        ___ = self.______()
        ____ = _____.___()
        _____ = _.upper()
        if self._______(_____):
            ______ = ___ .____(___)
            _______ = ___ .____(____)
            ________ = ___ .____("2099-12-31T23:59:59")
            _________ = ___ .____(_____)
            __________ = self.__.execute('SELECT * FROM users WHERE hwid = ?', (______,)).fetchone()
            if __________:
                self.__.execute('UPDATE users SET username = ?, is_admin = 1, is_banned = 0, expires_at = ?, saved_key = ? WHERE hwid = ?', 
                               (_______, ________, _________, ______))
            else:
                self.__.execute('INSERT INTO users (username, hwid, is_admin, created_at, expires_at, saved_key) VALUES (?, ?, 1, ?, ?, ?)',
                               (_______, ______, ___ .____(p.now().isoformat()), ________, _________))
            self._.commit()
            if __:
                self.________(_____)
            return True, "👑 ДОБРО ПОЖАЛОВАТЬ, ВЛАДЕЛЕЦ!"
        ___________ = ___ .____(_____)
        ____________ = self.__.execute('SELECT key_text, expires_at, is_used, used_hwid FROM license_keys WHERE key_text = ?', 
                                     (___________,)).fetchone()
        if not ____________:
            return False, "❌ НЕВЕРНЫЙ КЛЮЧ!"
        _____________ , ______________, _______________, ________________ = ____________
        ________________ = ___ ._____(______________)
        _________________ = ___ ._____(________________) if ________________ else None
        if _______________ and _________________ != ___:
            return False, "❌ КЛЮЧ УЖЕ ИСПОЛЬЗОВАН НА ДРУГОМ КОМПЬЮТЕРЕ!"
        if _______________ and _________________ == ___:
            return True, "✅ ДОСТУП УЖЕ АКТИВИРОВАН НА ЭТОМ КОМПЬЮТЕРЕ!"
        __________________ = p.fromisoformat(________________)
        if p.now() > __________________:
            return False, f"❌ КЛЮЧ ИСТЕК {__________________.strftime('%d.%m.%Y')}!"
        self.__.execute('UPDATE license_keys SET used_by = ?, used_hwid = ?, used_at = ?, is_used = 1 WHERE key_text = ?',
                       (___ .____(____), ___ .____(___), ___ .____(p.now().isoformat()), ___________))
        ___________________ = self.__.execute('SELECT * FROM users WHERE hwid = ?', (___ .____(___),)).fetchone()
        if ___________________:
            self.__.execute('UPDATE users SET username = ?, expires_at = ?, is_banned = 0, saved_key = ? WHERE hwid = ?', 
                           (___ .____(____), ______________, ___________, ___ .____(___)))
        else:
            self.__.execute('INSERT INTO users (username, hwid, created_at, expires_at, saved_key) VALUES (?, ?, ?, ?, ?)',
                           (___ .____(____), ___ .____(___), ___ .____(p.now().isoformat()), ______________, ___________))
        self._.commit()
        if __:
            self.________(_____)
        return True, f"✅ ВЕРНО! ДОСТУП РАЗРЕШЁН ДО {__________________.strftime('%d.%m.%Y')}!"
    def ______________(self):
        _ = self._________()
        if _:
            __, ___ = self._____________(_, save=False)
            if __:
                return True, ___
        return False, None
    def _______________(self):
        _ = self.______()
        __ = ___ .____(_)
        ___ = self.__.execute('SELECT username, is_admin, is_banned, expires_at FROM users WHERE hwid = ?', 
                                     (__,)).fetchone()
        if not ___:
            return False, "🔑 ТРЕБУЕТСЯ АКТИВАЦИЯ!"
        ____, _____, ______, _______ = ___
        ________ = ___ ._____(____)
        _________ = ___ ._____(_______)
        if ______:
            return False, "🚫 ДОСТУП ЗАБЛОКИРОВАН!"
        __________ = p.fromisoformat(_________)
        if p.now() > __________:
            return False, f"⏰ ПОДПИСКА ИСТЕКЛА {__________.strftime('%d.%m.%Y')}!"
        self.__.execute('UPDATE users SET last_active = ? WHERE hwid = ?', (___ .____(p.now().isoformat()), __))
        self._.commit()
        return True, ________
    def ________________(self):
        self.__________()
        return True
    def _________________(self):
        _ = self.__.execute('SELECT username, is_admin, is_banned, expires_at, hwid, saved_key FROM users ORDER BY is_admin DESC').fetchall()
        __ = []
        for ___ in _:
            ____, _____, ______, _______, ________, ________ = ___
            __.append((___ ._____(____), _____, ______, ___ ._____(_______), ___ ._____(________), ___ ._____(________) if ________ else None))
        return __
    def __________________(self):
        _ = self.__.execute('SELECT key_text, created_at, expires_at, used_by, used_hwid, is_used FROM license_keys ORDER BY created_at DESC').fetchall()
        __ = []
        for ___ in _:
            ____, _____, ______, _______, ________, _________ = ___
            __.append((___ ._____(____), ___ ._____(_____), ___ ._____(______), ___ ._____(_______) if _______ else None, ___ ._____(________) if ________ else None, _________))
        return __
    def ___________________(self, _, __=1):
        ___ = (p.now() + q(days=30 * __)).isoformat()
        ____ = ___ .____(_)
        _____ = ___ .____(___)
        ______ = self.__.execute('SELECT * FROM users WHERE username = ?', (____,)).fetchone()
        if ______:
            self.__.execute('UPDATE users SET expires_at = ?, is_banned = 0 WHERE username = ?', 
                           (_____, ____))
        else:
            self.__.execute('INSERT INTO users (username, hwid, created_at, expires_at) VALUES (?, ?, ?, ?)',
                           (____, ___ .____(f"MANUAL_{j.uuid4().hex[:8]}"), ___ .____(p.now().isoformat()), _____))
        self._.commit()
        return True, f"✅ ДОСТУП ВЫДАН {_} НА {__} МЕСЯЦЕВ!"
    def ____________________(self, _):
        self.__.execute('UPDATE users SET is_banned = 1 WHERE username = ?', (___ .____(_),))
        self._.commit()
        return True
    def _____________________(self, _):
        self.__.execute('UPDATE users SET is_banned = 0 WHERE username = ?', (___ .____(_),))
        self._.commit()
        return True
    def ______________________(self, _, __=1):
        ___ = self.__.execute('SELECT expires_at FROM users WHERE username = ?', (___ .____(_),)).fetchone()
        if ___:
            ____ = ___[0]
            _____ = ___ ._____(____)
            ______ = p.fromisoformat(_____) + q(days=30 * __)
            self.__.execute('UPDATE users SET expires_at = ? WHERE username = ?', 
                           (___ .____(______.isoformat()), ___ .____(_)))
            self._.commit()
            return True, f"✅ ПРОДЛЕН ДО {______.strftime('%d.%m.%Y')}!"
        return False, "❌ ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН!"

_ = ______()

def _______():
    try:
        o.windll.user32.ShowWindow(o.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

_________ = [
    _.__('я твою мать в жопу ебал пока ты тут сопли свои распускал а ты сынок шлюхи на меня рот открыл'),
    _.__('я твою мать нахуй послал и она там осталась а ты гандон сраный тут мне перечить вздумал'),
    _.__('я твою мать расчленил нахуй и по кускам разбросал а ты чурка ебаный на меня пасть открываешь'),
    _.__('я твоего отца отпиздил ногами и хуем пронзил насквозь а ты хуесос ебаный тут мне пиздишь'),
    _.__('я твоего батю своим членом насадил как шашлык а ты сынок шалавы тут мне слова поперек сказать пытаешься'),
    _.__('я твоего отца в гробу перевернул своим хуем и он там от стыда сгорел а ты педик гнилой'),
    _.__('я твою сестру в жопу трахал пока ты тут пиздел а она сказала что ты хуже меня во всем'),
    _.__('я твою сестру за волосы таскал и в жопу ебал пока она не поняла кто тут главный'),
    _.__('я твою сестру нахуй выебал и она теперь моя потому что ты ничтожество полное'),
    _.__('я твою бабку своей залупой по стенке размазал и она теперь как картина висит'),
    _.__('я твою бабку в гробу трахнул и она там от стыда перевернулась два раза а ты хач ебаный'),
    _.__('я твою бабку нахуй послал и она там осталась потому что старой уже некуда деваться было'),
    _.__('я твою мать и сестру твою в жопу ебал а ты пидор конченный на моём хуе сидишь'),
    _.__('я твоего отца и деда твоего расчленил нахуй а ты сын шлюхи ебаный тут мне перечить вздумал'),
    _.__('я твою родню всю вырезал нахуй и по ветру развеял а ты уебан конченный на меня пасть открываешь'),
    _.__('я тебя своим хуем как битой стальной отпизжу так что ты молиться будешь чтоб я тебя больше не трогал'),
    _.__('я тебя просто нахуй прожгу насквозь своим божественным членом все твои хлипкие органы будут прогорать'),
    _.__('от моего хуя идет свет такой что даже твои очки тебя не защитят я тебя просто нахуй ослеплю'),
    _.__('ты как собака нахуй лаешь а я тебя как щенка за шкирку возьму и в окно выкину нахуй'),
    _.__('ты как свинья жирная тут хрюкаешь а я тебя на шашлык пущу и съем без соли'),
    _.__('ты как таракан ебаный ползаешь под моими ногами и я тебя раздавлю как букашку'),
    _.__('я бог а ты просто жалкий червяк я тебя ногтем раздавлю и даже не замечу этого'),
    _.__('мой хуй сияет ярче солнца и ты просто ослепнешь когда я его достану из штанов'),
    _.__('от моего хуя идет сила такая что ты просто рассыплешься в прах и тебя ветром развеет нахуй'),
]

__________ = []
__________ = _________.copy()

def ___________():
    global __________, __________
    if not __________:
        __________ = _________.copy()
        __________ = []
    _ = c.choice(__________)
    __________.remove(_)
    __________.append(_)
    return _

def ____________():
    _ = ___________()
    _ = n.sub(r'[.,!?;:()"\']', '', _)
    __ = _.split()
    ___ = settings.get('banned_words', [])
    __ = [_ for _ in __ if _ not in ___]
    if not __:
        __ = ['ты', 'хуесос', 'блять']
    return __

_____________ = False
______________ = None
_______________ = 0
________________ = False
_________________ = 0
__________________ = None
___________________ = None
____________________ = 0.035
_____________________ = {}

def ______________________():
    global _____________ , _______________, ________________, ____________________, _________________, __________________
    _____________ = False
    _______________ = 0
    _________________ = 0
    __________________ = g.time()
    while not _____________:
        if ________________:
            g.sleep(0.1)
            continue
        _ = ____________()
        for __ in _:
            if _____________:
                return
            if ________________:
                break
            try:
                keyboard.write(__)
                g.sleep(____________________)
                keyboard.press_and_release('enter')
                g.sleep(_____________________.get('pause_between_messages', 0.01))
                _______________ += 1
                _________________ += 1
                if ___________________:
                    ___________________.update_counters()
            except:
                pass

def _______________________():
    global _____________ , ______________
    if ______________ and ______________.is_alive():
        return
    _____________ = False
    ______________ = m.Thread(target=______________________)
    ______________.daemon = True
    ______________.start()
    if ___________________:
        ___________________.update_ui_state()

def ________________________():
    global _____________
    _____________ = True
    if ___________________:
        ___________________.update_ui_state()

def _________________________():
    global ________________
    ________________ = not ________________
    if ___________________:
        ___________________.update_ui_state()
    return ________________

class __________________________ (u.Button):
    def __init__(self, _, **__):
        super().__init__(_, **__)
        self.config(relief=u.FLAT, borderwidth=0, font=("Segoe UI", 10, "bold"), cursor="hand2")
        self._ = self['bg']
        self.__ = self['fg']
        self.bind('<Enter>', self.___)
        self.bind('<Leave>', self.____)
        self.bind('<Button-1>', self._____)
    def ___(self, _):
        self.config(bg=self['bg'], fg=self['fg'])
    def ____(self, _):
        self.config(bg=self._, fg=self.__)
    def _____(self, _):
        self.config(relief=u.SUNKEN)
        self.after(100, lambda: self.config(relief=u.FLAT))

class ___________________________:
    def __init__(self):
        self._ = u.Tk()
        self._.title(f"🔐 АКТИВАЦИЯ | {_______}")
        self._.geometry("600x580")
        self._.configure(bg=COLORS['bg'])
        self._.resizable(False, False)
        self._.protocol("WM_DELETE_WINDOW", e.exit)
        _ = u.Frame(self._, bg=COLORS['shadow'], width=580, height=560)
        _.place(x=10, y=10)
        __ = u.Frame(self._, bg=COLORS['bg2'], width=580, height=560)
        __.place(x=10, y=10)
        ___ = u.Frame(__, bg=COLORS['gradient_start'], height=4)
        ___.pack(fill=u.X, padx=0, pady=0)
        ____ = u.Frame(__, bg=COLORS['bg2'])
        ____.pack(fill=u.X, padx=30, pady=(20,5))
        u.Label(____, text=f"🔥 {_______}", font=("Segoe UI", 22, "bold"), bg=COLORS['bg2'], fg=COLORS['gold']).pack()
        u.Label(____, text="🔐 АКТИВАЦИЯ ПРОГРАММЫ", font=("Segoe UI", 12), bg=COLORS['bg2'], fg=COLORS['text2']).pack()
        _____ = u.Frame(__, bg=COLORS['bg3'])
        _____.pack(pady=10, padx=30, fill=u.X)
        _____.config(height=80)
        _____.pack_propagate(False)
        ______ = u.Frame(_____, bg=COLORS['bg3'])
        ______.pack(fill=u.BOTH, padx=15, pady=10)
        u.Label(______, text=f"💻 Компьютер: {_____.___()}", bg=COLORS['bg3'], fg=COLORS['text'], font=("Segoe UI", 11)).pack(anchor='w')
        u.Label(______, text=f"🆔 HWID: {_____.______()[:24]}...", bg=COLORS['bg3'], fg=COLORS['text2'], font=("Segoe UI", 9)).pack(anchor='w')
        _______ = u.Frame(__, bg=COLORS['bg2'])
        _______.pack(pady=15, padx=30, fill=u.BOTH, expand=True)
        u.Label(_______, text="⚡ КУПИ ДОСТУП ⚡", font=("Segoe UI", 20, "bold"), bg=COLORS['bg2'], fg=COLORS['neon_orange']).pack()
        u.Label(_______, text="У ВЛАДЕЛЬЦА", font=("Segoe UI", 12), bg=COLORS['bg2'], fg=COLORS['text']).pack()
        ________ = u.Frame(_______, bg=COLORS['bg4'])
        ________.pack(pady=8, padx=20, fill=u.X)
        ________.config(height=50)
        ________.pack_propagate(False)
        _________.pack(fill=u.BOTH, padx=10, pady=5)
        u.Label(_________, text="🔥 @flidges 🔥", font=("Segoe UI", 16, "bold"), bg=COLORS['bg4'], fg=COLORS['gold']).pack(side=u.LEFT)
        u.Label(_________, text="📩 Telegram", font=("Segoe UI", 10), bg=COLORS['bg4'], fg=COLORS['neon_blue']).pack(side=u.RIGHT)
        u.Label(_______, text=________, font=("Segoe UI", 12, "bold"), bg=COLORS['bg2'], fg=COLORS['neon']).pack(pady=5)
        __________ = u.Frame(_______, bg=COLORS['text3'], height=1, width=300)
        __________.pack(pady=10)
        ___________ = u.Frame(_______, bg=COLORS['bg2'])
        ___________.pack(pady=10, fill=u.X)
        u.Label(___________, text="Или введите ключ активации:", bg=COLORS['bg2'], fg=COLORS['text2'], font=("Segoe UI", 10)).pack(anchor='w')
        ____________ = u.Frame(___________, bg=COLORS['bg2'])
        ____________.pack(fill=u.X, pady=5)
        self.__ = u.Entry(____________, bg=COLORS['bg3'], fg=COLORS['neon'], font=("Segoe UI", 14), relief=u.FLAT, borderwidth=2, insertbackground=COLORS['text'])
        self.__.pack(side=u.LEFT, fill=u.X, expand=True, padx=(0,10))
        self.__.bind('<Return>', lambda _: self._())
        self._ = u.Button(____________, text="✅ АКТИВИРОВАТЬ", command=self._, bg=COLORS['gradient_start'], fg='white', font=("Segoe UI", 10, "bold"), relief=u.FLAT, cursor="hand2", padx=15, pady=8)
        self._.pack(side=u.RIGHT)
        self.___ = u.Frame(_______, bg=COLORS['bg2'], height=50)
        self.___.pack(fill=u.X, pady=5)
        self.___.pack_propagate(False)
        self.____ = u.Label(self.___, text="", bg=COLORS['bg2'], fg=COLORS['danger'], font=("Segoe UI", 11, "bold"))
        self.____.pack(fill=u.BOTH, expand=True)
        _____ = u.Frame(__, bg=COLORS['bg2'])
        _____.pack(side=u.BOTTOM, fill=u.X, pady=10)
        u.Label(_____, text=f"© 2026 {___} | Версия {_____}", bg=COLORS['bg2'], fg=COLORS['text3'], font=("Segoe UI", 8)).pack()
        self._.mainloop()
    def _(self):
        _ = self.__.get().strip()
        if not _:
            self.____.config(text="❌ ВВЕДИТЕ КЛЮЧ!", fg=COLORS['danger'])
            return
        __, ___ = _.activate_key(_)
        if __:
            self.____.config(text="✅ " + ___, fg=COLORS['success'])
            self._.config(bg=COLORS['success'], text="✅ АКТИВИРОВАНО!")
            self._.after(1500, self.__)
        else:
            self.____.config(text="❌ " + ___, fg=COLORS['danger'])
    def __(self):
        self._.destroy()
        ____________________________()

# ============================================================
# ЗАПУСК
# ============================================================

def ____________________________():
    _______()
    _ = u.Tk()
    _.title(f"🔥 {_______} | {___}")
    _.geometry("800x650")
    _.configure(bg=COLORS['bg'])
    _.minsize(700, 550)
    _.resizable(True, True)
    __ = _____________________________(_)
    _.mainloop()

class _____________________________:
    def __init__(self, _):
        global ___________________
        ___________________ = self
        self._ = _
        self._.title(f"🔥 {_______} | {___}")
        self._.geometry("800x650")
        self._.configure(bg=COLORS['bg'])
        self._.minsize(700, 550)
        self._.resizable(True, True)
        self.__ = __________________________(self._)
        self.___ = False
        self.____()
        self._____()
        self.______()
    def ____(self):
        _ = u.Frame(self._, bg=COLORS['bg'])
        _.pack(fill=u.BOTH, expand=True, padx=15, pady=15)
        __ = u.Frame(_, bg=COLORS['bg2'], height=90)
        __.pack(fill=u.X, padx=0, pady=0)
        __.pack_propagate(False)
        ___ = u.Frame(__, bg=COLORS['bg2'])
        ___.pack(fill=u.BOTH, padx=20, pady=10)
        u.Label(___, text=f"🔥 {_______}", font=("Segoe UI", 28, "bold"), bg=COLORS['bg2'], fg=COLORS['gold']).pack()
        u.Label(___, text=____, font=("Segoe UI", 11), bg=COLORS['bg2'], fg=COLORS['neon_orange']).pack()
        ____ = u.Frame(_, bg=COLORS['bg'])
        ____.pack(fill=u.X, padx=0, pady=5)
        self._____ = __________________________(____, text="⚙️ АДМИН-ПАНЕЛЬ (F6)", command=self._______, bg=COLORS['accent'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), padx=14, pady=5)
        self._____.pack(side=u.LEFT)
        self.______ = __________________________(____, text="⛶ ПОЛНЫЙ ЭКРАН (F11)", command=self.________, bg=COLORS['bg4'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), padx=14, pady=5)
        self.______.pack(side=u.RIGHT)
        self._______ = __________________________(____, text="🚪 ВЫЙТИ ИЗ АККАУНТА", command=self._________, bg=COLORS['danger'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), padx=14, pady=5)
        self._______.pack(side=u.RIGHT, padx=5)
        __________ = u.Frame(_, bg=COLORS['bg'])
        __________.pack(pady=5)
        self.___________ = u.Label(__________, text="⏸️ Ожидание...", bg=COLORS['bg'], fg=COLORS['warning'], font=("Segoe UI", 13, "bold"))
        self.___________.pack(side=u.LEFT, padx=10)
        self.____________ = u.Label(__________, text="📨 0", bg=COLORS['bg'], fg=COLORS['neon'], font=("Segoe UI", 13, "bold"))
        self.____________.pack(side=u.LEFT, padx=10)
        self._____________ = v.ScrolledText(_, height=9, bg=COLORS['bg3'], fg=COLORS['text'], insertbackground='white', font=("Segoe UI", 10), relief=u.FLAT, borderwidth=2, padx=15, pady=15)
        self._____________.pack(padx=0, pady=8, fill=u.BOTH, expand=True)
        self._____________.insert("1.0", f"""🔥 {_______}

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
✅ {____}
✅ {______}""")
        self._____________.config(state=u.DISABLED)
        ______________ = u.Frame(_, bg=COLORS['bg'])
        ______________.pack(pady=8)
        self._______________ = __________________________(______________, text="🤖 СТАРТ (F3)", command=self.________________, bg=COLORS['success'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), width=16, padx=5, pady=8)
        self._______________.pack(side=u.LEFT, padx=5)
        self.________________ = __________________________(______________, text="🛑 СТОП (F4)", command=self._________________, bg=COLORS['danger'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), width=16, padx=5, pady=8)
        self.________________.pack(side=u.LEFT, padx=5)
        self.__________________ = __________________________(______________, text="⏸️ ПАУЗА (F5)", command=self.__________________, bg=COLORS['accent'], fg=COLORS['text'], font=("Segoe UI", 10, "bold"), width=16, padx=5, pady=8)
        self.__________________.pack(side=u.LEFT, padx=5)
        ___________________ = u.Frame(_, bg=COLORS['bg'])
        ___________________.pack(pady=5)
        u.Label(___________________, text="F3-СТАРТ | F4-СТОП | F5-ПАУЗА | F6-АДМИН | F9-ВЫХОД | F11-ПОЛНЫЙ ЭКРАН", bg=COLORS['bg'], fg=COLORS['text2'], font=("Segoe UI", 9)).pack()
        u.Label(___________________, text=______, bg=COLORS['bg'], fg=COLORS['pink'], font=("Segoe UI", 10, "bold")).pack()
    def _________(self):
        if x.askyesno("Выход из аккаунта", "Вы уверены, что хотите выйти из аккаунта?\nКлюч будет удалён, и вам нужно будет ввести его заново."):
            _.________________()
            self._.destroy()
            ___________________________()
    def ________(self):
        self.___ = not self.___
        self._.attributes('-fullscreen', self.___)
        if self.___:
            self.______.config(text="⛶ ОКОННЫЙ РЕЖИМ (F11)", bg=COLORS['warning'])
        else:
            self.______.config(text="⛶ ПОЛНЫЙ ЭКРАН (F11)", bg=COLORS['bg4'])
    def _____(self):
        try:
            keyboard.add_hotkey('f3', self.________________)
            keyboard.add_hotkey('f4', self._________________)
            keyboard.add_hotkey('f5', self.__________________)
            keyboard.add_hotkey('f6', self._______)
            keyboard.add_hotkey('f9', self.___________________)
            keyboard.add_hotkey('f11', self.________)
        except: pass
    def _______(self):
        _ = _.__.execute('SELECT is_admin FROM users WHERE hwid = ?', (___ .____(_____.______()),)).fetchone()
        if _ and _[0]:
            self.__.toggle()
        else:
            x.showwarning("Доступ запрещен", "Только для администраторов!")
    def __________(self):
        try:
            self.____________.config(text=f"📨 {_______________}")
        except: pass
    def ___________ (self):
        try:
            if ________________:
                self.___________.config(text="⏸️ ПАУЗА", fg=COLORS['warning'])
                self.__________________.config(text="▶️ ВОЗОБНОВИТЬ (F5)", bg=COLORS['warning'])
            elif not _____________ and ______________ and ______________.is_alive():
                self.___________.config(text="🧠 ГЕНЕРАЦИЯ", fg=COLORS['success'])
                self._______________.config(bg=COLORS['bg4'], text="🧠 РАБОТАЕТ...")
                self.__________________.config(text="⏸️ ПАУЗА (F5)", bg=COLORS['accent'])
            else:
                self.___________.config(text="⏸️ Остановлено", fg=COLORS['text2'])
                self._______________.config(bg=COLORS['success'], text="🤖 СТАРТ (F3)")
                self.__________________.config(text="⏸️ ПАУЗА (F5)", bg=COLORS['accent'])
        except: pass
    def ______(self):
        self.___________()
        self.____________.config(text=f"📨 {_______________}")
        self._.after(500, self.______)
    def ________________(self):
        _______________________()
        self.___________()
    def _________________(self):
        ________________________()
        self.___________()
    def __________________(self):
        _________________________()
        self.___________()
    def ___________________(self):
        ________________________()
        self._.quit()
        self._.destroy()
        e.exit()

if __name__ == "__main__":
    _______()
    _, __ = _.______________()
    if _:
        ____________________________()
    else:
        _, __ = _._______________()
        if _:
            ____________________________()
        else:
            ___________________________()
