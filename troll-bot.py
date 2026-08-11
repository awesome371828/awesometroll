@bot.message_handler(commands=['key'])
def generate_key(message):
    """Генерация нового ключа"""
    # Проверка что пользователь админ
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ Доступ запрещен!")
        return
    
    # Парсим аргументы: /key 3 (на 3 месяца)
    args = message.text.split()
    months = int(args[1]) if len(args) > 1 else 1
    
    key = generate_license_key(months)
    if key:
        bot.reply_to(
            message,
            f"🔑 Новый ключ сгенерирован:\n\n"
            f"`{key}`\n\n"
            f"📅 Действует: {months} месяц(ев)\n"
            f"📩 Отправь его покупателю!\n\n"
            f"⚠️ Ключ привяжется к первому компьютеру!"
        )
    else:
        bot.reply_to(message, "❌ Ошибка генерации ключа!")

@bot.message_handler(commands=['check'])
def check_key(message):
    """Проверка статуса ключа"""
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Использование: /check КЛЮЧ")
        return
    
    key = args[1].upper()
    status = check_key_status(key)
    bot.reply_to(message, f"📊 Статус ключа {key}:\n{status}")

@bot.message_handler(commands=['download'])
def download_program(message):
    """Ссылка на скачивание программы"""
    bot.reply_to(
        message,
        "📥 Скачать AWESOMETROLLING:\n\n"
        "🔗 Ссылка: [СКАЧАТЬ](тут_твоя_ссылка_на_exe)\n\n"
        "🔑 После скачивания введи полученный ключ в программу!"
    )
