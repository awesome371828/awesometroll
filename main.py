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

try:ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
except:pass

_0=lambda:hashlib.sha256((platform.node()+platform.processor()+platform.machine()+str(os.cpu_count())+os.environ.get('COMPUTERNAME','')+os.environ.get('PROCESSOR_IDENTIFIER','')).encode()).hexdigest()[:10]
_1=_0()

_2="https://yzhgcdnjuvfhcvwedgga"
_3=".supabase.co"
_4=_2+_3

_5="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
_6=".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6aGdjZG5qdXZmaGN3dmVkZ2dhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY0NjExNTgsImV4cCI6MjEwMjAzNzE1OH0"
_7=".ccCiaKPnpwjg69PC90qtPDOIWn5PezGxKERJtdWUB_I"
_8=_5+_6+_7

class _9:
    @classmethod
    def _(cls,d):
        if d is None:return None
        try:
            if isinstance(d,str):d=d.encode()
            return Fernet(base64.urlsafe_b64encode(hashlib.sha512(_1.encode()).digest()[:32])).encrypt(d)
        except:return d
    @classmethod
    def __(cls,e):
        if e is None:return None
        try:
            if isinstance(e,str):e=e.encode()
            return Fernet(base64.urlsafe_b64encode(hashlib.sha512(_1.encode()).digest()[:32])).decrypt(e).decode()
        except:return e

_10=_9._
_11=_9.__

class _12:
    @classmethod
    def _(cls,m,e,d=None):
        h={"apikey":_8,"Authorization":f"Bearer {_8}","Content-Type":"application/json"}
        try:
            if m=="GET":r=requests.get(f"{_4}/rest/v1/{e}",headers=h)
            elif m=="POST":r=requests.post(f"{_4}/rest/v1/{e}",headers=h,json=d)
            elif m=="PATCH":r=requests.patch(f"{_4}/rest/v1/{e}",headers=h,json=d)
            return r.json() if r.ok else None
        except:return None
    @classmethod
    def __(cls):return cls._("GET","users?order=id.desc")
    @classmethod
    def ___(cls,u,h,e,s,o=0,a=0):return cls._("POST","users",{"username":u,"hwid":h,"is_owner":o,"is_admin":a,"expires_at":e,"saved_key":s})
    @classmethod
    def ____(cls):return cls._("GET","license_keys?order=id.desc")
    @classmethod
    def _____(cls,k,e,o):return cls._("POST","license_keys",{"key_text":k,"expires_at":e,"owner_hwid":o,"is_used":0})
    @classmethod
    def ______(cls,k,u,h):return cls._("PATCH",f"license_keys?key_text=eq.{k}",{"used_by":u,"used_hwid":h,"used_at":datetime.now().isoformat(),"is_used":1})

_13=lambda:os.path.dirname(sys.executable)if getattr(sys,'frozen',False)else os.path.dirname(os.path.abspath(__file__))
_14=_13()
_15=os.path.join(_14,"troll_users.db")
_16=os.path.join(_14,"license.key")

