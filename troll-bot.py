import asyncio
import logging
import sqlite3
import random
import string
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ============================================================
# НАСТРОЙКИ — ТУТ ВСЁ МЕНЯЕШЬ
# ============================================================
BOT_TOKEN = "8935419647:AAF6qouUbEovd0SofKG_srXXwNlBpbRZSLY"  # ← СЮДА НОВЫЙ ТОКЕН!
ADMIN_IDS = [6652898792]  # ТВОЙ TELEGRAM ID
PRICE = 50  # ЦЕНА В РУБЛЯХ

# ============================================================
# БАЗА ДАННЫХ (ОБЩАЯ С ПРОГРАММОЙ!)
# ============================================================
DB_FILE = "troll_users.db"  # ← ОБЩАЯ БАЗА С EXE!

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Таблица пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            is_admin INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            created_at TEXT,
            expires_at TEXT,
            last_active TEXT
        )
    ''')
    
    # Таблица ключей (ОБЩАЯ С EXE!)
    c.execute('''
        CREATE TABLE IF NOT EXISTS license_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_text TEXT UNIQUE NOT NULL,
            created_at TEXT,
            expires_at TEXT,
            used_by TEXT,
            used_hwid TEXT,
            used_at TEXT,
            is_used INTEGER DEFAULT 0,
            telegram_id INTEGER
        )
    ''')
    
    # Таблица заказов
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            key_text TEXT,
            price INTEGER,
            months INTEGER,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    ''')
    
    # Таблица логов
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

def get_db():
    return sqlite3.connect(DB_FILE)

# ============================================================
# ФУНКЦИИ
# ============================================================

def generate_key(months=1, telegram_id=None):
    """Генерация ключа"""
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    created_at = datetime.now().isoformat()
    expires_at = (datetime.now() + timedelta(days=30 * months)).isoformat()
    
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO license_keys (key_text, created_at, expires_at, is_used, telegram_id)
            VALUES (?, ?, ?, 0, ?)
        ''', (key, created_at, expires_at, telegram_id))
        conn.commit()
        conn.close()
        return key
    except:
        conn.close()
        return None

def activate_key_in_db(key, telegram_id, username):
    """Активация ключа в БД"""
    conn = get_db()
    c = conn.cursor()
    
    # Проверяем ключ
    result = c.execute('''
        SELECT key_text, expires_at, is_used FROM license_keys WHERE key_text = ?
    ''', (key,)).fetchone()
    
    if not result:
        conn.close()
        return False, "❌ Ключ не найден!"
    
    key_text, expires_at, is_used = result
    
    if is_used:
        conn.close()
        return False, "❌ Ключ уже использован!"
    
    expiry = datetime.fromisoformat(expires_at)
    if datetime.now() > expiry:
        conn.close()
        return False, "❌ Ключ истек!"
    
    # Активируем ключ
    c.execute('''
        UPDATE license_keys SET used_by = ?, used_at = ?, is_used = 1 WHERE key_text = ?
    ''', (username, datetime.now().isoformat(), key))
    
    # Добавляем пользователя
    c.execute('''
        INSERT OR REPLACE INTO users (telegram_id, username, first_name, expires_at, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (telegram_id, username, username, expires_at, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    return True, f"✅ Ключ активирован до {expiry.strftime('%d.%m.%Y')}!"

# ============================================================
# СОСТОЯНИЯ
# ============================================================
class LicenseStates(StatesGroup):
    waiting_for_license = State()
    waiting_for_keygen = State()

# ============================================================
# БОТ
# ============================================================
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

# ============================================================
# КЛАВИАТУРЫ
# ============================================================
def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Купить доступ (50₽/мес)", callback_data="buy")],
        [InlineKeyboardButton(text="🔑 Активировать ключ", callback_data="activate")],
        [InlineKeyboardButton(text="📊 Мой статус", callback_data="status")],
        [InlineKeyboardButton(text="📥 Скачать программу", callback_data="download")],
        [InlineKeyboardButton(text="📩 Поддержка", url="https://t.me/flidges")],
        [InlineKeyboardButton(text="📝 О программе", callback_data="about")]
    ])

def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="🔑 Создать ключ", callback_data="admin_gen")],
        [InlineKeyboardButton(text="📋 Все ключи", callback_data="admin_keys")],
        [InlineKeyboardButton(text="📊 Логи", callback_data="admin_logs")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])

def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])

def payment_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплата картой", callback_data="pay_card")],
        [InlineKeyboardButton(text="₿ Криптовалюта", callback_data="pay_crypto")],
        [InlineKeyboardButton(text="💸 Другой способ", callback_data="pay_other")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])

