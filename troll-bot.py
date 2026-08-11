import asyncio
import logging
import sqlite3
import random
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta  # ← ИСПРАВЛЕНО!
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ============================================================
# НАСТРОЙКИ
# ============================================================
BOT_TOKEN = "8935419647:AAEcZOioBC5QU4-TkLBXtO88BWNmjo_S73w"
ADMIN_IDS = [6652898792]
PRICE = 50
ANTISPAM_SECONDS = 2
BAN_MINUTES = 15

PAYMENT_LINK = "https://yoomoney.ru/quickpay/fundraise/button?billNumber=1JJ662LM5S4.260811&"
DOWNLOAD_LINKS = {
    "google": "https://drive.google.com/file/d/16-z26al_gb2uBI3ozBbnWIIqW9Dg92Hv/view?usp=sharing",
    "yandex": "https://disk.yandex.ru/d/dtGhLWzdHDB6EA"
}
REVIEW_LINK = "https://www.youtube.com/watch?v=U5Vh9cGMRag"

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
            is_banned INTEGER DEFAULT 0,
            ban_until TEXT,
            created_at TEXT,
            last_message_time TEXT
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
    waiting_for_key_to_send = State()

# ============================================================
# БОТ
# ============================================================
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

# ============================================================
# КРАСИВЫЕ КЛАВИАТУРЫ
# ============================================================
def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Купить доступ", callback_data="buy"),
            InlineKeyboardButton(text="🔑 Активировать ключ", callback_data="activate")
        ],
        [
            InlineKeyboardButton(text="📊 Мой статус", callback_data="status"),
            InlineKeyboardButton(text="⬇️ Скачать", callback_data="download")
        ],
        [
            InlineKeyboardButton(text="📺 Обзор", url=REVIEW_LINK),
            InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/flidges")
        ],
        [
            InlineKeyboardButton(text="📝 О программе", callback_data="about")
        ]
    ])

def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text="🔑 Создать ключ", callback_data="admin_gen"),
            InlineKeyboardButton(text="📋 Все ключи", callback_data="admin_keys")
        ],
        [
            InlineKeyboardButton(text="📊 Логи", callback_data="admin_logs")
        ],
        [
            InlineKeyboardButton(text="⬅️ Главное меню", callback_data="menu")
        ]
    ])

def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu")]
    ])

def payment_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить картой", callback_data="pay_card")],
        [InlineKeyboardButton(text="💸 Другой способ", callback_data="pay_other")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])

def download_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Google Диск", url=DOWNLOAD_LINKS["google"])],
        [InlineKeyboardButton(text="📥 Яндекс.Диск", url=DOWNLOAD_LINKS["yandex"])],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])

