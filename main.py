import tkinter as tk,time,random,threading,sys,os,sqlite3,hashlib,uuid,subprocess,platform,json,re,ctypes,base64,requests
from datetime import datetime,timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
try:ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
except:pass

_a1="pe";_a2="pe";_a3="la";_a4="we";_a5="s";_a6=_a1+_a2+_a3+_a4+_a5
_a7=lambda d:base64.urlsafe_b64encode(hashlib.sha512(_a6.encode()).digest()[:32])
_a8=lambda d:Fernet(_a7()).encrypt(d.encode()if isinstance(d,str)else d)if d else None
_a9=lambda e:Fernet(_a7()).decrypt(e.encode()if isinstance(e,str)else e).decode()if e else None

_b1="https://yzhgcdnjuvfhcvwedgga";_b2=".supabase.co";_b3=_b1+_b2
_b4="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9";_b5=".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6aGdjZG5qdXZmaGN3dmVkZ2dhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY0NjExNTgsImV4cCI6MjEwMjAzNzE1OH0";_b6=".ccCiaKPnpwjg69PC90qtPDOIWn5PezGxKERJtdWUB_I";_b7=_b4+_b5+_b6

_b8=lambda m,e,d=None:requests.get if m=="GET"else requests.post if m=="POST"else requests.patch
_b9=lambda m,e,d=None:(lambda r:r.json()if r.ok else None)(_b8(m,e,d)(f"{_b3}/rest/v1/{e}",headers={"apikey":_b7,"Authorization":f"Bearer {_b7}","Content-Type":"application/json"},json=d))
_b10=lambda:_b9("GET","users?order=id.desc")
_b11=lambda u,h,e,s,o=0,a=0:_b9("POST","users",{"username":u,"hwid":h,"is_owner":o,"is_admin":a,"expires_at":e,"saved_key":s})
_b12=lambda:_b9("GET","license_keys?order=id.desc")
_b13=lambda k,e,o:_b9("POST","license_keys",{"key_text":k,"expires_at":e,"owner_hwid":o,"is_used":0})
_b14=lambda k,u,h:_b9("PATCH",f"license_keys?key_text=eq.{k}",{"used_by":u,"used_hwid":h,"used_at":datetime.now().isoformat(),"is_used":1})

_b15=lambda:os.path.dirname(sys.executable)if getattr(sys,'frozen',False)else os.path.dirname(os.path.abspath(__file__))
_b16=_b15()
_b17=os.path.join(_b16,"troll_users.db")
_b18=os.path.join(_b16,"license.key")