# ============================================================
# КОМАНДЫ
# ============================================================
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "без username"
    first_name = message.from_user.first_name or "User"
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO users (telegram_id, username, first_name, created_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    text = f"""🔥 <b>AWESOMETROLLING</b> — Нейросетевой троллинг 1Х1

🎯 <b>Что умеет:</b>
✅ Генерирует уникальные оскорбления
✅ 60+ шаблонов
✅ Работает при свёрнутом окне
✅ Защита HWID
✅ Каждое сообщение уникально

💎 <b>Цена: {PRICE}₽/месяц</b>

📩 <b>Как получить доступ:</b>
1. Нажми "Купить доступ"
2. Выбери способ оплаты
3. Получи ключ
4. Скачай программу
5. Введи ключ

👨‍💻 Разработчик: @flidges
"""
    await message.answer(text, reply_markup=main_keyboard(), parse_mode="HTML")

@dp.callback_query(F.data == "menu")
async def menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔥 <b>AWESOMETROLLING</b> — Главное меню",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    text = f"""🔥 <b>AWESOMETROLLING</b>

<b>Версия:</b> 3.0
<b>Разработчик:</b> @flidges

<b>Особенности:</b>
✅ Уникальные сообщения
✅ 60+ шаблонов
✅ Автовход по ключу
✅ Защита HWID
✅ Работает при свёрнутом окне

<b>Цена:</b> {PRICE}₽/месяц

<b>Горячие клавиши:</b>
F3 — Старт
F4 — Стоп
F5 — Пауза
F6 — Админ-панель
F11 — Полный экран
"""
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "download")
async def download(callback: types.CallbackQuery):
    text = """📥 <b>Скачать AWESOMETROLLING</b>

🔗 <a href="https://github.com/awesome371828/awesomeotroll/releases/download/latest/AWESOMETROLLING.exe">Скачать программу</a>

📌 <b>Инструкция:</b>
1. Скачай файл
2. Запусти AWESOMETROLLING.exe
3. Введи ключ активации
4. Наслаждайся!

⚠️ Антивирус может ругаться — это нормально!"""
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "buy")
async def buy(callback: types.CallbackQuery):
    text = f"""💎 <b>Покупка AWESOMETROLLING</b>

<b>Цена:</b> {PRICE}₽/месяц

<b>Вы получаете:</b>
✅ Ключ на 1 месяц
✅ Полный доступ
✅ Поддержка 24/7

Выберите способ оплаты:
"""
    await callback.message.edit_text(text, reply_markup=payment_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("pay_"))
async def payment_method(callback: types.CallbackQuery):
    method = callback.data.split("_")[1]
    
    # Генерируем ключ сразу после выбора оплаты
    key = generate_key(1, callback.from_user.id)
    
    texts = {
        "card": f"""💳 <b>Оплата картой</b>

💳 <b>Реквизиты:</b>
<code>1234 5678 9012 3456</code>

🔑 <b>Ваш ключ:</b>
<code>{key}</code>

📩 После оплаты активируй ключ в программе или через бота

📌 Свяжись с @flidges для подтверждения""",
        "crypto": f"""₿ <b>Оплата криптовалютой</b>

<b>USDT TRC-20:</b>
<code>TXxxxxxxxxxxxxxxxxxxxxxxxxx</code>

🔑 <b>Ваш ключ:</b>
<code>{key}</code>

📩 После оплаты активируй ключ в программе или через бота

📌 Свяжись с @flidges для подтверждения""",
        "other": f"""💸 <b>Другие способы оплаты</b>

🔑 <b>Ваш ключ:</b>
<code>{key}</code>

📩 Свяжись с @flidges для оплаты

📌 Ключ активируется после подтверждения оплаты"""
    }
    
    await callback.message.edit_text(
        texts.get(method, "Выбери способ"),
        reply_markup=back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "activate")
async def activate_prompt(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🔑 Введите ключ активации:\n\nПример: <code>ABCDEF123456</code>",
        reply_markup=back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(LicenseStates.waiting_for_license)
    await callback.answer()

@dp.message(LicenseStates.waiting_for_license)
async def activate_license(message: types.Message, state: FSMContext):
    key = message.text.strip().upper()
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "User"
    
    success, msg = activate_key_in_db(key, user_id, username)
    
    if success:
        await message.answer(
            f"✅ {msg}\n\n"
            f"📎 Скачай программу: /download",
            parse_mode="HTML",
            reply_markup=back_keyboard()
        )
    else:
        await message.answer(f"❌ {msg}", reply_markup=back_keyboard())
    
    await state.clear()

@dp.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conn = get_db()
    c = conn.cursor()
    
    # Проверяем ключи пользователя
    c.execute('''
        SELECT key_text, expires_at, is_used FROM license_keys 
        WHERE telegram_id = ? ORDER BY created_at DESC LIMIT 1
    ''', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        key_text, expires_at, is_used = result
        expiry = datetime.fromisoformat(expires_at)
        days_left = (expiry - datetime.now()).days
        
        if is_used:
            status_text = "✅ Активирован"
        else:
            status_text = "⏳ Ожидает активации"
        
        text = f"""📊 <b>Ваш статус:</b>

{status_text}
🔑 <b>Ключ:</b> <code>{key_text}</code>
📅 <b>Действует до:</b> {expiry.strftime('%d.%m.%Y')}
⏳ <b>Дней осталось:</b> {days_left if days_left > 0 else 0}"""
    else:
        text = "❌ <b>У вас нет лицензии!</b>\n\nКупите доступ за 50₽/месяц через меню."
    
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()

# ============================================================
# АДМИНКА
# ============================================================
def is_admin(user_id):
    return user_id in ADMIN_IDS

@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM users WHERE expires_at > datetime("now")')
    active = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM license_keys')
    keys = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM license_keys WHERE is_used = 1')
    used = c.fetchone()[0]
    conn.close()
    
    text = f"""📊 <b>Статистика</b>

👥 Пользователей: {total}
✅ Активных: {active}
🔑 Всего ключей: {keys}
✅ Использовано: {used}
🔓 Свободно: {keys - used}"""
    await callback.message.edit_text(text, reply_markup=admin_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "admin_users")
async def admin_users(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT telegram_id, username, first_name, expires_at 
        FROM users ORDER BY id DESC LIMIT 10
    ''')
    users = c.fetchall()
    conn.close()
    
    if not users:
        text = "📋 Пользователей нет"
    else:
        text = "📋 <b>Последние 10 пользователей:</b>\n\n"
        for user in users:
            user_id, username, first_name, expires_at = user
            name = first_name or username or str(user_id)
            if expires_at:
                expiry = datetime.fromisoformat(expires_at)
                status = "✅" if expiry > datetime.now() else "❌"
                text += f"{status} {name}\n"
            else:
                text += f"⏳ {name}\n"
    await callback.message.edit_text(text, reply_markup=admin_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "admin_gen")
async def admin_gen(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    await callback.message.edit_text(
        "🔑 Введите количество месяцев (1, 3, 6, 12, 24):",
        reply_markup=back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(LicenseStates.waiting_for_keygen)

@dp.message(LicenseStates.waiting_for_keygen)
async def generate_key_admin(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещен!")
        await state.clear()
        return
    
    try:
        months = int(message.text.strip())
        if months not in [1, 3, 6, 12, 24]:
            await message.answer("❌ Доступны: 1, 3, 6, 12, 24")
            return
    except:
        await message.answer("❌ Введите число!")
        return
    
    key = generate_key(months, message.from_user.id)
    if key:
        expires = (datetime.now() + timedelta(days=30*months)).isoformat()
        await message.answer(
            f"✅ <b>Ключ сгенерирован!</b>\n\n"
            f"🔑 <code>{key}</code>\n"
            f"📅 Действует: {months} месяцев\n"
            f"📅 До: {datetime.fromisoformat(expires).strftime('%d.%m.%Y')}",
            parse_mode="HTML",
            reply_markup=admin_keyboard()
        )
    else:
        await message.answer("❌ Ошибка генерации!", reply_markup=admin_keyboard())
    await state.clear()

@dp.callback_query(F.data == "admin_keys")
async def admin_keys(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT key_text, expires_at, is_used, used_by 
        FROM license_keys ORDER BY id DESC LIMIT 20
    ''')
    keys = c.fetchall()
    conn.close()
    
    if not keys:
        text = "🔑 Ключей нет"
    else:
        text = "🔑 <b>Последние 20 ключей:</b>\n\n"
        for key in keys:
            key_text, expires_at, is_used, used_by = key
            status = "✅" if is_used else "🔓"
            expiry = datetime.fromisoformat(expires_at).strftime('%d.%m.%Y')
            user = used_by if used_by else "-"
            text += f"{status} <code>{key_text}</code> | {expiry} | {user}\n"
    await callback.message.edit_text(text, reply_markup=admin_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "admin_logs")
async def admin_logs(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id, action, timestamp FROM logs ORDER BY id DESC LIMIT 20')
    logs = c.fetchall()
    conn.close()
    
    if not logs:
        text = "📋 Логов нет"
    else:
        text = "📋 <b>Последние действия:</b>\n\n"
        for log in logs:
            user_id, action, timestamp = log
            dt = datetime.fromisoformat(timestamp).strftime('%d.%m %H:%M')
            text += f"[{dt}] {action}\n"
    await callback.message.edit_text(text, reply_markup=admin_keyboard(), parse_mode="HTML")
    await callback.answer()

# ============================================================
# ЗАПУСК
# ============================================================
async def main():
    init_db()
    print("=" * 40)
    print("🔥 AWESOMETROLLING TELEGRAM БОТ")
    print(f"👨‍💻 АДМИН: {ADMIN_IDS}")
    print(f"💰 ЦЕНА: {PRICE}₽/месяц")
    print("=" * 40)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
