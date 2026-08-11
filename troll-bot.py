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
# НАСТРОЙКИ — ЗАМЕНИ НА СВОИ!
# ============================================================
BOT_TOKEN = "8935419647:AAEcZOioBC5QU4-TkLBXtO88BWNmjo_S73w"  # ТВОЙ ТОКЕН
ADMIN_IDS = [6652898792]  # ТВОЙ TELEGRAM ID (узнай у @userinfobot)
PRICE = 50  # ЦЕНА 50 РУБЛЕЙ В МЕСЯЦ

# ============================================================
# БАЗА ДАННЫХ
# ============================================================
DB_FILE = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            license_key TEXT,
            license_expires TEXT,
            is_activated INTEGER DEFAULT 0,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            license_key TEXT,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    ''')
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

def get_db():
    return sqlite3.connect(DB_FILE)

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
        [InlineKeyboardButton(text="💳 Карта РФ", callback_data="pay_card")],
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
        INSERT OR IGNORE INTO users (user_id, username, first_name, created_at)
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

💎 <b>Цена: {PRICE}₽/месяц</b>

📩 <b>Как купить:</b>
1. Нажми "Купить доступ"
2. Выбери способ оплаты
3. После оплаты получишь ключ

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

<b>Цена:</b> {PRICE}₽/месяц
"""
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "buy")
async def buy(callback: types.CallbackQuery):
    text = f"""💎 <b>Покупка AWESOMETROLLING</b>

<b>Цена:</b> {PRICE}₽/месяц

<b>Вы получаете:</b>
✅ Ключ на 1 месяц
✅ Полный доступ
✅ Поддержка

Выберите способ оплаты:
"""
    await callback.message.edit_text(text, reply_markup=payment_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("pay_"))
async def payment_method(callback: types.CallbackQuery):
    method = callback.data.split("_")[1]
    texts = {
        "card": "💳 <b>Оплата картой</b>\n\n💳 Карта: <code>1234 5678 9012 3456</code>\n\n📩 После оплаты напиши @flidges",
        "crypto": "₿ <b>Оплата криптой</b>\n\n<b>USDT TRC-20:</b>\n<code>TXxxxxxxxxxxxxxxxx</code>\n\n📩 После оплаты напиши @flidges",
        "other": "💸 <b>Другие способы</b>\n\n📩 Свяжись с @flidges"
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
        "🔑 Введите ключ:\n\nПример: <code>ABCDEF123456</code>",
        reply_markup=back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(LicenseStates.waiting_for_license)
    await callback.answer()

@dp.message(LicenseStates.waiting_for_license)
async def activate_license(message: types.Message, state: FSMContext):
    key = message.text.strip().upper()
    user_id = message.from_user.id
    
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT license_key, license_expires FROM users WHERE license_key = ? AND is_activated = 0', (key,))
    result = c.fetchone()
    
    if result:
        license_key, expires_at = result
        expiry = datetime.fromisoformat(expires_at)
        
        if datetime.now() > expiry:
            await message.answer("❌ Ключ истёк! Обратись к @flidges")
            await state.clear()
            return
        
        c.execute('UPDATE users SET is_activated = 1 WHERE license_key = ?', (key,))
        c.execute('INSERT INTO logs (user_id, action, timestamp) VALUES (?, ?, ?)',
                 (user_id, f"Активирован ключ {key}", datetime.now().isoformat()))
        conn.commit()
        
        await message.answer(
            f"✅ <b>Ключ активирован!</b>\n\n"
            f"🔑 Ключ: <code>{key}</code>\n"
            f"📅 До: {expiry.strftime('%d.%m.%Y')}\n\n"
            f"📎 Скачай программу у @flidges",
            parse_mode="HTML",
            reply_markup=back_keyboard()
        )
        await state.clear()
    else:
        await message.answer("❌ Неверный ключ!", reply_markup=back_keyboard())
        await state.clear()

@dp.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT license_key, license_expires, is_activated FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[2] and result[0]:
        license_key, expires_at, is_activated = result
        expiry = datetime.fromisoformat(expires_at)
        days_left = (expiry - datetime.now()).days
        text = f"""📊 <b>Ваш статус:</b>

✅ <b>Статус:</b> Активирован
🔑 <b>Ключ:</b> <code>{license_key}</code>
📅 <b>Действует до:</b> {expiry.strftime('%d.%m.%Y')}
⏳ <b>Дней осталось:</b> {days_left if days_left > 0 else 0}"""
    else:
        text = "❌ <b>У вас нет активной лицензии!</b>\n\nКупите доступ за 50₽/месяц через меню."
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
    c.execute('SELECT COUNT(*) FROM users WHERE is_activated = 1')
    active = c.fetchone()[0]
    conn.close()
    text = f"📊 <b>Статистика</b>\n\n👥 Пользователей: {total}\n✅ Активных: {active}"
    await callback.message.edit_text(text, reply_markup=admin_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "admin_users")
async def admin_users(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id, username, first_name, license_key, is_activated FROM users ORDER BY id DESC LIMIT 10')
    users = c.fetchall()
    conn.close()
    
    if not users:
        text = "📋 Пользователей нет"
    else:
        text = "📋 <b>Последние 10 пользователей:</b>\n\n"
        for user in users:
            user_id, username, first_name, license_key, is_activated = user
            status = "✅" if is_activated else "⏳"
            name = first_name or username or str(user_id)
            key = license_key[:8] + "..." if license_key else "❌"
            text += f"{status} {name} | Ключ: {key}\n"
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
async def generate_key(message: types.Message, state: FSMContext):
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
    
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    expires = (datetime.now() + timedelta(days=30*months)).isoformat()
    
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO users (user_id, username, license_key, license_expires, created_at) VALUES (?, ?, ?, ?, ?)',
             (message.from_user.id, "admin_gen", key, expires, datetime.now().isoformat()))
    c.execute('INSERT INTO logs (user_id, action, timestamp) VALUES (?, ?, ?)',
             (message.from_user.id, f"Сгенерирован ключ {key} на {months} мес", datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    await message.answer(
        f"✅ <b>Ключ сгенерирован!</b>\n\n🔑 <code>{key}</code>\n📅 Действует: {months} месяцев\n📅 До: {datetime.fromisoformat(expires).strftime('%d.%m.%Y')}",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )
    await state.clear()

@dp.callback_query(F.data == "admin_keys")
async def admin_keys(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT license_key, license_expires, is_activated FROM users WHERE license_key IS NOT NULL ORDER BY id DESC LIMIT 20')
    keys = c.fetchall()
    conn.close()
    
    if not keys:
        text = "🔑 Ключей нет"
    else:
        text = "🔑 <b>Последние 20 ключей:</b>\n\n"
        for key in keys:
            license_key, expires_at, is_activated = key
            status = "✅" if is_activated else "🔓"
            expiry = datetime.fromisoformat(expires_at).strftime('%d.%m.%Y')
            text += f"{status} <code>{license_key}</code> | До: {expiry}\n"
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
    print("🤖 БОТ ЗАПУЩЕН!")
    print(f"👨‍💻 АДМИН: {ADMIN_IDS}")
    print(f"💰 ЦЕНА: {PRICE}₽/месяц")
    print("=" * 40)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())