class _b19:
 def __init__(s):
  s._a=sqlite3.connect(_b17)
  s._b=s._a.cursor()
  s._c()
 def _c(s):
  s._b.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,hwid TEXT UNIQUE,is_owner INT DEFAULT 0,is_admin INT DEFAULT 0,is_banned INT DEFAULT 0,created_at TEXT,expires_at TEXT,saved_key TEXT)')
  s._b.execute('CREATE TABLE IF NOT EXISTS keys(key_text TEXT UNIQUE,created_at TEXT,expires_at TEXT,used_by TEXT,used_hwid TEXT,is_used INT DEFAULT 0,owner_hwid TEXT)')
  s._a.commit()
 def _d(s):
  try:
   _=uuid.getnode()
   return ':'.join(('%012x'%_)[i:i+2]for i in range(0,12,2))
  except:return "unknown"
 def _e(s):
  try:return os.environ.get('USERNAME','unknown')
  except:return "unknown"
 def _f(s):
  try:return os.environ.get('COMPUTERNAME','unknown')
  except:return "unknown"
 def _g(s):
  try:
   if platform.system()=='Windows':
    _=subprocess.run(['wmic','diskdrive','get','serialnumber'],capture_output=True,text=True)
    __=_.stdout.strip().split('\n')
    if len(__)>1:return __[1].strip()
   return "unknown"
  except:return "unknown"
 def _h(s):
  try:
   if platform.system()=='Windows':
    _=subprocess.run(['wmic','cpu','get','processorid'],capture_output=True,text=True)
    __=_.stdout.strip().split('\n')
    if len(__)>1:return __[1].strip()
   return "unknown"
  except:return "unknown"
 def _i(s):
  _=s._d()+s._e()+s._f()+s._g()+s._h()+platform.processor()+platform.machine()
  return hashlib.sha512(_a8(_)).hexdigest()[:64]
 def _j(s,k):return k==_a6
 def _k(s,k):
  with open(_b18,'w')as _:_.write(base64.b64encode(_a8(k)).decode())
 def _l(s):
  if os.path.exists(_b18):
   try:
    with open(_b18,'r')as _:return _a9(base64.b64decode(_.read().strip().encode()))
   except:return None
  return None
 def _m(s):
  if os.path.exists(_b18):os.remove(_b18)
 def _n(s,m=1,c=None):
  k=c or hashlib.sha256(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()[:12].upper()
  e=(datetime.now()+timedelta(days=30*m)).isoformat()
  o=s._i()
  try:
   s._b.execute('INSERT INTO keys(key_text,created_at,expires_at,is_used,owner_hwid)VALUES(?,?,?,0,?)',(_a8(k),_a8(datetime.now().isoformat()),_a8(e),_a8(o)))
   s._a.commit()
   try:_b13(k,e,o)
   except:pass
   return True,k
  except:return False,None
 def _o(s,k):
  s._b.execute('DELETE FROM keys WHERE key_text=?',(_a8(k),))
  s._a.commit()
  return True
 def _p(s,k,save=True):
  h=s._i();u=s._e();ku=k.upper()
  if s._j(ku):
   a=_a8(h);b=_a8(u);c=_a8("2099-12-31T23:59:59");d=_a8(ku)
   e=s._b.execute('SELECT*FROM users WHERE hwid=?',(a,)).fetchone()
   if e:s._b.execute('UPDATE users SET username=?,is_owner=1,is_admin=1,is_banned=0,expires_at=?,saved_key=?WHERE hwid=?',(b,c,d,a))
   else:s._b.execute('INSERT INTO users(username,hwid,is_owner,is_admin,created_at,expires_at,saved_key)VALUES(?,?,1,1,?,?,?)',(b,a,_a8(datetime.now().isoformat()),c,d))
   s._a.commit()
   if save:s._k(ku)
   try:_b11(u,h,"2099-12-31T23:59:59",ku,1,1)
   except:pass
   return True,"👑 ДОБРО ПОЖАЛОВАТЬ, ОВНЕР!"
  r=s._b.execute('SELECT key_text,expires_at,is_used,used_hwid,owner_hwid FROM keys WHERE key_text=?',(_a8(ku),)).fetchone()
  if not r:return False,"❌ НЕВЕРНЫЙ КЛЮЧ!"
  a,b,c,d,e=r
  f=_a9(b);g=_a9(d)if d else None;h=_a9(e)if e else None
  if h and h!=s._i():return False,"❌ ЭТОТ КЛЮЧ НЕ ДЛЯ ТВОЕГО КОМПЬЮТЕРА!"
  if c and g and g!=s._i():return False,"❌ КЛЮЧ УЖЕ АКТИВИРОВАН НА ДРУГОМ КОМПЬЮТЕРЕ!"
  if c and g==s._i():
   i=datetime.fromisoformat(f)
   if datetime.now()>i:return False,f"❌ КЛЮЧ ИСТЕК {i.strftime('%d.%m.%Y')}!"
   return True,f"✅ ДОСТУП УЖЕ АКТИВИРОВАН ДО {i.strftime('%d.%m.%Y')}!"
  i=datetime.fromisoformat(f)
  if datetime.now()>i:return False,f"❌ КЛЮЧ ИСТЕК {i.strftime('%d.%m.%Y')}!"
  s._b.execute('UPDATE keys SET used_by=?,used_hwid=?,is_used=1 WHERE key_text=?',(_a8(u),_a8(h),_a8(ku)))
  j=s._b.execute('SELECT*FROM users WHERE hwid=?',(_a8(h),)).fetchone()
  if j:s._b.execute('UPDATE users SET username=?,expires_at=?,is_banned=0,saved_key=?WHERE hwid=?',(_a8(u),a,_a8(ku),_a8(h)))
  else:s._b.execute('INSERT INTO users(username,hwid,created_at,expires_at,saved_key)VALUES(?,?,?,?,?)',(_a8(u),_a8(h),_a8(datetime.now().isoformat()),a,_a8(ku)))
  s._a.commit()
  if save:s._k(ku)
  try:_b11(u,h,f,ku,0,0);_b14(ku,u,h)
  except:pass
  return True,f"✅ ВЕРНО! ДОСТУП ДО {i.strftime('%d.%m.%Y')}!"
 def _q(s):
  k=s._l()
  if k:
   ok,msg=s._p(k,False)
   if ok:return True,msg
  return False,None
 def _r(s):
  h=s._i();a=_a8(h)
  r=s._b.execute('SELECT username,is_owner,is_admin,is_banned,expires_at FROM users WHERE hwid=?',(a,)).fetchone()
  if not r:return False,"🔑 ТРЕБУЕТСЯ АКТИВАЦИЯ!"
  a,b,c,d,e=r
  u=_a9(a);ex=_a9(e)
  if d:return False,"🚫 ДОСТУП ЗАБЛОКИРОВАН!"
  exp=datetime.fromisoformat(ex)
  if datetime.now()>exp:return False,f"⏰ ПОДПИСКА ИСТЕКЛА {exp.strftime('%d.%m.%Y')}!"
  s._b.execute('UPDATE users SET last_active=? WHERE hwid=?',(_a8(datetime.now().isoformat()),_a8(h)))
  s._a.commit()
  return True,u
 def _s(s):
  r=s._b.execute('SELECT username,is_owner,is_admin,is_banned,expires_at,hwid,saved_key FROM users ORDER BY is_owner DESC').fetchall()
  return[(_a9(x[0]),x[1],x[2],x[3],_a9(x[4]),_a9(x[5]),_a9(x[6])if x[6]else None)for x in r]
 def _t(s):
  r=s._b.execute('SELECT key_text,created_at,expires_at,used_by,used_hwid,is_used,owner_hwid FROM keys ORDER BY created_at DESC').fetchall()
  return[(_a9(x[0]),_a9(x[1]),_a9(x[2]),_a9(x[3])if x[3]else None,_a9(x[4])if x[4]else None,x[5],_a9(x[6])if x[6]else None)for x in r]
 def _u(s,u,m=1):
  e=(datetime.now()+timedelta(days=30*m)).isoformat()
  a=_a8(u);b=_a8(e)
  c=s._b.execute('SELECT*FROM users WHERE username=?',(a,)).fetchone()
  if c:s._b.execute('UPDATE users SET expires_at=?,is_banned=0 WHERE username=?',(b,a))
  else:s._b.execute('INSERT INTO users(username,hwid,created_at,expires_at)VALUES(?,?,?,?)',(a,_a8(f"MANUAL_{uuid.uuid4().hex[:8]}"),_a8(datetime.now().isoformat()),b))
  s._a.commit()
  return True,f"✅ ДОСТУП ВЫДАН {u} НА {m} МЕСЯЦЕВ!"
 def _v(s,u):
  s._b.execute('UPDATE users SET is_banned=1 WHERE username=?',(_a8(u),))
  s._a.commit()
  return True
 def _w(s,u):
  s._b.execute('UPDATE users SET is_banned=0 WHERE username=?',(_a8(u),))
  s._a.commit()
  return True
 def _x(s,u,m=1):
  r=s._b.execute('SELECT expires_at FROM users WHERE username=?',(_a8(u),)).fetchone()
  if r:
   e=_a9(r[0])
   n=datetime.fromisoformat(e)+timedelta(days=30*m)
   s._b.execute('UPDATE users SET expires_at=? WHERE username=?',(_a8(n.isoformat()),_a8(u)))
   s._a.commit()
   return True,f"✅ ПРОДЛЕН ДО {n.strftime('%d.%m.%Y')}!"
  return False,"❌ ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН!"
_b20=_b19()

_INSULT_TEMPLATES=[
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

_b21=[];_b22=_INSULT_TEMPLATES.copy()
def _b23():
 global _b21,_b22
 if not _b22:
  _b22=_INSULT_TEMPLATES.copy();_b21=[]
 _=random.choice(_b22);_b22.remove(_);_b21.append(_);return _
def _b24():
 _=_b23()
 _=re.sub(r'[.,!?;:()"\']','',_)
 __=_.split()
 ___=settings.get('banned_words',[])
 __=[x for x in __ if x not in ___]
 if not __:__=['ты','хуесос','блять']
 return __

_b25=False;_b26=None;_b27=0;_b28=False;_b29=0;_b30=None;_b31=None;_b32=0.035;settings={}

def _b33():
 global _b25,_b27,_b28,_b32,_b29,_b30
 _b25=False;_b27=0;_b29=0;_b30=time.time()
 while not _b25:
  if _b28:
   time.sleep(0.1);continue
  _=_b24()
  for __ in _:
   if _b25:return
   if _b28:break
   try:
    keyboard.write(__)
    time.sleep(_b32)
    keyboard.press_and_release('enter')
    time.sleep(settings.get('pause_between_messages',0.01))
    _b27+=1;_b29+=1
    if _b31:_b31.uc()
   except:pass
def _b34():
 global _b25,_b26
 if _b26 and _b26.is_alive():return
 _b25=False
 _b26=threading.Thread(target=_b33)
 _b26.daemon=True
 _b26.start()
 if _b31:_b31.uis()
def _b35():
 global _b25
 _b25=True
 if _b31:_b31.uis()
def _b36():
 global _b28
 _b28=not _b28
 if _b31:_b31.uis()
 return _b28

class _b37(tk.Button):
 def __init__(s,master,**kwargs):
  super().__init__(master,**kwargs)
  s.config(relief=tk.FLAT,borderwidth=0,font=("Segoe UI",10,"bold"),cursor="hand2")
  s._a=s['bg'];s._b=s['fg']
  s.bind('<Enter>',s._c)
  s.bind('<Leave>',s._d)
  s.bind('<Button-1>',s._e)
 def _c(s,e):s.config(bg=s['bg'],fg=s['fg'])
 def _d(s,e):s.config(bg=s._a,fg=s._b)
 def _e(s,e):s.config(relief=tk.SUNKEN);s.after(100,lambda:s.config(relief=tk.FLAT))

class _b38:
 def __init__(s,canvas,num=150):
  s.canvas=canvas;s.stars=[];s.running=True;s.num=num
  for _ in range(num):
   _a=random.randint(0,2000);_b=random.randint(0,2000)
   _c=random.uniform(0.5,2.5);_d=random.uniform(0.005,0.03)
   _e=random.randint(50,255);_f=random.uniform(0,6.28)
   _g=random.uniform(-0.3,0.3);_h=random.uniform(-0.3,0.3)
   _i=random.choice(['blue','white','gold','pink'])
   s.stars.append({'x':_a,'y':_b,'size':_c,'speed':_d,'brightness':_e,'phase':_f,'dx':_g,'dy':_h,'color':_i})
 def update(s):
  if not s.running:return
  s.canvas.delete("star")
  _a=s.canvas.winfo_width()or 900
  _b=s.canvas.winfo_height()or 700
  for _ in s.stars:
   _['x']+=_['dx'];_['y']+=_['dy'];_['phase']+=_['speed']
   if _['x']<0:_['x']=_a
   if _['x']>_a:_['x']=0
   if _['y']<0:_['y']=_b
   if _['y']>_b:_['y']=0
   _c=int(_['brightness']*(0.6+0.4*(_['phase']%1)))
   _d={'blue':f"#{min(255,_c):02x}{min(255,_c//3):02x}{min(255,_c):02x}",'white':f"#{min(255,_c):02x}{min(255,_c):02x}{min(255,_c):02x}",'gold':f"#{min(255,_c):02x}{min(255,_c//2):02x}{min(255,_c//4):02x}",'pink':f"#{min(255,_c):02x}{min(255,_c//3):02x}{min(255,_c//2):02x}"}
   _e=_d.get(_['color'],f"#{min(255,_c):02x}{min(255,_c//2):02x}{min(255,_c):02x}")
   _f=_['size'];_g=_f*2
   s.canvas.create_oval(_['x']-_g,_['y']-_g,_['x']+_g,_['y']+_g,fill='',outline=_e,width=0.5,tags="star",stipple="gray50")
   s.canvas.create_oval(_['x']-_f,_['y']-_f,_['x']+_f,_['y']+_f,fill=_e,outline='',tags="star")
  s.canvas.after(50,s.update)
 def stop(s):s.running=False

class _b39:
 def __init__(s):
  s.window=tk.Tk()
  s.window.title("🔐 АКТИВАЦИЯ")
  s.window.geometry("600x650")
  s.window.configure(bg='#0a0e27')
  s.window.resizable(False,False)
  s.window.protocol("WM_DELETE_WINDOW",sys.exit)
  s.window.update_idletasks()
  _a=600;_b=650
  _c=(s.window.winfo_screenwidth()//2)-(_a//2)
  _d=(s.window.winfo_screenheight()//2)-(_b//2)
  s.window.geometry(f'{_a}x{_b}+{_c}+{_d}')
  s.canvas=tk.Canvas(s.window,width=600,height=650,bg='#0a0e27',highlightthickness=0)
  s.canvas.pack(fill=tk.BOTH,expand=True)
  s.stars=_b38(s.canvas,100)
  s.stars.update()
  _e=tk.Frame(s.canvas,bg='#1a1f4a',width=580,height=600)
  _e.place(x=10,y=25)
  _f=tk.Frame(s.canvas,bg='#111638',width=580,height=600)
  _f.place(x=10,y=25)
  _g=tk.Frame(_f,bg='#6c5ce7',height=4)
  _g.pack(fill=tk.X,padx=0,pady=0)
  _h=tk.Frame(_f,bg='#111638')
  _h.pack(fill=tk.X,padx=30,pady=(20,5))
  tk.Label(_h,text="🔥 AWESOMETROLLING",font=("Segoe UI",26,"bold"),bg='#111638',fg='#ffd700').pack()
  tk.Label(_h,text="🔐 АКТИВАЦИЯ",font=("Segoe UI",12),bg='#111638',fg='#dfe6e9').pack()
  _i=tk.Frame(_f,bg='#1a1f4a')
  _i.pack(pady=10,padx=30,fill=tk.X)
  _i.config(height=80)
  _i.pack_propagate(False)
  _j=tk.Frame(_i,bg='#1a1f4a')
  _j.pack(fill=tk.BOTH,padx=15,pady=10)
  tk.Label(_j,text=f"💻 Компьютер: {os.environ.get('USERNAME','unknown')}",bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",11)).pack(anchor='w')
  tk.Label(_j,text=f"🆔 HWID: {_b20._i()[:24]}...",bg='#1a1f4a',fg='#b2bec3',font=("Segoe UI",9)).pack(anchor='w')
  _k=tk.Frame(_f,bg='#111638')
  _k.pack(pady=15,padx=30,fill=tk.BOTH,expand=True)
  tk.Label(_k,text="⚡ КУПИ ДОСТУП ⚡",font=("Segoe UI",20,"bold"),bg='#111638',fg='#ff6b35').pack()
  tk.Label(_k,text="У ВЛАДЕЛЬЦА",font=("Segoe UI",12),bg='#111638',fg='#dfe6e9').pack()
  _l=tk.Frame(_k,bg='#222860')
  _l.pack(pady=8,padx=20,fill=tk.X)
  _l.config(height=50)
  _l.pack_propagate(False)
  _m=tk.Frame(_l,bg='#222860')
  _m.pack(fill=tk.BOTH,padx=10,pady=5)
  tk.Label(_m,text="🔥 @flidges 🔥",font=("Segoe UI",16,"bold"),bg='#222860',fg='#ffd700').pack(side=tk.LEFT)
  tk.Label(_m,text="📩 Telegram",font=("Segoe UI",10),bg='#222860',fg='#4fc3f7').pack(side=tk.RIGHT)
  tk.Label(_k,text="💰 Цена - узнайте у @flidges",font=("Segoe UI",12,"bold"),bg='#111638',fg='#00ff88').pack(pady=5)
  _n=tk.Frame(_k,bg='#636e72',height=1,width=300)
  _n.pack(pady=10)
  _o=tk.Frame(_k,bg='#111638')
  _o.pack(pady=10,fill=tk.X)
  tk.Label(_o,text="Или введите ключ активации:",bg='#111638',fg='#b2bec3',font=("Segoe UI",10)).pack(anchor='w')
  _p=tk.Frame(_o,bg='#111638')
  _p.pack(fill=tk.X,pady=5)
  s.key_entry=tk.Entry(_p,bg='#1a1f4a',fg='#00ff88',font=("Segoe UI",14),relief=tk.FLAT,borderwidth=2,insertbackground='#dfe6e9')
  s.key_entry.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=(0,10))
  s.key_entry.bind('<Return>',lambda e:s._q())
  s.activate_btn=tk.Button(_p,text="✅ АКТИВИРОВАТЬ",command=s._q,bg='#6c5ce7',fg='white',font=("Segoe UI",10,"bold"),relief=tk.FLAT,cursor="hand2",padx=15,pady=8)
  s.activate_btn.pack(side=tk.RIGHT)
  s.status_frame=tk.Frame(_k,bg='#111638',height=50)
  s.status_frame.pack(fill=tk.X,pady=5)
  s.status_frame.pack_propagate(False)
  s.status_label=tk.Label(s.status_frame,text="",bg='#111638',fg='#e17055',font=("Segoe UI",11,"bold"))
  s.status_label.pack(fill=tk.BOTH,expand=True)
  _r=tk.Frame(_f,bg='#111638')
  _r.pack(side=tk.BOTTOM,fill=tk.X,pady=10)
  tk.Label(_r,text="© 2026 @flidges | Версия 3.0",bg='#111638',fg='#636e72',font=("Segoe UI",8)).pack()
  s.window.mainloop()
 def _q(s):
  _=s.key_entry.get().strip()
  if not _:
   s.status_label.config(text="❌ ВВЕДИТЕ КЛЮЧ!",fg='#e17055')
   return
  __,___=_b20._p(_)
  if __:
   s.status_label.config(text="✅ "+___,fg='#00b894')
   s.activate_btn.config(bg='#00b894',text="✅ АКТИВИРОВАНО!")
   s.window.after(1500,s._r)
  else:
   s.status_label.config(text="❌ "+___,fg='#e17055')
 def _r(s):
  if s.stars:s.stars.stop()
  s.window.destroy()
  _b40()

def _b40():
 _=tk.Tk()
 _.title("AWESOMETROLLING")
 _.geometry("900x700")
 _.configure(bg='#0a0e27')
 _.minsize(850,650)
 _.resizable(True,True)
 _.update_idletasks()
 _a=900;_b=700
 _c=(_.winfo_screenwidth()//2)-(_a//2)
 _d=(_.winfo_screenheight()//2)-(_b//2)
 _.geometry(f'{_a}x{_b}+{_c}+{_d}')
 _e=_b41(_)
 _.mainloop()

class _b41:
 def __init__(s,root):
  global _b31
  _b31=s
  s.root=root
  s.root.title("AWESOMETROLLING")
  s.root.geometry("900x700")
  s.root.configure(bg='#0a0e27')
  s.root.minsize(850,650)
  s.root.resizable(True,True)
  _=_b20._i()
  s.is_admin=False
  __=_b20._l()
  if __ and _b20._j(__):s.is_admin=True
  else:
   ___=_b20._b.execute('SELECT is_admin,is_owner FROM users WHERE hwid=?',(_a8(_),)).fetchone()
   if ___ and (___[0]==1 or ___[1]==1):s.is_admin=True
  s.canvas=tk.Canvas(s.root,bg='#0a0e27',highlightthickness=0)
  s.canvas.pack(fill=tk.BOTH,expand=True)
  s.stars=_b38(s.canvas,150)
  s.stars.update()
  _a=tk.Frame(s.canvas,bg='#111638',bd=2,relief=tk.FLAT)
  _a.place(relx=0.5,rely=0.5,anchor=tk.CENTER,width=860,height=660)
  s.main_frame=_a
  _b=tk.Frame(_a,bg='#111638',height=80)
  _b.pack(fill=tk.X,padx=0,pady=0)
  _b.pack_propagate(False)
  _c=tk.Frame(_b,bg='#111638')
  _c.pack(fill=tk.BOTH,padx=20,pady=10)
  tk.Label(_c,text="🔥 AWESOMETROLLING",font=("Segoe UI",26,"bold"),bg='#111638',fg='#ffd700').pack(side=tk.LEFT)
  tk.Label(_c,text="✨ Создатель: awesome / tg @flidges ✨",font=("Segoe UI",10),bg='#111638',fg='#ff6b35').pack(side=tk.RIGHT)
  _d=tk.Frame(_a,bg='#0a0e27')
  _d.pack(fill=tk.X,padx=0,pady=5)
  s.admin_btn=_b37(_d,text="⚙️ АДМИН-ПАНЕЛЬ (F6)",command=s._e,bg='#6c5ce7',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=14,pady=5)
  s.admin_btn.pack(side=tk.LEFT,padx=5)
  s.fs_btn=_b37(_d,text="⛶ ПОЛНЫЙ ЭКРАН (F11)",command=s._f,bg='#222860',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=14,pady=5)
  s.fs_btn.pack(side=tk.RIGHT,padx=5)
  s.logout_btn=_b37(_d,text="🚪 ВЫЙТИ (F9)",command=s._g,bg='#e17055',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=14,pady=5)
  s.logout_btn.pack(side=tk.RIGHT,padx=5)
  _h=tk.Frame(_a,bg='#0a0e27')
  _h.pack(pady=5)
  s.status_label=tk.Label(_h,text="⏸️ Ожидание...",bg='#0a0e27',fg='#fdcb6e',font=("Segoe UI",13,"bold"))
  s.status_label.pack(side=tk.LEFT,padx=10)
  s.count_label=tk.Label(_h,text="📨 0",bg='#0a0e27',fg='#00ff88',font=("Segoe UI",13,"bold"))
  s.count_label.pack(side=tk.LEFT,padx=10)
  s.preview=scrolledtext.ScrolledText(_a,height=8,bg='#1a1f4a',fg='#dfe6e9',insertbackground='white',font=("Segoe UI",10),relief=tk.FLAT,borderwidth=2,padx=15,pady=15)
  s.preview.pack(padx=10,pady=5,fill=tk.BOTH,expand=True)
  s.preview.insert("1.0","🔥 AWESOMETROLLING\n\n╔══════════════════════════════════════════════════════════════╗\n║  🎯 F3 → СТАРТ    🛑 F4 → СТОП    ⏸️ F5 → ПАУЗА           ║\n║  ⚙️ F6 → АДМИН-ПАНЕЛЬ    ⛶ F11 → ПОЛНЫЙ ЭКРАН              ║\n║  ❌ F9 → ВЫХОД                                             ║\n╚══════════════════════════════════════════════════════════════╝\n\n✅ Каждое сообщение уникально\n✅ Длинные связные предложения\n✅ 60+ шаблонов\n✅ Работает даже при свёрнутом окне\n✅ Автовход по ключу")
  s.preview.config(state=tk.DISABLED)
  _i=tk.Frame(_a,bg='#0a0e27')
  _i.pack(pady=8)
  s.start_btn=_b37(_i,text="🤖 СТАРТ (F3)",command=s._j,bg='#00b894',fg='#dfe6e9',font=("Segoe UI",10,"bold"),width=16,padx=5,pady=8)
  s.start_btn.pack(side=tk.LEFT,padx=5)
  s.stop_btn=_b37(_i,text="🛑 СТОП (F4)",command=s._k,bg='#e17055',fg='#dfe6e9',font=("Segoe UI",10,"bold"),width=16,padx=5,pady=8)
  s.stop_btn.pack(side=tk.LEFT,padx=5)
  s.pause_btn=_b37(_i,text="⏸️ ПАУЗА (F5)",command=s._l,bg='#6c5ce7',fg='#dfe6e9',font=("Segoe UI",10,"bold"),width=16,padx=5,pady=8)
  s.pause_btn.pack(side=tk.LEFT,padx=5)
  _m=tk.Frame(_a,bg='#0a0e27')
  _m.pack(pady=5)
  tk.Label(_m,text="F3-СТАРТ | F4-СТОП | F5-ПАУЗА | F6-АДМИН | F9-ВЫХОД | F11-ПОЛНЫЙ ЭКРАН",bg='#0a0e27',fg='#b2bec3',font=("Segoe UI",9)).pack()
  tk.Label(_m,text="💜 Сделано с любовью и матом 💜",bg='#0a0e27',fg='#fd79a8',font=("Segoe UI",10,"bold")).pack()
  s.admin_panel=_b42(s.root,s.is_admin)
  s.fullscreen=False
  s._n()
  s._o()
 def _e(s):s.admin_panel.toggle()
 def _f(s):
  s.fullscreen=not s.fullscreen
  s.root.attributes('-fullscreen',s.fullscreen)
  if s.fullscreen:s.fs_btn.config(text="⛶ ОКОННЫЙ РЕЖИМ (F11)",bg='#fdcb6e')
  else:s.fs_btn.config(text="⛶ ПОЛНЫЙ ЭКРАН (F11)",bg='#222860')
 def _n(s):
  try:
   keyboard.add_hotkey('f3',s._j)
   keyboard.add_hotkey('f4',s._k)
   keyboard.add_hotkey('f5',s._l)
   keyboard.add_hotkey('f6',s._e)
   keyboard.add_hotkey('f9',s._p)
   keyboard.add_hotkey('f11',s._f)
  except:pass
 def _j(s):_b34();s.uis()
 def _k(s):_b35();s.uis()
 def _l(s):_b36();s.uis()
 def _g(s):
  if messagebox.askyesno("Выход из аккаунта","Вы уверены, что хотите выйти?"):
   _b20._m()
   if s.stars:s.stars.stop()
   s.root.destroy()
   _b43()
 def _p(s):
  _b35()
  if s.stars:s.stars.stop()
  s.root.quit()
  s.root.destroy()
  sys.exit()
 def uc(s):
  try:s.count_label.config(text=f"📨 {_b27}")
  except:pass
 def uis(s):
  try:
   if _b28:
    s.status_label.config(text="⏸️ ПАУЗА",fg='#fdcb6e')
    s.pause_btn.config(text="▶️ ВОЗОБНОВИТЬ (F5)",bg='#fdcb6e')
   elif not _b25 and _b26 and _b26.is_alive():
    s.status_label.config(text="🧠 ГЕНЕРАЦИЯ",fg='#00b894')
    s.start_btn.config(bg='#222860',text="🧠 РАБОТАЕТ...")
    s.pause_btn.config(text="⏸️ ПАУЗА (F5)",bg='#6c5ce7')
   else:
    s.status_label.config(text="⏸️ Остановлено",fg='#b2bec3')
    s.start_btn.config(bg='#00b894',text="🤖 СТАРТ (F3)")
    s.pause_btn.config(text="⏸️ ПАУЗА (F5)",bg='#6c5ce7')
  except:pass
 def _o(s):
  s.uis()
  s.count_label.config(text=f"📨 {_b27}")
  s.root.after(500,s._o)

class _b42:
 def __init__(s,parent,is_admin=False):
  s.parent=parent
  s.is_admin=is_admin
  s.window=None
  s.is_open=False
  s.sut=None
  s.cp()
 def cp(s):
  s.window=tk.Toplevel(s.parent)
  s.window.title("✨ АДМИН-ПАНЕЛЬ")
  s.window.geometry("950x750")
  s.window.configure(bg='#0a0e27')
  s.window.minsize(850,650)
  s.window.protocol("WM_DELETE_WINDOW",s.hide)
  s.window.bind('<Escape>',lambda e:s.hide())
  s.window.withdraw()
  s.window.update_idletasks()
  _a=950;_b=750
  _c=(s.window.winfo_screenwidth()//2)-(_a//2)
  _d=(s.window.winfo_screenheight()//2)-(_b//2)
  s.window.geometry(f'{_a}x{_b}+{_c}+{_d}')
  _e=tk.Canvas(s.window,bg='#0a0e27',highlightthickness=0)
  _e.pack(fill=tk.BOTH,expand=True)
  s.admin_stars=_b38(_e,100)
  s.admin_stars.update()
  _f=tk.Frame(_e,bg='#111638',bd=2,relief=tk.FLAT)
  _f.place(relx=0.5,rely=0.5,anchor=tk.CENTER,width=910,height=710)
  _g=tk.Frame(_f,bg='#111638',height=60)
  _g.pack(fill=tk.X,padx=0,pady=0)
  _g.pack_propagate(False)
  _h=tk.Frame(_g,bg='#111638')
  _h.pack(fill=tk.BOTH,padx=20,pady=10)
  tk.Label(_h,text="✨ АДМИН-ПАНЕЛЬ",font=("Segoe UI",22,"bold"),bg='#111638',fg='#ffd700').pack(side=tk.LEFT)
  tk.Label(_h,text="⭐ @flidges",font=("Segoe UI",12),bg='#111638',fg='#ff6b35').pack(side=tk.RIGHT)
  _i=tk.Frame(_f,bg='#00ff88',height=3)
  _i.pack(fill=tk.X,padx=0)
  s.notebook=ttk.Notebook(_f)
  s.notebook.pack(fill=tk.BOTH,expand=True,padx=15,pady=10)
  _j=ttk.Style()
  _j.theme_use('clam')
  _j.configure('TNotebook',background='#0a0e27',borderwidth=0)
  _j.configure('TNotebook.Tab',background='#111638',foreground='#dfe6e9',padding=[20,8],font=("Segoe UI",10,"bold"))
  _j.map('TNotebook.Tab',background=[('selected','#6c5ce7')])
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
  _=s.tab_main
  _a=tk.Frame(_,bg='#0a0e27')
  _a.pack(pady=10,padx=20,fill=tk.X)
  tk.Label(_a,text="🚀 Скорость отправки",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#a29bfe').pack(anchor='w')
  _b=tk.Frame(_a,bg='#0a0e27')
  _b.pack(fill=tk.X,pady=5)
  s.speed_slider=tk.Scale(_b,from_=0.001,to=0.45,resolution=0.001,orient=tk.HORIZONTAL,length=500,bg='#0a0e27',fg='#dfe6e9',troughcolor='#1a1f4a',sliderlength=22,highlightthickness=0)
  s.speed_slider.set(_b32)
  s.speed_slider.pack(side=tk.LEFT,fill=tk.X,expand=True)
  s.speed_label=tk.Label(_b,text=f"{_b32:.3f}с",bg='#0a0e27',fg='#ffd700',font=("Segoe UI",18,"bold"),width=8)
  s.speed_label.pack(side=tk.LEFT,padx=10)
  def _c(val):
   _d=float(val)
   s.speed_label.config(text=f"{_d:.3f}с")
   if s.sut:s.window.after_cancel(s.sut)
   def _e():
    global _b32
    _b32=_d
    settings['spam_speed']=_d
    _b44(settings)
   s.sut=s.window.after(300,_e)
  s.speed_slider.config(command=_c)
  _f=tk.Frame(_,bg='#0a0e27')
  _f.pack(pady=5,padx=20,fill=tk.X)
  tk.Label(_f,text="⚡ Быстрые пресеты",font=("Segoe UI",11,"bold"),bg='#0a0e27',fg='#b2bec3').pack(anchor='w')
  _g=tk.Frame(_f,bg='#0a0e27')
  _g.pack(fill=tk.X,pady=5)
  for _h,_i in [("🐢 0.1с",0.1),("🚶 0.05с",0.05),("🏃 0.02с",0.02),("🚀 0.005с",0.005),("🔥 0.001с",0.001)]:
   _j=_b37(_g,text=_h,command=lambda sp=_i:s._k(sp),bg='#222860',fg='#dfe6e9',font=("Segoe UI",9,"bold"),padx=14,pady=6)
   _j.pack(side=tk.LEFT,padx=3)
  _l=tk.Frame(_,bg='#0a0e27')
  _l.pack(pady=15,padx=20,fill=tk.BOTH,expand=True)
  tk.Label(_l,text="📊 Живая статистика",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#00ff88').pack(anchor='w')
  s.info_text=tk.Text(_l,height=8,bg='#111638',fg='#dfe6e9',font=("Consolas",10),relief=tk.FLAT,borderwidth=2,padx=15,pady=12)
  s.info_text.pack(fill=tk.BOTH,expand=True,pady=5)
  s.info_text.insert("1.0","⏳ Ожидание запуска...")
  s.info_text.config(state=tk.DISABLED)
  _m=tk.Frame(_,bg='#0a0e27')
  _m.pack(pady=10)
  for _n,_o in [("🔄 Обновить",s.ui),("🧹 Сбросить счётчик",s.rc)]:
   _p=_b37(_m,text=_n,command=_o,bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",10,"bold"),padx=18,pady=6)
   _p.pack(side=tk.LEFT,padx=5)
 def cat(s):
  _=s.tab_about
  _a=tk.Frame(_,bg='#0a0e27')
  _a.pack(fill=tk.BOTH,expand=True,padx=40,pady=40)
  tk.Label(_a,text="🔥",font=("Segoe UI",70),bg='#0a0e27').pack(pady=5)
  tk.Label(_a,text="AWESOMETROLLING",font=("Segoe UI",26,"bold"),bg='#0a0e27',fg='#ffd700').pack(pady=5)
  tk.Label(_a,text="✨ Версия 3.0 ✨",font=("Segoe UI",14),bg='#0a0e27',fg='#b2bec3').pack(pady=5)
  _b=tk.Frame(_a,bg='#00ff88',height=2,width=350)
  _b.pack(pady=15)
  tk.Label(_a,text="👨‍💻 РАЗРАБОТЧИК",font=("Segoe UI",13,"bold"),bg='#0a0e27',fg='#dfe6e9').pack()
  tk.Label(_a,text="@flidges",font=("Segoe UI",20,"bold"),bg='#0a0e27',fg='#fd79a8').pack(pady=3)
  tk.Label(_a,text="✨ Создатель: awesome / tg @flidges ✨",font=("Segoe UI",12),bg='#0a0e27',fg='#ffd700').pack(pady=5)
  tk.Label(_a,text="💰 Цена - узнайте у @flidges",font=("Segoe UI",12,"bold"),bg='#0a0e27',fg='#00ff88').pack(pady=5)
  _c=tk.Frame(_a,bg='#6c5ce7',height=1,width=250)
  _c.pack(pady=10)
  for _d in ["🔥 Каждое сообщение уникально","💎 Длинные связные предложения","📚 60+ шаблонов","⚡ Работает при свёрнутом окне","🔒 Защита HWID","💾 Автосохранение ключа"]:
   tk.Label(_a,text=_d,font=("Segoe UI",11),bg='#0a0e27',fg='#00ff88').pack(pady=2)
  _e=tk.Frame(_a,bg='#6c5ce7',height=1,width=200)
  _e.pack(pady=10)
  tk.Label(_a,text="💜 Сделано с любовью и матом 💜",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#fd79a8').pack(pady=5)
  tk.Label(_a,text="© 2026 Все права защищены 🚀",font=("Segoe UI",9),bg='#0a0e27',fg='#636e72').pack(pady=5)
 def cut(s):
  if not s.is_admin:return
  _=s.tab_users
  _a=tk.Frame(_,bg='#0a0e27')
  _a.pack(pady=10,padx=20,fill=tk.X)
  tk.Label(_a,text="👥 Управление пользователями",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#ffd700').pack(anchor='w')
  _b=tk.Frame(_a,bg='#0a0e27')
  _b.pack(fill=tk.X,pady=5)
  s.user_entry=tk.Entry(_b,bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",11),relief=tk.FLAT,borderwidth=2,width=20)
  s.user_entry.pack(side=tk.LEFT,padx=5)
  s.user_entry.insert(0,"Имя пользователя")
  s.user_entry.bind('<FocusIn>',lambda e:s.user_entry.delete(0,tk.END))
  _c=tk.StringVar(value="1")
  _d=ttk.Combobox(_b,textvariable=_c,values=["1","3","6","12","24"],width=5,state="readonly")
  _d.pack(side=tk.LEFT,padx=5)
  tk.Label(_b,text="мес.",bg='#0a0e27',fg='#b2bec3').pack(side=tk.LEFT)
  tk.Button(_b,text="✅ ВЫДАТЬ",command=lambda:s._e(_c.get()),bg='#00b894',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
  tk.Button(_b,text="🚫 ЗАБРАТЬ",command=s._f,bg='#e17055',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
  tk.Button(_b,text="🔄 ПРОДЛИТЬ",command=lambda:s._g(_c.get()),bg='#6c5ce7',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
  _h=tk.Frame(_,bg='#0a0e27')
  _h.pack(pady=10,padx=20,fill=tk.BOTH,expand=True)
  _i=("Имя","Статус","Бан","До","Ключ","HWID")
  s.tree=ttk.Treeview(_h,columns=_i,show="headings",height=12)
  for _j in _i:
   s.tree.heading(_j,text=_j)
   s.tree.column(_j,width=100)
  s.tree.column("HWID",width=120)
  _k=ttk.Scrollbar(_h,orient=tk.VERTICAL,command=s.tree.yview)
  s.tree.configure(yscrollcommand=_k.set)
  s.tree.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
  _k.pack(side=tk.RIGHT,fill=tk.Y)
  tk.Label(_,text="💡 Двойной клик по пользователю → бан/разбан",bg='#0a0e27',fg='#b2bec3',font=("Segoe UI",9)).pack(pady=5)
  s.ru()
 def ckt(s):
  if not s.is_admin:return
  _=s.tab_keys
  _a=tk.Frame(_,bg='#0a0e27')
  _a.pack(pady=10,padx=20,fill=tk.X)
  tk.Label(_a,text="🔑 Управление ключами",font=("Segoe UI",14,"bold"),bg='#0a0e27',fg='#ffd700').pack(anchor='w')
  _b=tk.Frame(_a,bg='#0a0e27')
  _b.pack(fill=tk.X,pady=5)
  tk.Label(_b,text="Ключ:",bg='#0a0e27',fg='#dfe6e9',font=("Segoe UI",10)).pack(side=tk.LEFT,padx=5)
  s.key_entry=tk.Entry(_b,bg='#1a1f4a',fg='#dfe6e9',font=("Segoe UI",11),relief=tk.FLAT,borderwidth=2,width=20)
  s.key_entry.pack(side=tk.LEFT,padx=5)
  s.key_entry.insert(0,"Введите ключ")
  s.key_entry.bind('<FocusIn>',lambda e:s.key_entry.delete(0,tk.END)if s.key_entry.get()=="Введите ключ"else None)
  tk.Label(_b,text="мес:",bg='#0a0e27',fg='#dfe6e9',font=("Segoe UI",10)).pack(side=tk.LEFT,padx=5)
  s.key_months=ttk.Combobox(_b,values=["1","3","6","12","24"],width=5,state="readonly")
  s.key_months.set("1")
  s.key_months.pack(side=tk.LEFT,padx=5)
  tk.Button(_b,text="➕ ДОБАВИТЬ КЛЮЧ",command=s._h,bg='#00b894',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
  tk.Button(_b,text="🎲 СГЕНЕРИРОВАТЬ",command=s._i,bg='#6c5ce7',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT,padx=5)
  _j=tk.Frame(_,bg='#0a0e27')
  _j.pack(pady=10,padx=20,fill=tk.BOTH,expand=True)
  _k=("Ключ","Создан","До","Использован","Кем","HWID")
  s.keys_tree=ttk.Treeview(_j,columns=_k,show="headings",height=10)
  for _l in _k:
   s.keys_tree.heading(_l,text=_l)
   s.keys_tree.column(_l,width=100)
  s.keys_tree.column("HWID",width=100)
  _m=ttk.Scrollbar(_j,orient=tk.VERTICAL,command=s.keys_tree.yview)
  s.keys_tree.configure(yscrollcommand=_m.set)
  s.keys_tree.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
  _m.pack(side=tk.RIGHT,fill=tk.Y)
  _n=tk.Frame(_,bg='#0a0e27')
  _n.pack(pady=5,padx=20,fill=tk.X)
  tk.Button(_n,text="🗑 УДАЛИТЬ ВЫБРАННЫЙ КЛЮЧ",command=s._j,bg='#e17055',fg='white',font=("Segoe UI",9,"bold"),relief=tk.FLAT,cursor="hand2",padx=10,pady=5).pack(side=tk.LEFT)
  tk.Label(_n,text="💡 Выберите ключ в списке и нажмите УДАЛИТЬ",bg='#0a0e27',fg='#b2bec3',font=("Segoe UI",9)).pack(side=tk.LEFT,padx=10)
  s.rk()
 def cst(s):
  if not s.is_admin:return
  _=s.tab_stats
  _a=tk.Frame(_,bg='#0a0e27')
  _a.pack(fill=tk.BOTH,expand=True,padx=20,pady=20)
  tk.Label(_a,text="📈 ДЕТАЛЬНАЯ СТАТИСТИКА",font=("Segoe UI",18,"bold"),bg='#0a0e27',fg='#ffd700').pack(pady=10)
  s.stats_text=tk.Text(_a,height=14,bg='#111638',fg='#dfe6e9',font=("Consolas",11),relief=tk.FLAT,borderwidth=2,padx=20,pady=15)
  s.stats_text.pack(fill=tk.BOTH,expand=True,pady=10)
  s.stats_text.config(state=tk.DISABLED)
  _b=tk.Frame(_a,bg='#0a0e27')
  _b.pack(pady=10)
  tk.Button(_b,text="🔄 ОБНОВИТЬ",command=s._k,bg='#6c5ce7',fg='white',font=("Segoe UI",10,"bold"),relief=tk.FLAT,cursor="hand2",padx=20,pady=8).pack()
  s._k()
 def _k(s,speed):
  global _b32
  _b32=speed
  s.speed_slider.set(speed)
  s.speed_label.config(text=f"{speed:.3f}с")
  settings['spam_speed']=speed
  _b44(settings)
 def _e(s,months):
  if not s.is_admin:
   messagebox.showwarning("Доступ запрещен","Только для администраторов!")
   return
  _=s.user_entry.get().strip()
  if not _ or _=="Имя пользователя":
   messagebox.showerror("Ошибка","Введите имя пользователя!")
   return
  __,___=_b20._u(_,int(months))
  if __:
   messagebox.showinfo("Успех",___)
   s.ru()
  else:messagebox.showerror("Ошибка",___)
 def _f(s):
  if not s.is_admin:
   messagebox.showwarning("Доступ запрещен","Только для администраторов!")
   return
  _=s.user_entry.get().strip()
  if not _ or _=="Имя пользователя":
   messagebox.showerror("Ошибка","Введите имя пользователя!")
   return
  if messagebox.askyesno("Подтверждение",f"Забрать доступ у {_}?"):
   _b20._v(_)
   messagebox.showinfo("Успех",f"Доступ у {_} забран!")
   s.ru()
 def _g(s,months):
  if not s.is_admin:
   messagebox.showwarning("Доступ запрещен","Только для администраторов!")
   return
  _=s.user_entry.get().strip()
  if not _ or _=="Имя пользователя":
   messagebox.showerror("Ошибка","Введите имя пользователя!")
   return
  __,___=_b20._x(_,int(months))
  if __:
   messagebox.showinfo("Успех",___)
   s.ru()
  else:messagebox.showerror("Ошибка",___)
 def _h(s):
  if not s.is_admin:
   messagebox.showwarning("Доступ запрещен","Только для администраторов!")
   return
  _=s.key_entry.get().strip().upper()
  __=int(s.key_months.get())
  if not _ or _=="ВВЕДИТЕ КЛЮЧ":
   messagebox.showerror("Ошибка","Введите ключ!")
   return
  ___,____=_b20._n(__,_)
  if ___:
   messagebox.showinfo("Успех",f"🔑 Ключ {_} добавлен на {__} месяцев!")
   s.rk()
   s.key_entry.delete(0,tk.END)
   s.key_entry.insert(0,"Введите ключ")
  else:messagebox.showerror("Ошибка","Такой ключ уже существует!")
 def _i(s):
  if not s.is_admin:
   messagebox.showwarning("Доступ запрещен","Только для администраторов!")
   return
  _=int(s.key_months.get())
  __,___=_b20._n(_)
  if __:
   messagebox.showinfo("Ключ сгенерирован",f"🔑 Ключ: {___}\n📅 Действует: {_} месяцев\n📩 Отправь его покупателю!\n⚠️ Ключ привяжется к первому компьютеру!")
   s.rk()
 def _j(s):
  if not s.is_admin:
   messagebox.showwarning("Доступ запрещен","Только для администраторов!")
   return
  _=s.keys_tree.selection()
  if not _:
   messagebox.showerror("Ошибка","Выберите ключ для удаления!")
   return
  __=_[0]
  ___=s.keys_tree.item(__,'values')
  ____=___[0]
  if messagebox.askyesno("Подтверждение",f"Удалить ключ {____}?"):
   _b20._o(____)
   messagebox.showinfo("Успех",f"Ключ {____} удален!")
   s.rk()
 def ru(s):
  if not s.is_admin:return
  for _ in s.tree.get_children():s.tree.delete(_)
  _a=_b20._s()
  for _b in _a:
   _c,_d,_e,_f,_g,_h,_i=_b
   if _g:
    try:_j=datetime.fromisoformat(_g).strftime('%d.%m.%Y')
    except:_j="Ошибка"
   else:_j="-"
   _k="👑"if _d else("⭐"if _e else"👤")
   _l="🚫"if _f else"✅"
   _m=_h[:12]+"..."if _h else"-"
   _n=_i[:8]+"..."if _i else"-"
   s.tree.insert("",tk.END,values=(_c,_k,_l,_j,_n,_m),tags=(_c,_f))
  s.tree.bind('<Double-Button-1>',s._o)
 def _o(s,e):
  if not s.is_admin:return
  _=s.tree.selection()
  if not _:return
  __=_[0]
  ___=s.tree.item(__,'values')
  ____=___[0]
  _____=___[2]=="🚫"
  ______=___[1]=="👑"
  if ______:
   messagebox.showinfo("Инфо","Нельзя изменять овнера!")
   return
  if _____:
   if messagebox.askyesno("Восстановить",f"Разбанить {____}?"):
    _b20._w(____)
    messagebox.showinfo("Успех",f"{____} разбанен!")
    s.ru()
  else:
   if messagebox.askyesno("Забанить",f"Забанить {____}?"):
    _b20._v(____)
    messagebox.showinfo("Успех",f"{____} забанен!")
    s.ru()
 def rk(s):
  if not s.is_admin:return
  for _ in s.keys_tree.get_children():s.keys_tree.delete(_)
  _a=_b20._t()
  for _b in _a:
   _c,_d,_e,_f,_g,_h,_i=_b
   try:_j=datetime.fromisoformat(_d).strftime('%d.%m')if _d else"-"
   except:_j="-"
   try:_k=datetime.fromisoformat(_e).strftime('%d.%m.%Y')if _e else"-"
   except:_k="-"
   _l="✅"if _h else"🔓"
   _m=_f if _f else"-"
   _n=_g[:12]+"..."if _g else"-"
   s.keys_tree.insert("",tk.END,values=(_c,_j,_k,_l,_m,_n))
 def _k(s):
  if not s.is_admin:return
  _a=_b20._s()
  _b=_b20._t()
  _c=f"""
╔══════════════════════════════════════════════════════════════╗
║                      📊 СТАТИСТИКА                          ║
╠══════════════════════════════════════════════════════════════╣
║  👥 Всего пользователей: {len(_a):>4}                                     ║
║  👑 Овнеров:             {sum(1 for u in _a if u[1]):>4}                                     ║
║  ⭐ Админов:             {sum(1 for u in _a if u[2]):>4}                                     ║
║  🚫 Забаненных:          {sum(1 for u in _a if u[3]):>4}                                     ║
║  ✅ Активных:            {sum(1 for u in _a if not u[3]):>4}                                     ║
╠══════════════════════════════════════════════════════════════╣
║  🔑 Всего ключей:        {len(_b):>4}                                     ║
║  ✅ Использованных:      {sum(1 for k in _b if k[5]):>4}                                     ║
║  🔓 Свободных:           {len(_b) - sum(1 for k in _b if k[5]):>4}                                     ║
╚══════════════════════════════════════════════════════════════╝
"""
  s.stats_text.config(state=tk.NORMAL)
  s.stats_text.delete("1.0",tk.END)
  s.stats_text.insert("1.0",_c)
  s.stats_text.config(state=tk.DISABLED)
 def ui(s):
  global _b27,_b29,_b30
  _a="0с"
  if _b30:
   _b=int(time.time()-_b30)
   _c=_b//60;_b%=60
   _d=_c//60;_c%=60
   if _d>0:_a=f"{_d}ч {_c}м {_b}с"
   elif _c>0:_a=f"{_c}м {_b}с"
   else:_a=f"{_b}с"
  _e="⏸️ Остановлено"
  if not _b25 and _b26 and _b26.is_alive():
   if _b28:_e="⏸️ ПАУЗА"
   else:_e="🧠 АКТИВЕН"
  _f=f"""
╔══════════════════════════════════════════════════════╗
║  📊 СТАТИСТИКА              Статус: {_e:<10} ║
╠══════════════════════════════════════════════════════╣
║  📨 За сессию: {_b27:>6}                                  ║
║  📨 Всего:      {_b29:>6}                                  ║
║  ⏱ Время:      {_a:>10}                              ║
║  🚀 Скорость:  {_b32:.3f}с                                   ║
║  📝 Шаблонов:  {len(_INSULT_TEMPLATES):>6}                                  ║
║  🚫 Забанено:  {len(settings.get('banned_words',[])):>6}                                  ║
║  ⭐ Dev:       @flidges                              ║
╚══════════════════════════════════════════════════════╝
"""
  s.info_text.config(state=tk.NORMAL)
  s.info_text.delete("1.0",tk.END)
  s.info_text.insert("1.0",_f)
  s.info_text.config(state=tk.DISABLED)
 def rc(s):
  global _b27,_b29
  _b27=0;_b29=0
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

def _b44(settings_data):
 try:
  _={}
  for __,___ in settings_data.items():
   if isinstance(___,(str,int,float,bool)):
    _[__]=_a8(str(___))
   else:_[__]=___
  with open(os.path.join(_b16,"troll_settings.json"),'w',encoding='utf-8')as ____:
   json.dump(_,____,ensure_ascii=False,indent=2)
 except:pass

def _b43():
 try:ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
 except:pass
 _=tk.Tk()
 _.title("🔐 АКТИВАЦИЯ")
 _.geometry("450x350")
 _.configure(bg='#0a0e27')
 tk.Label(_,text="🔥 AWESOMETROLLING",font=("Segoe UI",24,"bold"),bg='#0a0e27',fg='#ffd700').pack(pady=20)
 tk.Label(_,text="ВВЕДИТЕ КЛЮЧ",font=("Segoe UI",14),bg='#0a0e27',fg='#dfe6e9').pack(pady=5)
 __=tk.Entry(_,font=("Segoe UI",14),bg='#1a1f4a',fg='#00ff88',relief=tk.FLAT,borderwidth=2)
 __.pack(pady=10,padx=40,fill=tk.X)
 __.focus()
 ___.pack()
 def ____():
  _____=__.get().strip()
  if not _____:
   ___.config(text="❌ ВВЕДИТЕ КЛЮЧ!",fg='#e17055')
   return
  ______,_______=_b20._p(_____)
  if ______:
   ___.config(text="✅ "+_______,fg='#00b894')
   _.after(1500,lambda:[_.destroy(),_b40()])
  else:
   ___.config(text="❌ "+_______,fg='#e17055')
 tk.Button(_,text="АКТИВИРОВАТЬ",command=____,bg='#6c5ce7',fg='white',font=("Segoe UI",10,"bold"),relief=tk.FLAT,cursor="hand2",padx=20,pady=10).pack(pady=10)
 _.bind('<Return>',lambda e:____())
 _.mainloop()

if __name__=="__main__":
 try:ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
 except:pass
 _a,_b=_b20._q()
 if _a:_b40()
 else:
  _a,_b=_b20._r()
  if _a:_b40()
  else:_b43()