class _17:
    def __init__(s):
        s._18=sqlite3.connect(_15)
        s._19=s._18.cursor()
        s._20()
    def _20(s):
        s._19.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,hwid TEXT UNIQUE,is_owner INT DEFAULT 0,is_admin INT DEFAULT 0,is_banned INT DEFAULT 0,created_at TEXT,expires_at TEXT,saved_key TEXT)')
        s._19.execute('CREATE TABLE IF NOT EXISTS keys (key_text TEXT UNIQUE,created_at TEXT,expires_at TEXT,used_by TEXT,used_hwid TEXT,is_used INT DEFAULT 0,owner_hwid TEXT)')
        s._18.commit()
    def _21(s):
        try:
            _22=uuid.getnode()
            return ':'.join(('%012x'%_22)[_23:_23+2]for _23 in range(0,12,2))
        except:return "unknown"
    def _24(s):
        try:return os.environ.get('USERNAME','unknown')
        except:return "unknown"
    def _25(s):
        try:return os.environ.get('COMPUTERNAME','unknown')
        except:return "unknown"
    def _26(s):
        try:
            if platform.system()=='Windows':
                _27=subprocess.run(['wmic','diskdrive','get','serialnumber'],capture_output=True,text=True)
                _28=_27.stdout.strip().split('\n')
                if len(_28)>1:return _28[1].strip()
            return "unknown"
        except:return "unknown"
    def _29(s):
        try:
            if platform.system()=='Windows':
                _30=subprocess.run(['wmic','cpu','get','processorid'],capture_output=True,text=True)
                _31=_30.stdout.strip().split('\n')
                if len(_31)>1:return _31[1].strip()
            return "unknown"
        except:return "unknown"
    def _32(s):
        _33=s._21()+s._24()+s._25()+s._26()+s._29()+platform.processor()+platform.machine()
        return hashlib.sha512(_10(_33)).hexdigest()[:64]
    def _34(s,_35):return _35==_1
    def _36(s,_37):
        with open(_16,'w')as _38:_38.write(base64.b64encode(_10(_37)).decode())
    def _39(s):
        if os.path.exists(_16):
            try:
                with open(_16,'r')as _40:return _11(base64.b64decode(_40.read().strip().encode()))
            except:return None
        return None
    def _41(s):
        if os.path.exists(_16):os.remove(_16)
    def _42(s,_43=1,_44=None):
        _45=_44 or hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()[:12].upper()
        _46=(datetime.now()+timedelta(days=30*_43)).isoformat()
        _47=s._32()
        try:
            s._19.execute('INSERT INTO keys (key_text,created_at,expires_at,is_used,owner_hwid) VALUES (?,?,?,0,?)',(_10(_45),_10(datetime.now().isoformat()),_10(_46),_10(_47)))
            s._18.commit()
            try:_12._____(_45,_46,_47)
            except:pass
            return True,_45
        except:return False,None
    def _48(s,_49):
        s._19.execute('DELETE FROM keys WHERE key_text=?',(_10(_49),))
        s._18.commit()
        return True
    def _50(s,_51,_52=True):
        _53=s._32()
        _54=s._24()
        _55=_51.upper()
        if s._34(_55):
            _56=_10(_53)
            _57=_10(_54)
            _58=_10("2099-12-31T23:59:59")
            _59=_10(_55)
            _60=s._19.execute('SELECT * FROM users WHERE hwid=?',(_56,)).fetchone()
            if _60:s._19.execute('UPDATE users SET username=?,is_owner=1,is_admin=1,is_banned=0,expires_at=?,saved_key=? WHERE hwid=?',(_57,_58,_59,_56))
            else:s._19.execute('INSERT INTO users (username,hwid,is_owner,is_admin,created_at,expires_at,saved_key) VALUES (?,?,1,1,?,?,?)',(_57,_56,_10(datetime.now().isoformat()),_58,_59))
            s._18.commit()
            if _52:s._36(_55)
            try:_12.___(_54,_53,"2099-12-31T23:59:59",_55,1,1)
            except:pass
            return True,"👑 ДОБРО ПОЖАЛОВАТЬ, ОВНЕР!"
        _61=s._19.execute('SELECT key_text,expires_at,is_used,used_hwid,owner_hwid FROM keys WHERE key_text=?',(_10(_55),)).fetchone()
        if not _61:return False,"❌ НЕВЕРНЫЙ КЛЮЧ!"
        _62,_63,_64,_65,_66=_61
        _67=_11(_63)
        _68=_11(_65)if _65 else None
        _69=_11(_66)if _66 else None
        if _69 and _69!=_53:return False,"❌ ЭТОТ КЛЮЧ НЕ ДЛЯ ТВОЕГО КОМПЬЮТЕРА!"
        if _64 and _68 and _68!=_53:return False,"❌ КЛЮЧ УЖЕ АКТИВИРОВАН НА ДРУГОМ КОМПЬЮТЕРЕ!"
        if _64 and _68==_53:
            _70=datetime.fromisoformat(_67)
            if datetime.now()>_70:return False,f"❌ КЛЮЧ ИСТЕК {_70.strftime('%d.%m.%Y')}!"
            return True,f"✅ ДОСТУП УЖЕ АКТИВИРОВАН ДО {_70.strftime('%d.%m.%Y')}!"
        _70=datetime.fromisoformat(_67)
        if datetime.now()>_70:return False,f"❌ КЛЮЧ ИСТЕК {_70.strftime('%d.%m.%Y')}!"
        s._19.execute('UPDATE keys SET used_by=?,used_hwid=?,is_used=1 WHERE key_text=?',(_10(_54),_10(_53),_10(_55)))
        _71=s._19.execute('SELECT * FROM users WHERE hwid=?',(_10(_53),)).fetchone()
        if _71:s._19.execute('UPDATE users SET username=?,expires_at=?,is_banned=0,saved_key=? WHERE hwid=?',(_10(_54),_63,_10(_55),_10(_53)))
        else:s._19.execute('INSERT INTO users (username,hwid,created_at,expires_at,saved_key) VALUES (?,?,?,?,?)',(_10(_54),_10(_53),_10(datetime.now().isoformat()),_63,_10(_55)))
        s._18.commit()
        if _52:s._36(_55)
        try:
            _12.___(_54,_53,_67,_55,0,0)
            _12.______(_55,_54,_53)
        except:pass
        return True,f"✅ ВЕРНО! ДОСТУП ДО {_70.strftime('%d.%m.%Y')}!"
    def _72(s):
        _73=s._39()
        if _73:
            _74,_75=s._50(_73,False)
            if _74:return True,_75
        return False,None
    def _76(s):
        _77=s._32()
        _78=_10(_77)
        _79=s._19.execute('SELECT username,is_owner,is_admin,is_banned,expires_at FROM users WHERE hwid=?',(_78,)).fetchone()
        if not _79:return False,"🔑 ТРЕБУЕТСЯ АКТИВАЦИЯ!"
        _80,_81,_82,_83,_84=_79
        _85=_11(_80)
        _86=_11(_84)
        if _83:return False,"🚫 ДОСТУП ЗАБЛОКИРОВАН!"
        _87=datetime.fromisoformat(_86)
        if datetime.now()>_87:return False,f"⏰ ПОДПИСКА ИСТЕКЛА {_87.strftime('%d.%m.%Y')}!"
        s._19.execute('UPDATE users SET last_active=? WHERE hwid=?',(_10(datetime.now().isoformat()),_78))
        s._18.commit()
        return True,_85
    def _88(s):
        _89=s._19.execute('SELECT username,is_owner,is_admin,is_banned,expires_at,hwid,saved_key FROM users ORDER BY is_owner DESC').fetchall()
        return [(_11(_90[0]),_90[1],_90[2],_90[3],_11(_90[4]),_11(_90[5]),_11(_90[6])if _90[6]else None)for _90 in _89]
    def _91(s):
        _92=s._19.execute('SELECT key_text,created_at,expires_at,used_by,used_hwid,is_used,owner_hwid FROM keys ORDER BY created_at DESC').fetchall()
        return [(_11(_93[0]),_11(_93[1]),_11(_93[2]),_11(_93[3])if _93[3]else None,_11(_93[4])if _93[4]else None,_93[5],_11(_93[6])if _93[6]else None)for _93 in _92]
    def _94(s,_95,_96=1):
        _97=(datetime.now()+timedelta(days=30*_96)).isoformat()
        _98=_10(_95)
        _99=_10(_97)
        _100=s._19.execute('SELECT * FROM users WHERE username=?',(_98,)).fetchone()
        if _100:s._19.execute('UPDATE users SET expires_at=?,is_banned=0 WHERE username=?',(_99,_98))
        else:s._19.execute('INSERT INTO users (username,hwid,created_at,expires_at) VALUES (?,?,?,?)',(_98,_10(f"MANUAL_{uuid.uuid4().hex[:8]}"),_10(datetime.now().isoformat()),_99))
        s._18.commit()
        return True,f"✅ ДОСТУП ВЫДАН {_95} НА {_96} МЕСЯЦЕВ!"
    def _101(s,_102):
        s._19.execute('UPDATE users SET is_banned=1 WHERE username=?',(_10(_102),))
        s._18.commit()
        return True
    def _103(s,_104):
        s._19.execute('UPDATE users SET is_banned=0 WHERE username=?',(_10(_104),))
        s._18.commit()
        return True
    def _105(s,_106,_107=1):
        _108=s._19.execute('SELECT expires_at FROM users WHERE username=?',(_10(_106),)).fetchone()
        if _108:
            _109=_11(_108[0])
            _110=datetime.fromisoformat(_109)+timedelta(days=30*_107)
            s._19.execute('UPDATE users SET expires_at=? WHERE username=?',(_10(_110.isoformat()),_10(_106)))
            s._18.commit()
            return True,f"✅ ПРОДЛЕН ДО {_110.strftime('%d.%m.%Y')}!"
        return False,"❌ ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН!"

_111=_17()

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

_112=[];_113=INSULT_TEMPLATES.copy()
def _114():
    global _112,_113
    if not _113:
        _113=INSULT_TEMPLATES.copy()
        _112=[]
    _115=random.choice(_113)
    _113.remove(_115)
    _112.append(_115)
    return _115
def _116():
    _117=_114()
    _117=re.sub(r'[.,!?;:()"\']','',_117)
    _118=_117.split()
    _119=settings.get('banned_words',[])
    _118=[x for x in _118 if x not in _119]
    if not _118:_118=['ты','хуесос','блять']
    return _118

_120=False
_121=None
_122=0
_123=False
_124=0
_125=None
_126=None
_127=0.035
settings={}

def _128():
    global _120,_122,_123,_127,_124,_125
    _120=False
    _122=0
    _124=0
    _125=time.time()
    while not _120:
        if _123:
            time.sleep(0.1)
            continue
        _129=_116()
        for _130 in _129:
            if _120:return
            if _123:break
            try:
                keyboard.write(_130)
                time.sleep(_127)
                keyboard.press_and_release('enter')
                time.sleep(settings.get('pause_between_messages',0.01))
                _122+=1
                _124+=1
                if _126:_126.uc()
            except:pass
def _131():
    global _120,_121
    if _121 and _121.is_alive():return
    _120=False
    _121=threading.Thread(target=_128)
    _121.daemon=True
    _121.start()
    if _126:_126.uis()
def _132():
    global _120
    _120=True
    if _126:_126.uis()
def _133():
    global _123
    _123=not _123
    if _126:_126.uis()
    return _123

class _134(tk.Button):
    def __init__(s,master,**kwargs):
        super().__init__(master,**kwargs)
        s.config(relief=tk.FLAT,borderwidth=0,font=("Segoe UI",10,"bold"),cursor="hand2")
        s._135=s['bg']
        s._136=s['fg']
        s.bind('<Enter>',s._137)
        s.bind('<Leave>',s._138)
        s.bind('<Button-1>',s._139)
    def _137(s,e):s.config(bg=s['bg'],fg=s['fg'])
    def _138(s,e):s.config(bg=s._135,fg=s._136)
    def _139(s,e):s.config(relief=tk.SUNKEN);s.after(100,lambda:s.config(relief=tk.FLAT))

