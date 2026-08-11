import telebot
from telebot import types

# === 1. ИНИЦИАЛИЗАЦИЯ И НАСТРОЙКИ ===
BOT_TOKEN = "8675670535:AAFJk1nH5vLlo3ENIJJstwrVUtbMmHRFs8s"
ADMIN_ID = 7926462587

bot = telebot.TeleBot(BOT_TOKEN)

# Временное хранилище данных пользователей
user_data = {}


def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Заполнить анкету"))
    return markup


# === 2. СТАРТ И ОСНОВНЫЕ КОМАНДЫ ===
@bot.message_handler(commands=['start'])
def start_cmd(message):
    welcome_text = (
        "Привет! Я бот для записи на онлайн-ведение и тренировки.\n\n"
        "Нажми кнопку <b>«Заполнить анкету»</b> ниже, чтобы отправить свои данные."
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == "Заполнить анкету")
def start_survey(message):
    user_data[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "Как тебя зовут? (Напиши имя и фамилию)",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, process_name)


# === 3. ШАГИ АНКЕТЫ ===
def process_name(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(
        message.chat.id,
        "Укажи твой возраст и текущий вес (например: 25 лет, 80 кг):"
    )
    bot.register_next_step_handler(message, process_age_weight)


def process_age_weight(message):
    user_data[message.chat.id]['age_weight'] = message.text
    bot.send_message(
        message.chat.id,
        "Какая у тебя главная цель? (Похудение, набор массы, силовые показатели и т.д.):"
    )
    bot.register_next_step_handler(message, process_goal)


def process_goal(message):
    user_data[message.chat.id]['goal'] = message.text
    bot.send_message(
        message.chat.id,
        "Есть ли у тебя травмы, ограничения по здоровью или болячки? (Если нет, напиши 'Нет'):"
    )
    bot.register_next_step_handler(message, process_injury)


def process_injury(message):
    chat_id = message.chat.id
    user_data[chat_id]['injury'] = message.text
    data = user_data[chat_id]

    # Полный ответ пользователю с анкетой, прайсом и контактами
    summary = (
        "<b>Твоя анкета принята!</b>\n\n"
        f"<b>Имя:</b> {data['name']}\n"
        f"<b>Параметры:</b> {data['age_weight']}\n"
        f"<b>Цель:</b> {data['goal']}\n"
        f"<b>Травмы/Ограничения:</b> {data['injury']}\n\n"
        "💳 <b>ПРАЙС-ЛИСТ УСЛУГ:</b>\n"
        "• Составление программы тренировок — 500 грн\n"
        "• Индивидуальный план питания — 400 грн\n"
        "• Полное онлайн-ведение (месяц) — 1200 грн\n\n"
        "📩 <b>СВЯЗЬ СО МНОЙ:</b>\n"
        "Если есть вопросы, напиши мне в личку напрямую.\n\n"
        "Creator изучит данные и свяжется с тобой в ближайшее время!"
    )

    bot.send_message(
        chat_id,
        summary,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

    # Уведомление администратору (в личку) со всей анкетой клиента
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

    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")


# === 4. ЗАПУСК БОТА ===
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
    
