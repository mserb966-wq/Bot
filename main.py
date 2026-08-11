import telebot
from telebot import types

# === 1. НАСТРОЙКИ (ВСТАВЬ СВОИ ДАННЫЕ) === 
BOT_TOKEN = "8675670535:AAFJk1nH5vLIo3ENlJJstwrVUtbMmHRFs8s"
ADMIN_ID = 7926462587

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище ответов анкеты
user_data = {}


# === 2. КЛАВИАТУРА МЕНЮ ===
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📋 Заполнить анкету подопечного")
    btn2 = types.KeyboardButton("💰 Услуги и прайс")
    btn3 = types.KeyboardButton("✍️ Связаться с Creator")
    markup.add(btn1)
    markup.add(btn2, btn3)
    return markup


# === 3. КОМАНДА /start ===
@bot.message_handler(commands=["start"])
def start_message(message):
    welcome_text = (
        "<b>CREATOR | Биомеханика и Сила</b>\n\n"
        "Приветствую. Я — цифровой помощник проекта CREATOR.\n"
        "Здесь не торгуют лицом и мотивацией. Только жесткая биомеханика, "
        "безопасный прогресс и работа на результат.\n\n"
        "Выбери нужное действие в меню ниже:"
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard(),
    )


# === 4. ОБРАБОТКА КНОПОК ===
@bot.message_handler(
    func=lambda msg: msg.text
    in [
        "💰 Услуги и прайс",
        "✍️ Связаться с Creator",
        "📋 Заполнить анкету подопечного",
    ]
)
def handle_menu(message):
    if message.text == "💰 Услуги и прайс":
        price_text = (
            "<b>АКТУАЛЬНЫЙ ПРАЙС-ЛИСТ (UAH):</b>\n\n"
            "🏋️‍♂️ <b>Индивидуальная программа тренировок:</b> 800 – 1 200 грн\n"
            "<i>(Расчет нагрузки на 4-8 недель, учет травм, видео с техникой)</i>\n\n"
            "🥗 <b>План питания (КБЖУ + Рацион):</b> 800 – 1 000 грн\n"
            "<i>(Гибкое меню из доступных продуктов под твою цель)</i>\n\n"
            "🔥 <b>Комбо (Программа + Питание):</b> 1 500 – 2 000 грн\n\n"
            "🎯 <b>Онлайн-ведение (1 месяц):</b> 2 500 – 4 000 грн\n"
            "<i>(Полный контроль, корректировки, разбор техники 24/7)</i>\n\n"
            "Чтобы заказать услугу, заполни анкету через кнопку в меню."
        )
        bot.send_message(message.chat.id, price_text, parse_mode="HTML")

    elif message.text == "✍️ Связаться с Creator":
        bot.send_message(
            message.chat.id,
            "По всем вопросам пиши напрямую в ЛС: @M_Serbin",
        )

    elif message.text == "📋 Заполнить анкету подопечного":
        user_data[message.chat.id] = {}
        msg = bot.send_message(
            message.chat.id,
            "Шаг 1/4: Как к тебе обращаться? (Имя или позывной)",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        bot.register_next_step_handler(msg, process_name)


# === 5. ПОШАГОВАЯ АНКЕТА ===
def process_name(message):
    user_data[message.chat.id]["name"] = message.text
    msg = bot.send_message(
        message.chat.id,
        "Шаг 2/4: Укажи ваш возраст, рост и текущий вес (например: 22 года, 180 см, 85 кг).",
    )
    bot.register_next_step_handler(msg, process_age_weight)


def process_age_weight(message):
    user_data[message.chat.id]["age_weight"] = message.text
    msg = bot.send_message(
        message.chat.id,
        "Шаг 3/4: Какая твоя главная цель? (Набор массы, сушка, увеличение силовых в жиме/тяге и т.д.)",
    )
    bot.register_next_step_handler(msg, process_goal)


def process_goal(message):
    user_data[message.chat.id]["goal"] = message.text
    msg = bot.send_message(
        message.chat.id,
        "Шаг 4/4: Есть ли травмы, дискомфорт или ограничения по здоровью? (Особенно: локти, плечи, поясница, колени).",
    )
    bot.register_next_step_handler(msg, process_injuries)


def process_injuries(message):
    user_data[message.chat.id]["injuries"] = message.text
    data = user_data[message.chat.id]

    summary = (
        "<b>Анкета успешно отправлена!</b>\n\n"
        f"<b>Имя:</b> {data['name']}\n"
        f"<b>Параметры:</b> {data['age_weight']}\n"
        f"<b>Цель:</b> {data['goal']}\n"
        f"<b>Травмы/Ограничения:</b> {data['injuries']}\n\n"
        "Creator изучит данные и свяжется с тобой."
    )
    # Уведомление тебе в личку со всей анкетой клиентов
if message.from_user.username:
    user_tag = f"@{message.from_user.username}"
else:
    user_tag = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"

admin_text = (
    "🚨 <b>НОВАЯ АНКЕТА ПОДОПЕЧНОГО!</b>\n\n"
    f"<b>Клиент:</b> {user_tag}\n"
    f"<b>Имя:</b> {data['name']}\n"
    f"<b>Параметры:</b> {data['age_weight']}\n"
    f"<b>Цель:</b> {data['goal']}\n"
    f"<b>Травмы/Ограничения:</b> {data['injury']}"
)

) 
    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")


# === 6. ЗАПУСК БОТА ===
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