class _140:
    def __init__(s,canvas,num=150):
        s.canvas=canvas
        s.stars=[]
        s.running=True
        s.num=num
        for _ in range(num):
            _141=random.randint(0,2000)
            _142=random.randint(0,2000)
            _143=random.uniform(0.5,2.5)
            _144=random.uniform(0.005,0.03)
            _145=random.randint(50,255)
            _146=random.uniform(0,6.28)
            _147=random.uniform(-0.3,0.3)
            _148=random.uniform(-0.3,0.3)
            _149=random.choice(['blue','white','gold','pink'])
            s.stars.append({'x':_141,'y':_142,'size':_143,'speed':_144,'brightness':_145,'phase':_146,'dx':_147,'dy':_148,'color':_149})
    def update(s):
        if not s.running:return
        s.canvas.delete("star")
        _150=s.canvas.winfo_width()or 900
        _151=s.canvas.winfo_height()or 700
        for _152 in s.stars:
            _152['x']+=_152['dx']
            _152['y']+=_152['dy']
            _152['phase']+=_152['speed']
            if _152['x']<0:_152['x']=_150
            if _152['x']>_150:_152['x']=0
            if _152['y']<0:_152['y']=_151
            if _152['y']>_151:_152['y']=0
            _153=int(_152['brightness']*(0.6+0.4*(_152['phase']%1)))
            _154={'blue':f"#{min(255,_153):02x}{min(255,_153//3):02x}{min(255,_153):02x}",'white':f"#{min(255,_153):02x}{min(255,_153):02x}{min(255,_153):02x}",'gold':f"#{min(255,_153):02x}{min(255,_153//2):02x}{min(255,_153//4):02x}",'pink':f"#{min(255,_153):02x}{min(255,_153//3):02x}{min(255,_153//2):02x}"}
            _155=_154.get(_152['color'],f"#{min(255,_153):02x}{min(255,_153//2):02x}{min(255,_153):02x}")
            _156=_152['size']
            _157=_156*2
            s.canvas.create_oval(_152['x']-_157,_152['y']-_157,_152['x']+_157,_152['y']+_157,fill='',outline=_155,width=0.5,tags="star",stipple="gray50")
            s.canvas.create_oval(_152['x']-_156,_152['y']-_156,_152['x']+_156,_152['y']+_156,fill=_155,outline='',tags="star")
        s.canvas.after(50,s.update)
    def stop(s):s.running=False