# ============================================================
# АНТИСПАМ И БАН
# ============================================================
async def check_antispam(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT last_message_time FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    
    if result and result[0]:
        last_time = datetime.fromisoformat(result[0])
        if (datetime.now() - last_time).total_seconds() < ANTISPAM_SECONDS:
            conn.close()
            return False
    
    c.execute('UPDATE users SET last_message_time = ? WHERE user_id = ?', 
              (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()
    return True

async def is_user_banned(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT is_banned, ban_until FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] and result[1]:
        ban_until = datetime.fromisoformat(result[1])
        if datetime.now() < ban_until:
            return True, ban_until
        else:
            conn = get_db()
            c = conn.cursor()
            c.execute('UPDATE users SET is_banned = 0, ban_until = NULL WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()
    return False, None

# ============================================================
# КОМАНДЫ
# ============================================================
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    
    if not await check_antispam(user_id):
        return
    
    is_banned, ban_until = await is_user_banned(user_id)
    if is_banned:
        await message.answer(
            f"🚫 <b>Вы забанены до {ban_until.strftime('%d.%m.%Y %H:%M')}</b>\n\n"
            f"📩 По вопросам: @flidges",
            parse_mode="HTML"
        )
        return
    
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
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.message.edit_text(
            "🚫 Вы забанены! Обратитесь к @flidges",
            reply_markup=back_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "🔥 <b>AWESOMETROLLING</b> — Главное меню\n\nВыберите действие:",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "download")
async def download(callback: types.CallbackQuery):
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    text = """📥 <b>Скачать AWESOMETROLLING</b>

Выберите удобный способ скачивания:

📌 <b>Google Диск</b> — для пользователей Google
📌 <b>Яндекс.Диск</b> — для пользователей Яндекса

Если ссылки не работают — напишите @flidges"""
    
    await callback.message.edit_text(text, reply_markup=download_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    text = f"""🔥 <b>AWESOMETROLLING</b>

<b>Версия:</b> 3.0
<b>Разработчик:</b> @flidges

<b>Особенности:</b>
✅ Каждое сообщение уникально
✅ Длинные связные предложения
✅ 60+ шаблонов
✅ Работает при свёрнутом окне
✅ Автовход по ключу
✅ Защита HWID

<b>Цена:</b> {PRICE}₽/месяц

📺 <b>Смотрите обзор программы:</b>"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📺 Смотреть обзор на YouTube", url=REVIEW_LINK)],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

# ============================================================
# ПОКУПКА
# ============================================================
@dp.callback_query(F.data == "buy")
async def buy(callback: types.CallbackQuery):
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    text = f"""💎 <b>Покупка AWESOMETROLLING</b>

<b>Цена:</b> {PRICE}₽/месяц

<b>Вы получаете:</b>
✅ Лицензионный ключ на 1 месяц
✅ Полный доступ ко всем функциям
✅ Поддержка 24/7

Выберите способ оплаты:"""
    
    await callback.message.edit_text(text, reply_markup=payment_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "pay_card")
async def pay_card(callback: types.CallbackQuery):
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    text = f"""💳 <b>Оплата картой РФ</b>

<b>Ссылка для оплаты:</b>
<a href="{PAYMENT_LINK}">💰 Оплатить {PRICE}₽</a>

📩 <b>После оплаты:</b>
1. Нажми на ссылку и оплати {PRICE}₽
2. Нажми кнопку "✅ Я оплатил" ниже
3. Админ проверит оплату и выдаст ключ

👨‍💻 По вопросам: @flidges"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💰 Оплатить {PRICE}₽", url=PAYMENT_LINK)],
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment_done")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "pay_other")
async def pay_other(callback: types.CallbackQuery):
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    text = """💸 <b>Другие способы оплаты</b>

Принимаются:
• Стим-подарки
• Подарочные карты
• Перевод на карту

📩 Свяжись с @flidges"""
    
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "payment_done")
async def payment_done(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    if not await check_antispam(user_id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(user_id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    username = callback.from_user.username or "без username"
    first_name = callback.from_user.first_name or "User"
    
    for admin_id in ADMIN_IDS:
        try:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Подтвердить оплату", callback_data=f"confirm_pay_{user_id}")],
                [InlineKeyboardButton(text="❌ Отклонить (бан 15 мин)", callback_data=f"reject_pay_{user_id}")]
            ])
            
            await bot.send_message(
                admin_id,
                f"💳 <b>НОВАЯ ОПЛАТА!</b>\n\n"
                f"👤 Пользователь: {first_name} (@{username})\n"
                f"🆔 ID: <code>{user_id}</code>\n"
                f"💰 Сумма: {PRICE}₽\n"
                f"📅 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"Выберите действие:",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except:
            pass
    
    await callback.message.edit_text(
        "✅ <b>Спасибо! Ваша оплата отправлена на проверку.</b>\n\n"
        "⏳ Админ проверит оплату и выдаст ключ в ближайшее время.\n\n"
        "📩 Если задержка — напишите @flidges",
        reply_markup=back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

# ============================================================
# АДМИН: ПОДТВЕРЖДЕНИЕ/ОТКЛОНЕНИЕ
# ============================================================
@dp.callback_query(F.data.startswith("confirm_pay_"))
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    
    user_id = int(callback.data.split("_")[2])
    
    await callback.message.edit_text(
        f"✅ <b>Подтверждение оплаты</b>\n\n"
        f"Пользователь ID: <code>{user_id}</code>\n\n"
        f"📝 Введите ключ активации для этого пользователя:",
        parse_mode="HTML"
    )
    
    await state.update_data(user_id=user_id)
    await state.set_state(LicenseStates.waiting_for_key_to_send)
    await callback.answer()

@dp.callback_query(F.data.startswith("reject_pay_"))
async def reject_payment(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    
    user_id = int(callback.data.split("_")[2])
    
    conn = get_db()
    c = conn.cursor()
    ban_until = (datetime.now() + timedelta(minutes=BAN_MINUTES)).isoformat()
    c.execute('UPDATE users SET is_banned = 1, ban_until = ? WHERE user_id = ?', (ban_until, user_id))
    conn.commit()
    conn.close()
    
    try:
        await bot.send_message(
            user_id,
            f"🚫 <b>Ваша оплата отклонена!</b>\n\n"
            f"Причина: Не удалось подтвердить оплату\n"
            f"⏳ Вы забанены на {BAN_MINUTES} минут\n\n"
            f"📩 Если это ошибка — напишите @flidges",
            parse_mode="HTML"
        )
    except:
        pass
    
    await callback.message.edit_text(
        f"❌ <b>Оплата отклонена!</b>\n\n"
        f"Пользователь ID: <code>{user_id}</code>\n"
        f"⏳ Забанен на {BAN_MINUTES} минут",
        parse_mode="HTML"
    )
    await callback.answer()

@dp.message(LicenseStates.waiting_for_key_to_send)
async def send_key_to_user(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Доступ запрещен!")
        await state.clear()
        return
    
    key = message.text.strip().upper()
    data = await state.get_data()
    user_id = data.get('user_id')
    
    if not user_id:
        await message.answer("❌ Ошибка: пользователь не найден!")
        await state.clear()
        return
    
    expires_at = (datetime.now() + relativedelta(months=1)).isoformat()
    
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE users SET license_key = ?, license_expires = ?, is_activated = 1 WHERE user_id = ?', 
              (key, expires_at, user_id))
    c.execute('INSERT INTO logs (user_id, action, timestamp) VALUES (?, ?, ?)',
              (user_id, f"Админ выдал ключ {key}", datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    try:
        await bot.send_message(
            user_id,
            f"🎉 <b>Поздравляем! Вы купили AWESOMETROLLING!</b>\n\n"
            f"🔑 <b>Ваш ключ:</b> <code>{key}</code>\n"
            f"📅 <b>Действует до:</b> {datetime.fromisoformat(expires_at).strftime('%d.%m.%Y')}\n\n"
            f"⬇️ <b>Скачать программу:</b>\n"
            f"Google Drive: {DOWNLOAD_LINKS['google']}\n"
            f"Яндекс.Диск: {DOWNLOAD_LINKS['yandex']}\n\n"
            f"📺 <b>Обзор программы:</b>\n{REVIEW_LINK}\n\n"
            f"📩 При проблемах: @flidges",
            parse_mode="HTML"
        )
    except:
        pass
    
    await message.answer(
        f"✅ <b>Ключ отправлен!</b>\n\n"
        f"🔑 Ключ: <code>{key}</code>\n"
        f"👤 Пользователь ID: <code>{user_id}</code>\n"
        f"📅 Действует до: {datetime.fromisoformat(expires_at).strftime('%d.%m.%Y')}",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )
    await state.clear()

# ============================================================
# СТАТУС
# ============================================================
@dp.callback_query(F.data == "status")
async def status(callback: types.CallbackQuery):
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    user_id = callback.from_user.id
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT license_key, license_expires, is_activated FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[2] and result[0]:
        license_key, expires_at, is_activated = result
        expiry = datetime.fromisoformat(expires_at)
        
        now = datetime.now()
        if expiry > now:
            diff = relativedelta(expiry, now)
            if diff.months > 0:
                if diff.days > 0:
                    time_left = f"{diff.months} мес, {diff.days} дн"
                else:
                    time_left = f"{diff.months} мес"
            elif diff.days > 0:
                time_left = f"{diff.days} дн"
            else:
                time_left = "менее дня"
        else:
            time_left = "0"
        
        text = f"""📊 <b>Ваш статус:</b>

✅ <b>Статус:</b> Активирован
🔑 <b>Ключ:</b> <code>{license_key}</code>
📅 <b>Действует до:</b> {expiry.strftime('%d.%m.%Y')}
⏳ <b>Осталось:</b> {time_left}

📺 <b>Обзор программы:</b>
{REVIEW_LINK}"""
    else:
        text = "❌ <b>У вас нет активной лицензии!</b>\n\nКупите доступ за 50₽/месяц через меню."
    await callback.message.edit_text(text, reply_markup=back_keyboard(), parse_mode="HTML")
    await callback.answer()

# ============================================================
# АКТИВАЦИЯ КЛЮЧА
# ============================================================
@dp.callback_query(F.data == "activate")
async def activate_prompt(callback: types.CallbackQuery, state: FSMContext):
    if not await check_antispam(callback.from_user.id):
        await callback.answer("⏳ Подождите немного!", show_alert=True)
        return
    
    is_banned, _ = await is_user_banned(callback.from_user.id)
    if is_banned:
        await callback.answer("🚫 Вы забанены!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🔑 Введите ключ:\n\nПример: <code>ABCDEF123456</code>",
        reply_markup=back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(LicenseStates.waiting_for_license)
    await callback.answer()

@dp.message(LicenseStates.waiting_for_license)
async def activate_license(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    if not await check_antispam(user_id):
        await message.answer("⏳ Подождите немного!")
        return
    
    is_banned, _ = await is_user_banned(user_id)
    if is_banned:
        await message.answer("🚫 Вы забанены! Обратитесь к @flidges")
        await state.clear()
        return
    
    key = message.text.strip().upper()
    
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
            f"⬇️ <b>Скачать программу:</b> /download\n"
            f"📺 <b>Обзор:</b> {REVIEW_LINK}",
            parse_mode="HTML",
            reply_markup=back_keyboard()
        )
        await state.clear()
    else:
        await message.answer("❌ Неверный ключ!", reply_markup=back_keyboard())
        await state.clear()
    
    conn.close()

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
    c.execute('SELECT COUNT(*) FROM users WHERE is_banned = 1')
    banned = c.fetchone()[0]
    conn.close()
    text = f"📊 <b>Статистика</b>\n\n👥 Всего: {total}\n✅ Активных: {active}\n🚫 Забанено: {banned}"
    await callback.message.edit_text(text, reply_markup=admin_keyboard(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "admin_users")
async def admin_users(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещен!", show_alert=True)
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id, username, first_name, license_key, is_activated, is_banned FROM users ORDER BY id DESC LIMIT 10')
    users = c.fetchall()
    conn.close()
    
    if not users:
        text = "📋 Пользователей нет"
    else:
        text = "📋 <b>Последние 10 пользователей:</b>\n\n"
        for user in users:
            user_id, username, first_name, license_key, is_activated, is_banned = user
            status = "✅" if is_activated else ("🚫" if is_banned else "⏳")
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
    expires_at = (datetime.now() + relativedelta(months=months)).isoformat()
    
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO users (user_id, username, license_key, license_expires, created_at) VALUES (?, ?, ?, ?, ?)',
             (message.from_user.id, "admin_gen", key, expires_at, datetime.now().isoformat()))
    c.execute('INSERT INTO logs (user_id, action, timestamp) VALUES (?, ?, ?)',
             (message.from_user.id, f"Сгенерирован ключ {key} на {months} мес", datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    await message.answer(
        f"✅ <b>Ключ сгенерирован!</b>\n\n🔑 <code>{key}</code>\n📅 Действует: {months} месяцев\n📅 До: {datetime.fromisoformat(expires_at).strftime('%d.%m.%Y')}",
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
    print(f"📺 ОБЗОР: {REVIEW_LINK}")
    print("=" * 40)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