class _158:
    def __init__(s):
        s.window=tk.Tk()
        s.window.title(f"🔐 АКТИВАЦИЯ | AWESOMETROLLING")
        s.window.geometry("600x650")
        s.window.configure(bg='#0a0e27')
        s.window.resizable(False,False)
        s.window.protocol("WM_DELETE_WINDOW",sys.exit)
        s.window.update_idletasks()
        _159=600;_160=650
        _161=(s.window.winfo_screenwidth()//2)-(_159//2)
        _162=(s.window.winfo_screenheight()//2)-(_160//2)
        s.window.geometry(f'{_159}x{_160}+{_161}+{_162}')
        s.canvas=tk.Canvas(s.window,width=600,height=650,bg='#0a0e27',highlightthickness=0)
        s.canvas.pack(fill=tk.BOTH,expand=True)
        s.stars=_140(s.canvas,100)
        s.stars.update()
        _163=tk.Frame(s.canvas,bg='#1a1f4a',width=580,height=600)
        _163.place(x=10,y=25)
        _164=tk.Frame(s.canvas,bg='#111638',width=580,height=600)
        _164.place(x=10,y=25)
        _165=tk.Frame(_164,bg='#6c5ce7',height=4)
        _165.pack(fill=tk.X,padx=0,pady=0)
        _166=tk.Frame(_164,bg='#111638')
        _166.pack(fill=tk.X,padx=30,pady=(20,5))
        tk.Label(_166,text="🔥 AWESOMETROLLING",font=("Segoe UI",26,"bold"),bg='#111638',fg='#ffd700').pack()
        tk.Label(_166,text="🔐 АКТИВАЦИЯ ПРОГРАММЫ",font=("Segoe UI",12),bg='#111638',fg='#dfe6e9').pack()
        _167=tk.Frame(_164,bg='#1a1f4a')
        _167.pack(pady=10,padx=30,fill=tk.X)
        _167.config(height=80)
        _167.pack_propagate(False)
        _168=tk.Frame(_167,bg='#1a1f4a')
        _168.pack(fill=tk.BOTH,padx=15,pady=10)
        tk.Label(_168,text=f"💻 Компьютер: {os.environ.get('USERNAME','unknown')}",bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",11)).pack(anchor='w')
        tk.Label(_168,text=f"🆔 HWID: {_111._32()[:24]}...",bg='#1a1f4a',fg='#b2bec3',font=("Segoe UI",9)).pack(anchor='w')
        _169=tk.Frame(_164,bg='#111638')
        _169.pack(pady=15,padx=30,fill=tk.BOTH,expand=True)
        tk.Label(_169,text="⚡ КУПИ ДОСТУП ⚡",font=("Segoe UI",20,"bold"),bg='#111638',fg='#ff6b35').pack()
        tk.Label(_169,text="У ВЛАДЕЛЬЦА",font=("Segoe UI",12),bg='#111638',fg='#dfe6e9').pack()
        _170=tk.Frame(_169,bg='#222860')
        _170.pack(pady=8,padx=20,fill=tk.X)
        _170.config(height=50)
        _170.pack_propagate(False)
        _171=tk.Frame(_170,bg='#222860')
        _171.pack(fill=tk.BOTH,padx=10,pady=5)
        tk.Label(_171,text="🔥 @flidges 🔥",font=("Segoe UI",16,"bold"),bg='#222860',fg='#ffd700').pack(side=tk.LEFT)
        tk.Label(_171,text="📩 Telegram",font=("Segoe UI",10),bg='#222860',fg='#4fc3f7').pack(side=tk.RIGHT)
        tk.Label(_169,text="💰 Цена - узнайте у @flidges",font=("Segoe UI",12,"bold"),bg='#111638',fg='#00ff88').pack(pady=5)
        _172=tk.Frame(_169,bg='#636e72',height=1,width=300)
        _172.pack(pady=10)
        _173=tk.Frame(_169,bg='#111638')
        _173.pack(pady=10,fill=tk.X)
        tk.Label(_173,text="Или введите ключ активации:",bg='#111638',fg='#b2bec3',font=("Segoe UI",10)).pack(anchor='w')
        _174=tk.Frame(_173,bg='#111638')
        _174.pack(fill=tk.X,pady=5)
        s.key_entry=tk.Entry(_174,bg='#1a1f4a',fg='#00ff88',font=("Segoe UI",14),relief=tk.FLAT,borderwidth=2,insertbackground='#dfe6e9')
        s.key_entry.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=(0,10))
        s.key_entry.bind('<Return>',lambda e:s._175())
        s.activate_btn=tk.Button(_174,text="✅ АКТИВИРОВАТЬ",command=s._175,bg='#6c5ce7',fg='white',font=("Segoe UI",10,"bold"),relief=tk.FLAT,cursor="hand2",padx=15,pady=8)
        s.activate_btn.pack(side=tk.RIGHT)
        s.status_frame=tk.Frame(_169,bg='#111638',height=50)
        s.status_frame.pack(fill=tk.X,pady=5)
        s.status_frame.pack_propagate(False)
        s.status_label=tk.Label(s.status_frame,text="",bg='#111638',fg='#e17055',font=("Segoe UI",11,"bold"))
        s.status_label.pack(fill=tk.BOTH,expand=True)
        _176=tk.Frame(_164,bg='#111638')
        _176.pack(side=tk.BOTTOM,fill=tk.X,pady=10)
        tk.Label(_176,text=f"© 2026 @flidges | Версия 3.0",bg='#111638',fg='#636e72',font=("Segoe UI",8)).pack()
        s.window.mainloop()
    def _175(s):
        _177=s.key_entry.get().strip()
        if not _177:
            s.status_label.config(text="❌ ВВЕДИТЕ КЛЮЧ!",fg='#e17055')
            return
        _178,_179=_111._50(_177)
        if _178:
            s.status_label.config(text="✅ "+_179,fg='#00b894')
            s.activate_btn.config(bg='#00b894',text="✅ АКТИВИРОВАНО!")
            s.window.after(1500,s._180)
        else:
            s.status_label.config(text="❌ "+_179,fg='#e17055')
    def _180(s):
        if s.stars:s.stars.stop()
        s.window.destroy()
        _181()

def _181():
    _182=tk.Tk()
    _182.title(f"🔥 AWESOMETROLLING | @flidges")
    _182.geometry("900x700")
    _182.configure(bg='#0a0e27')
    _182.minsize(850,650)
    _182.resizable(True,True)
    _182.update_idletasks()
    _183=900;_184=700
    _185=(_182.winfo_screenwidth()//2)-(_183//2)
    _186=(_182.winfo_screenheight()//2)-(_184//2)
    _182.geometry(f'{_183}x{_184}+{_185}+{_186}')
    _187=_188(_182)
    _182.mainloop()

class _188:
    def __init__(s,root):
        global _126
        _126=s
        s.root=root
        s.root.title(f"🔥 AWESOMETROLLING | @flidges")
        s.root.geometry("900x700")
        s.root.configure(bg='#0a0e27')
        s.root.minsize(850,650)
        s.root.resizable(True,True)
        _189=_111._32()
        s.is_admin=False
        _190=_111._39()
        if _190 and _111._34(_190):s.is_admin=True
        else:
            _191=_111._19.execute('SELECT is_admin,is_owner FROM users WHERE hwid=?',(_10(_189),)).fetchone()
            if _191 and (_191[0]==1 or _191[1]==1):s.is_admin=True
        s.canvas=tk.Canvas(s.root,bg='#0a0e27',highlightthickness=0)
        s.canvas.pack(fill=tk.BOTH,expand=True)
        s.stars=_140(s.canvas,150)
        s.stars.update()
        _192=tk.Frame(s.canvas,bg='#111638',bd=2,relief=tk.FLAT)
        _192.place(relx=0.5,rely=0.5,anchor=tk.CENTER,width=860,height=660)
        s.main_frame=_192
        _193=tk.Frame(_192,bg='#111638',height=80)
        _193.pack(fill=tk.X,padx=0,pady=0)
        _193.pack_propagate(False)
        _194=tk.Frame(_193,bg='#111638')
        _194.pack(fill=tk.BOTH,padx=20,pady=10)
        tk.Label(_194,text="🔥 AWESOMETROLLING",font=("Segoe UI",26,"bold"),bg='#111638',fg='#ffd700').pack(side=tk.LEFT)
        tk.Label(_194,text="✨ Создатель: awesome / tg @flidges ✨",font=("Segoe UI",10),bg='#111638',fg='#ff6b35').pack(side=tk.RIGHT)
        _195=tk.Frame(_192,bg='#0a0e27')
        _195.pack(fill=tk.X,padx=0,pady=5)
        s.admin_btn=_134(_195,text="⚙️ АДМИН-ПАНЕЛЬ (F6)",command=s._196,bg='#6c5ce7',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=14,pady=5)
        s.admin_btn.pack(side=tk.LEFT,padx=5)
        s.fs_btn=_134(_195,text="⛶ ПОЛНЫЙ ЭКРАН (F11)",command=s._197,bg='#222860',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=14,pady=5)
        s.fs_btn.pack(side=tk.RIGHT,padx=5)
        s.logout_btn=_134(_195,text="🚪 ВЫЙТИ (F9)",command=s._198,bg='#e17055',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=14,pady=5)
        s.logout_btn.pack(side=tk.RIGHT,padx=5)
        _199=tk.Frame(_192,bg='#0a0e27')
        _199.pack(pady=5)
        s.status_label=tk.Label(_199,text="⏸️ Ожидание...",bg='#0a0e27',fg='#fdcb6e',font=("Segoe UI",13,"bold"))
        s.status_label.pack(side=tk.LEFT,padx=10)
        s.count_label=tk.Label(_199,text="📨 0",bg='#0a0e27',fg='#00ff88',font=("Segoe UI",13,"bold"))
        s.count_label.pack(side=tk.LEFT,padx=10)
        s.preview=scrolledtext.ScrolledText(_192,height=8,bg='#1a1f4a',fg='#dfe6e9',insertbackground='white',font=("Segoe UI",10),relief=tk.FLAT,borderwidth=2,padx=15,pady=15)
        s.preview.pack(padx=10,pady=5,fill=tk.BOTH,expand=True)
        s.preview.insert("1.0","🔥 AWESOMETROLLING\n\n╔══════════════════════════════════════════════════════════════╗\n║  🎯 F3 → СТАРТ    🛑 F4 → СТОП    ⏸️ F5 → ПАУЗА           ║\n║  ⚙️ F6 → АДМИН-ПАНЕЛЬ    ⛶ F11 → ПОЛНЫЙ ЭКРАН              ║\n║  ❌ F9 → ВЫХОД                                             ║\n╚══════════════════════════════════════════════════════════════╝\n\n✅ Каждое сообщение уникально\n✅ Длинные связные предложения\n✅ 60+ шаблонов\n✅ Работает даже при свёрнутом окне\n✅ Автовход по ключу")
        s.preview.config(state=tk.DISABLED)
        _200=tk.Frame(_192,bg='#0a0e27')
        _200.pack(pady=8)
        s.start_btn=_134(_200,text="🤖 СТАРТ (F3)",command=s._201,bg='#00b894',fg='#dfe6e9',font=("Segoe UI",10,"bold"),width=16,padx=5,pady=8)
        s.start_btn.pack(side=tk.LEFT,padx=5)
        s.stop_btn=_134(_200,text="🛑 СТОП (F4)",command=s._202,bg='#e17055',fg='#dfe6e9',font=("Segoe UI",10,"bold"),width=16,padx=5,pady=8)
        s.stop_btn.pack(side=tk.LEFT,padx=5)
        s.pause_btn=_134(_200,text="⏸️ ПАУЗА (F5)",command=s._203,bg='#6c5ce7',fg='#dfe6e9',font=("Segoe UI",10,"bold"),width=16,padx=5,pady=8)
        s.pause_btn.pack(side=tk.LEFT,padx=5)
        _204=tk.Frame(_192,bg='#0a0e27')
        _204.pack(pady=5)
        tk.Label(_204,text="F3-СТАРТ | F4-СТОП | F5-ПАУЗА | F6-АДМИН | F9-ВЫХОД | F11-ПОЛНЫЙ ЭКРАН",bg='#0a0e27',fg='#b2bec3',font=("Segoe UI",9)).pack()
        tk.Label(_204,text="💜 Сделано с любовью и матом 💜",bg='#0a0e27',fg='#fd79a8',font=("Segoe UI",10,"bold")).pack()
        s.admin_panel=_205(s.root,s.is_admin)
        s.fullscreen=False
        s._206()
        s._207()
    def _196(s):s.admin_panel.toggle()
    def _197(s):
        s.fullscreen=not s.fullscreen
        s.root.attributes('-fullscreen',s.fullscreen)
        if s.fullscreen:s.fs_btn.config(text="⛶ ОКОННЫЙ РЕЖИМ (F11)",bg='#fdcb6e')
        else:s.fs_btn.config(text="⛶ ПОЛНЫЙ ЭКРАН (F11)",bg='#222860')
    def _206(s):
        try:
            keyboard.add_hotkey('f3',s._201)
            keyboard.add_hotkey('f4',s._202)
            keyboard.add_hotkey('f5',s._203)
            keyboard.add_hotkey('f6',s._196)
            keyboard.add_hotkey('f9',s._208)
            keyboard.add_hotkey('f11',s._197)
        except:pass
    def _201(s):_131();s.uis()
    def _202(s):_132();s.uis()
    def _203(s):_133();s.uis()
    def _198(s):
        if messagebox.askyesno("Выход из аккаунта","Вы уверены, что хотите выйти?"):
            _111._41()
            if s.stars:s.stars.stop()
            s.root.destroy()
            _209()
    def _208(s):
        _132()
        if s.stars:s.stars.stop()
        s.root.quit()
        s.root.destroy()
        sys.exit()
    def uc(s):
        try:s.count_label.config(text=f"📨 {_122}")
        except:pass
    def uis(s):
        try:
            if _123:
                s.status_label.config(text="⏸️ ПАУЗА",fg='#fdcb6e')
                s.pause_btn.config(text="▶️ ВОЗОБНОВИТЬ (F5)",bg='#fdcb6e')
            elif not _120 and _121 and _121.is_alive():
                s.status_label.config(text="🧠 ГЕНЕРАЦИЯ",fg='#00b894')
                s.start_btn.config(bg='#222860',text="🧠 РАБОТАЕТ...")
                s.pause_btn.config(text="⏸️ ПАУЗА (F5)",bg='#6c5ce7')
            else:
                s.status_label.config(text="⏸️ Остановлено",fg='#b2bec3')
                s.start_btn.config(bg='#00b894',text="🤖 СТАРТ (F3)")
                s.pause_btn.config(text="⏸️ ПАУЗА (F5)",bg='#6c5ce7')
        except:pass
    def _207(s):
        s.uis()
        s.count_label.config(text=f"📨 {_122}")
        s.root.after(500,s._207)

class _205:
    def __init__(s,parent,is_admin=False):
        s.parent=parent
        s.is_admin=is_admin
        s.window=None
        s.is_open=False
        s.sut=None
        s.cp()
    def cp(s):
        s.window=tk.Toplevel(s.parent)
        s.window.title(f"✨ АДМИН-ПАНЕЛЬ | AWESOMETROLLING")
        s.window.geometry("950x750")
        s.window.configure(bg='#0a0e27')
        s.window.minsize(850,650)
        s.window.protocol("WM_DELETE_WINDOW",s.hide)
        s.window.bind('<Escape>',lambda e:s.hide())
        s.window.withdraw()
        s.window.update_idletasks()
        _210=950;_211=750
        _212=(s.window.winfo_screenwidth()//2)-(_210//2)
        _213=(s.window.winfo_screenheight()//2)-(_211//2)
        s.window.geometry(f'{_210}x{_211}+{_212}+{_213}')
        _214=tk.Canvas(s.window,bg='#0a0e27',highlightthickness=0)
        _214.pack(fill=tk.BOTH,expand=True)
        s.admin_stars=_140(_214,100)
        s.admin_stars.update()
        _215=tk.Frame(_214,bg='#111638',bd=2,relief=tk.FLAT)
        _215.place(relx=0.5,rely=0.5,anchor=tk.CENTER,width=910,height=710)
        _216=tk.Frame(_215,bg='#111638',height=60)
        _216.pack(fill=tk.X,padx=0,pady=0)
        _216.pack_propagate(False)
        _217=tk.Frame(_216,bg='#111638')
        _217.pack(fill=tk.BOTH,padx=20,pady=10)
        tk.Label(_217,text="✨ АДМИН-ПАНЕЛЬ",font=("Segoe UI",22,"bold"),bg='#111638',fg='#ffd700').pack(side=tk.LEFT)
        tk.Label(_217,text=f"⭐ @flidges",font=("Segoe UI",12),bg='#111638',fg='#ff6b35').pack(side=tk.RIGHT)
        _218=tk.Frame(_215,bg='#00ff88',height=3)
        _218.pack(fill=tk.X,padx=0)
        s.notebook=ttk.Notebook(_215)
        s.notebook.pack(fill=tk.BOTH,expand=True,padx=15,pady=10)
        _219=ttk.Style()
        _219.theme_use('clam')
        _219.configure('TNotebook',background='#0a0e27',borderwidth=0)
        _219.configure('TNotebook.Tab',background='#111638',foreground='#dfe6e9',padding=[20,8],font=("Segoe UI",10,"bold"))
        _219.map('TNotebook.Tab',background=[('selected','#6c5ce7')])
        s.tab_main=tk.Frame(s.notebook,bg='#0a0e27')
        s.notebook.add(s.tab_main,text="📊 Главная")
        s.cmt()
        s.tab_about=tk.Frame(s.notebook,bg='#0a0e27')
        s.notebook.add(s.tab_about,text="💜 О нас")
        s.cat()
        if s.is_admin:
            s.tab_users=tk.Frame(s.notebook,bg='#0a0e27')
            s.notebook.add(s.tab_users,text="👥 Пользователи")
            s.cut()
            s.tab_keys=tk.Frame(s.notebook,bg='#0a0e27')
            s.notebook.add(s.tab_keys,text="🔑 Ключи")
            s.ckt()
            s.tab_stats=tk.Frame(s.notebook,bg='#0a0e27')
            s.notebook.add(s.tab_stats,text="📈 Статистика")
            s.cst()
        s.us()
    def cmt(s):
        _220=s.tab_main
        _221=tk.Frame(_220,bg='#0a0e27')
        _221.pack(pady=10,padx=20,fill=tk.X)
        tk.Label(_221,text="🚀 Скорость отправки",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#a29bfe').pack(anchor='w')
        _222=tk.Frame(_221,bg='#0a0e27')
        _222.pack(fill=tk.X,pady=5)
        s.speed_slider=tk.Scale(_222,from_=0.001,to=0.45,resolution=0.001,orient=tk.HORIZONTAL,length=500,bg='#0a0e27',fg='#dfe6e9',troughcolor='#1a1f4a',sliderlength=22,highlightthickness=0)
        s.speed_slider.set(_127)
        s.speed_slider.pack(side=tk.LEFT,fill=tk.X,expand=True)
        s.speed_label=tk.Label(_222,text=f"{_127:.3f}с",bg='#0a0e27',fg='#ffd700',font=("Segoe UI",18,"bold"),width=8)
        s.speed_label.pack(side=tk.LEFT,padx=10)
        def _223(val):
            _224=float(val)
            s.speed_label.config(text=f"{_224:.3f}с")
            if s.sut:s.window.after_cancel(s.sut)
            def _225():
                global _127
                _127=_224
                settings['spam_speed']=_224
                _226(settings)
            s.sut=s.window.after(300,_225)
        s.speed_slider.config(command=_223)
        _227=tk.Frame(_220,bg='#0a0e27')
        _227.pack(pady=5,padx=20,fill=tk.X)
        tk.Label(_227,text="⚡ Быстрые пресеты",font=("Segoe UI",11,"bold"),bg='#0a0e27',fg='#b2bec3').pack(anchor='w')
        _228=tk.Frame(_227,bg='#0a0e27')
        _228.pack(fill=tk.X,pady=5)
        for _229,_230 in [("🐢 0.1с",0.1),("🚶 0.05с",0.05),("🏃 0.02с",0.02),("🚀 0.005с",0.005),("🔥 0.001с",0.001)]:
            _231=_134(_228,text=_229,command=lambda sp=_230:s._232(sp),bg='#222860',fg='#dfe6e9',font=("Segoe UI",9,"bold"),padx=14,pady=6)
            _231.pack(side=tk.LEFT,padx=3)
        _233=tk.Frame(_220,bg='#0a0e27')
        _233.pack(pady=15,padx=20,fill=tk.BOTH,expand=True)
        tk.Label(_233,text="📊 Живая статистика",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#00ff88').pack(anchor='w')
        s.info_text=tk.Text(_233,height=8,bg='#111638',fg='#dfe6e9',font=("Consolas",10),relief=tk.FLAT,borderwidth=2,padx=15,pady=12)
        s.info_text.pack(fill=tk.BOTH,expand=True,pady=5)
        s.info_text.insert("1.0","⏳ Ожидание запуска...")
        s.info_text.config(state=tk.DISABLED)
        _234=tk.Frame(_220,bg='#0a0e27')
        _234.pack(pady=10)
        for _235,_236 in [("🔄 Обновить",s.ui),("🧹 Сбросить счётчик",s.rc)]:
            _237=_134(_234,text=_235,command=_236,bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=18,pady=6)
            _237.pack(side=tk.LEFT,padx=5)
    def cat(s):
        _238=s.tab_about
        _239=tk.Frame(_238,bg='#0a0e27')
        _239.pack(fill=tk.BOTH,expand=True,padx=40,pady=40)
        tk.Label(_239,text="🔥",font=("Segoe UI",70),bg='#0a0e27').pack(pady=5)
        tk.Label(_239,text="AWESOMETROLLING",font=("Segoe UI",26,"bold"),bg='#0a0e27',fg='#ffd700').pack(pady=5)
        tk.Label(_239,text="✨ Версия 3.0 ✨",font=("Segoe UI",14),bg='#0a0e27',fg='#b2bec3').pack(pady=5)
        _240=tk.Frame(_239,bg='#00ff88',height=2,width=350)
        _240.pack(pady=15)
        tk.Label(_239,text="👨‍💻 РАЗРАБОТЧИК",font=("Segoe UI",13,"bold"),bg='#0a0e27',fg='#dfe6e9').pack()
        tk.Label(_239,text="@flidges",font=("Segoe UI",20,"bold"),bg='#0a0e27',fg='#fd79a8').pack(pady=3)
        tk.Label(_239,text="✨ Создатель: awesome / tg @flidges ✨",font=("Segoe UI",12),bg='#0a0e27',fg='#ffd700').pack(pady=5)
        tk.Label(_239,text="💰 Цена - узнайте у @flidges",font=("Segoe UI",12,"bold"),bg='#0a0e27',fg='#00ff88').pack(pady=5)
        _241=tk.Frame(_239,bg='#6c5ce7',height=1,width=250)
        _241.pack(pady=10)
        for _242 in ["🔥 Каждое сообщение уникально","💎 Длинные связные предложения","📚 60+ шаблонов","⚡ Работает при свёрнутом окне","🔒 Защита HWID","💾 Автосохранение ключа"]:
            tk.Label(_239,text=_242,font=("Segoe UI",11),bg='#0a0e27',fg='#00ff88').pack(pady=2)
        _243=tk.Frame(_239,bg='#6c5ce7',height=1,width=200)
        _243.pack(pady=10)
        tk.Label(_239,text="💜 Сделано с любовью и матом 💜",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#fd79a8').pack(pady=5)
        tk.Label(_239,text="© 2026 Все права защищены 🚀",font=("Segoe UI",9),bg='#0a0e27',fg='#636e72').pack(pady=5)
    def cut(s):
        if not s.is_admin:return
        _244=s.tab_users
        _245=tk.Frame(_244,bg='#0a0e27')
        _245.pack(pady=10,padx=20,fill=tk.X)
        tk.Label(_245,text="👥 Управление пользователями",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#ffd700').pack(anchor='w')
        _246=tk.Frame(_245,bg='#0a0e27')
        _246.pack(fill=tk.X,pady=5)
        s.user_entry=tk.Entry(_246,bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",11),relief=tk.FLAT,borderwidth=2,width=20)
        s.user_entry.pack(side=tk.LEFT,padx=5)
        s.user_entry.insert(0,"Имя пользователя")
        s.user_entry.bind('<FocusIn>',lambda e:s.user_entry.delete(0,tk.END))
        _247=tk.StringVar(value="1")
        _248=ttk.Combobox(_246,textvariable=_247,values=["1","3","6","12","24"],width=5,state="readonly")
        _248.pack(side=tk.LEFT,padx=5)
        tk.Label(_246,text="мес.",bg='#0a0e27',fg='#b2bec3').pack(side=tk.LEFT)
        tk.Button(_246,text="✅ ВЫДАТЬ",command=lambda:s._249(_247.get()),bg='#00b894',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
        tk.Button(_246,text="🚫 ЗАБРАТЬ",command=s._250,bg='#e17055',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
        tk.Button(_246,text="🔄 ПРОДЛИТЬ",command=lambda:s._251(_247.get()),bg='#6c5ce7',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
        _252=tk.Frame(_244,bg='#0a0e27')
        _252.pack(pady=10,padx=20,fill=tk.BOTH,expand=True)
        _253=("Имя","Статус","Бан","До","Ключ","HWID")
        s.tree=ttk.Treeview(_252,columns=_253,show="headings",height=12)
        for _254 in _253:
            s.tree.heading(_254,text=_254)
            s.tree.column(_254,width=100)
        s.tree.column("HWID",width=120)
        _255=ttk.Scrollbar(_252,orient=tk.VERTICAL,command=s.tree.yview)
        s.tree.configure(yscrollcommand=_255.set)
        s.tree.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        _255.pack(side=tk.RIGHT,fill=tk.Y)
        tk.Label(_244,text="💡 Двойной клик по пользователю → бан/разбан",bg='#0a0e27',fg='#b2bec3',font=("Segoe UI",9)).pack(pady=5)
        s.ru()
    def ckt(s):
        if not s.is_admin:return
        _256=s.tab_keys
        _257=tk.Frame(_256,bg='#0a0e27')
        _257.pack(pady=10,padx=20,fill=tk.X)
        tk.Label(_257,text="🔑 Управление ключами",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#ffd700').pack(anchor='w')
        _258=tk.Frame(_257,bg='#0a0e27')
        _258.pack(fill=tk.X,pady=5)
        tk.Label(_258,text="Ключ:",bg='#0a0e27',fg='#dfe6e9',font=("Segoe UI",10)).pack(side=tk.LEFT,padx=5)
        s.key_entry=tk.Entry(_258,bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",11),relief=tk.FLAT,borderwidth=2,width=20)
        s.key_entry.pack(side=tk.LEFT,padx=5)
        s.key_entry.insert(0,"Введите ключ")
        s.key_entry.bind('<FocusIn>',lambda e:s.key_entry.delete(0,tk.END)if s.key_entry.get()=="Введите ключ"else None)
        tk.Label(_258,text="мес:",bg='#0a0e27',fg='#dfe6e9',font=("Segoe UI",10)).pack(side=tk.LEFT,padx=5)
        s.key_months=ttk.Combobox(_258,values=["1","3","6","12","24"],width=5,state="readonly")
        s.key_months.set("1")
        s.key_months.pack(side=tk.LEFT,padx=5)
        tk.Button(_258,text="➕ ДОБАВИТЬ КЛЮЧ",command=s._259,bg='#00b894',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
        tk.Button(_258,text="🎲 СГЕНЕРИРОВАТЬ",command=s._260,bg='#6c5ce7',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
        _261=tk.Frame(_256,bg='#0a0e27')
        _261.pack(pady=10,padx=20,fill=tk.BOTH,expand=True)
        _262=("Ключ","Создан","До","Использован","Кем","HWID")
        s.keys_tree=ttk.Treeview(_261,columns=_262,show="headings",height=10)
        for _263 in _262:
            s.keys_tree.heading(_263,text=_263)
            s.keys_tree.column(_263,width=100)
        s.keys_tree.column("HWID",width=100)
        _264=ttk.Scrollbar(_261,orient=tk.VERTICAL,command=s.keys_tree.yview)
        s.keys_tree.configure(yscrollcommand=_264.set)
        s.keys_tree.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        _264.pack(side=tk.RIGHT,fill=tk.Y)
        _265=tk.Frame(_256,bg='#0a0e27')
        _265.pack(pady=5,padx=20,fill=tk.X)
        tk.Button(_265,text="🗑 УДАЛИТЬ ВЫБРАННЫЙ КЛЮЧ",command=s._266,bg='#e17055',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT)
        tk.Label(_265,text="💡 Выберите ключ в списке и нажмите УДАЛИТЬ",bg='#0a0e27',fg='#b2bec3',font=("Segoe UI",9)).pack(side=tk.LEFT,padx=10)
        s.rk()
    def cst(s):
        if not s.is_admin:return
        _267=s.tab_stats
        _268=tk.Frame(_267,bg='#0a0e27')
        _268.pack(fill=tk.BOTH,expand=True,padx=20,pady=20)
        tk.Label(_268,text="📈 ДЕТАЛЬНАЯ СТАТИСТИКА",font=("Segoe UI",18,"bold"),bg='#0a0e27',fg='#ffd700').pack(pady=10)
        s.stats_text=tk.Text(_268,height=14,bg='#111638',fg='#dfe6e9',font=("Consolas",11),relief=tk.FLAT,borderwidth=2,padx=20,pady=15)
        s.stats_text.pack(fill=tk.BOTH,expand=True,pady=10)
        s.stats_text.config(state=tk.DISABLED)
        _269=tk.Frame(_268,bg='#0a0e27')
        _269.pack(pady=10)
        tk.Button(_269,text="🔄 ОБНОВИТЬ",command=s._270,bg='#6c5ce7',fg='white',font=("Segoe UI",10,"bold"),relief=tk.FLAT,cursor="hand2",padx=20,pady=8).pack()
        s._270()
    def _232(s,speed):
        global _127
        _127=speed
        s.speed_slider.set(speed)
        s.speed_label.config(text=f"{speed:.3f}с")
        settings['spam_speed']=speed
        _226(settings)
    def _249(s,months):
        if not s.is_admin:
            messagebox.showwarning("Доступ запрещен","Только для администраторов!")
            return
        _271=s.user_entry.get().strip()
        if not _271 or _271=="Имя пользователя":
            messagebox.showerror("Ошибка","Введите имя пользователя!")
            return
        _272,_273=_111._94(_271,int(months))
        if _272:
            messagebox.showinfo("Успех",_273)
            s.ru()
        else:messagebox.showerror("Ошибка",_273)
    def _250(s):
        if not s.is_admin:
            messagebox.showwarning("Доступ запрещен","Только для администраторов!")
            return
        _274=s.user_entry.get().strip()
        if not _274 or _274=="Имя пользователя":
            messagebox.showerror("Ошибка","Введите имя пользователя!")
            return
        if messagebox.askyesno("Подтверждение",f"Забрать доступ у {_274}?"):
            _111._101(_274)
            messagebox.showinfo("Успех",f"Доступ у {_274} забран!")
            s.ru()
    def _251(s,months):
        if not s.is_admin:
            messagebox.showwarning("Доступ запрещен","Только для администраторов!")
            return
        _275=s.user_entry.get().strip()
        if not _275 or _275=="Имя пользователя":
            messagebox.showerror("Ошибка","Введите имя пользователя!")
            return
        _276,_277=_111._105(_275,int(months))
        if _276:
            messagebox.showinfo("Успех",_277)
            s.ru()
        else:messagebox.showerror("Ошибка",_277)
    def _259(s):
        if not s.is_admin:
            messagebox.showwarning("Доступ запрещен","Только для администраторов!")
            return
        _278=s.key_entry.get().strip().upper()
        _279=int(s.key_months.get())
        if not _278 or _278=="ВВЕДИТЕ КЛЮЧ":
            messagebox.showerror("Ошибка","Введите ключ!")
            return
        _280,_281=_111._42(_279,_278)
        if _280:
            messagebox.showinfo("Успех",f"🔑 Ключ {_278} добавлен на {_279} месяцев!")
            s.rk()
            s.key_entry.delete(0,tk.END)
            s.key_entry.insert(0,"Введите ключ")
        else:messagebox.showerror("Ошибка","Такой ключ уже существует!")
    def _260(s):
        if not s.is_admin:
            messagebox.showwarning("Доступ запрещен","Только для администраторов!")
            return
        _282=int(s.key_months.get())
        _283,_284=_111._42(_282)
        if _283:
            messagebox.showinfo("Ключ сгенерирован",f"🔑 Ключ: {_284}\n📅 Действует: {_282} месяцев\n📩 Отправь его покупателю!\n⚠️ Ключ привяжется к первому компьютеру!")
            s.rk()
    def _266(s):
        if not s.is_admin:
            messagebox.showwarning("Доступ запрещен","Только для администраторов!")
            return
        _285=s.keys_tree.selection()
        if not _285:
            messagebox.showerror("Ошибка","Выберите ключ для удаления!")
            return
        _286=_285[0]
        _287=s.keys_tree.item(_286,'values')
        _288=_287[0]
        if messagebox.askyesno("Подтверждение",f"Удалить ключ {_288}?"):
            _111._48(_288)
            messagebox.showinfo("Успех",f"Ключ {_288} удален!")
            s.rk()
    def ru(s):
        if not s.is_admin:return
        for _289 in s.tree.get_children():s.tree.delete(_289)
        _290=_111._88()
        for _291 in _290:
            _292,_293,_294,_295,_296,_297,_298=_291
            if _296:
                try:_299=datetime.fromisoformat(_296).strftime('%d.%m.%Y')
                except:_299="Ошибка"
            else:_299="-"
            _300="👑"if _293 else("⭐"if _294 else"👤")
            _301="🚫"if _295 else"✅"
            _302=_297[:12]+"..."if _297 else"-"
            _303=_298[:8]+"..."if _298 else"-"
            s.tree.insert("",tk.END,values=(_292,_300,_301,_299,_303,_302),tags=(_292,_295))
        s.tree.bind('<Double-Button-1>',s._304)
    def _304(s,e):
        if not s.is_admin:return
        _305=s.tree.selection()
        if not _305:return
        _306=_305[0]
        _307=s.tree.item(_306,'values')
        _308=_307[0]
        _309=_307[2]=="🚫"
        _310=_307[1]=="👑"
        if _310:
            messagebox.showinfo("Инфо","Нельзя изменять овнера!")
            return
        if _309:
            if messagebox.askyesno("Восстановить",f"Разбанить {_308}?"):
                _111._103(_308)
                messagebox.showinfo("Успех",f"{_308} разбанен!")
                s.ru()
        else:
            if messagebox.askyesno("Забанить",f"Забанить {_308}?"):
                _111._101(_308)
                messagebox.showinfo("Успех",f"{_308} забанен!")
                s.ru()
    def rk(s):
        if not s.is_admin:return
        for _311 in s.keys_tree.get_children():s.keys_tree.delete(_311)
        _312=_111._91()
        for _313 in _312:
            _314,_315,_316,_317,_318,_319,_320=_313
            try:_321=datetime.fromisoformat(_315).strftime('%d.%m')if _315 else"-"
            except:_321="-"
            try:_322=datetime.fromisoformat(_316).strftime('%d.%m.%Y')if _316 else"-"
            except:_322="-"
            _323="✅"if _319 else"🔓"
            _324=_317 if _317 else"-"
            _325=_318[:12]+"..."if _318 else"-"
            s.keys_tree.insert("",tk.END,values=(_314,_321,_322,_323,_324,_325))
    def _270(s):
        if not s.is_admin:return
        _326=_111._88()
        _327=_111._91()
        _328=f"""
╔══════════════════════════════════════════════════════════════╗
║                      📊 СТАТИСТИКА                          ║
╠══════════════════════════════════════════════════════════════╣
║  👥 Всего пользователей: {len(_326):>4}                                     ║
║  👑 Овнеров:             {sum(1 for u in _326 if u[1]):>4}                                     ║
║  ⭐ Админов:             {sum(1 for u in _326 if u[2]):>4}                                     ║
║  🚫 Забаненных:          {sum(1 for u in _326 if u[3]):>4}                                     ║
║  ✅ Активных:            {sum(1 for u in _326 if not u[3]):>4}                                     ║
╠══════════════════════════════════════════════════════════════╣
║  🔑 Всего ключей:        {len(_327):>4}                                     ║
║  ✅ Использованных:      {sum(1 for k in _327 if k[5]):>4}                                     ║
║  🔓 Свободных:           {len(_327) - sum(1 for k in _327 if k[5]):>4}                                     ║
╚══════════════════════════════════════════════════════════════╝
"""
        s.stats_text.config(state=tk.NORMAL)
        s.stats_text.delete("1.0",tk.END)
        s.stats_text.insert("1.0",_328)
        s.stats_text.config(state=tk.DISABLED)
    def ui(s):
        global _122,_124,_125
        _329="0с"
        if _125:
            _330=int(time.time()-_125)
            _331=_330//60
            _330%=60
            _332=_331//60
            _331%=60
            if _332>0:_329=f"{_332}ч {_331}м {_330}с"
            elif _331>0:_329=f"{_331}м {_330}с"
            else:_329=f"{_330}с"
        _333="⏸️ Остановлено"
        if not _120 and _121 and _121.is_alive():
            if _123:_333="⏸️ ПАУЗА"
            else:_333="🧠 АКТИВЕН"
        _334=f"""
╔══════════════════════════════════════════════════════╗
║  📊 СТАТИСТИКА              Статус: {_333:<10} ║
╠══════════════════════════════════════════════════════╣
║  📨 За сессию: {_122:>6}                                  ║
║  📨 Всего:      {_124:>6}                                  ║
║  ⏱ Время:      {_329:>10}                              ║
║  🚀 Скорость:  {_127:.3f}с                                   ║
║  📝 Шаблонов:  {len(INSULT_TEMPLATES):>6}                                  ║
║  🚫 Забанено:  {len(settings.get('banned_words',[])):>6}                                  ║
║  ⭐ Dev:       @flidges                              ║
╚══════════════════════════════════════════════════════╝
"""
        s.info_text.config(state=tk.NORMAL)
        s.info_text.delete("1.0",tk.END)
        s.info_text.insert("1.0",_334)
        s.info_text.config(state=tk.DISABLED)
    def rc(s):
        global _122,_124
        _122=0
        _124=0
        s.ui()
        messagebox.showinfo("✅ Сброшено","Счётчики обнулены!")
    def us(s):
        s.ui()
        s.window.after(2000,s.us)
    def show(s):
        if s.window:
            s.window.deiconify()
            s.window.lift()
            s.is_open=True
            s.us()
    def hide(s):
        if s.window:
            s.window.withdraw()
            s.is_open=False
            if hasattr(s,'admin_stars')and s.admin_stars:s.admin_stars.stop()
    def toggle(s):
        if s.is_open:s.hide()
        else:s.show()

def _226(settings_data):
    try:
        _335={}
        for _336,_337 in settings_data.items():
            if isinstance(_337,(str,int,float,bool)):
                _335[_336]=_10(str(_337))
            else:_335[_336]=_337
        with open(os.path.join(_14,"troll_settings.json"),'w',encoding='utf-8')as _338:
            json.dump(_335,_338,ensure_ascii=False,indent=2)
    except:pass

def _209():
    try:ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
    except:pass
    _339=tk.Tk()
    _339.title("🔐 АКТИВАЦИЯ")
    _339.geometry("450x350")
    _339.configure(bg='#0a0e27')
    tk.Label(_339,text="🔥 AWESOMETROLLING",font=("Segoe UI",24,"bold"),bg='#0a0e27',fg='#ffd700').pack(pady=20)
    tk.Label(_339,text="ВВЕДИТЕ КЛЮЧ",font=("Segoe UI",14),bg='#0a0e27',fg='#dfe6e9').pack(pady=5)
    _340=tk.Entry(_339,font=("Segoe UI",14),bg='#1a1f4a',fg='#00ff88',relief=tk.FLAT,borderwidth=2)
    _340.pack(pady=10,padx=40,fill=tk.X)
    _340.focus()
    _341=tk.Label(_339,text="",bg='#0a0e27',fg='#e17055')
    _341.pack()
    def _342():
        _343=_340.get().strip()
        if not _343:
            _341.config(text="❌ ВВЕДИТЕ КЛЮЧ!",fg='#e17055')
            return
        _344,_345=_111._50(_343)
        if _344:
            _341.config(text="✅ "+_345,fg='#00b894')
            _339.after(1500,lambda:[_339.destroy(),_181()])
        else:
            _341.config(text="❌ "+_345,fg='#e17055')
    tk.Button(_339,text="АКТИВИРОВАТЬ",command=_342,bg='#6c5ce7',fg='white',font=("Segoe UI",10,"bold"),relief=tk.FLAT,cursor="hand2",padx=20,pady=10).pack(pady=10)
    _339.bind('<Return>',lambda e:_342())
    _339.mainloop()

if __name__=="__main__":
    try:ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
    except:pass
    _346,_347=_111._72()
    if _346:_181()
    else:
        _346,_347=_111._76()
        if _346:_181()
        else:_209()
