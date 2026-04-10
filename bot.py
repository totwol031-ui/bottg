import time
import telebot
from telebot import types

# 🔑 ВСТАВЬ СВОЙ ТОКЕН
BOT_TOKEN = "7774651689:AAEDDVX6QhBdlDQFRxdfDQ5ubexztx8NF4E"

# 👑 ID админов
ADMINS = [6605628273, 2004192760]

bot = telebot.TeleBot(BOT_TOKEN)

print("=" * 50)
print("БОТ ЗАПУЩЕН (СЕРВЕРНАЯ ВЕРСИЯ БЕЗ ПРОКСИ)")
print("=" * 50)


def is_admin(user_id):
    return user_id in ADMINS


def send_to_all_admins(text):
    for admin_id in ADMINS:
        try:
            bot.send_message(admin_id, text)
        except Exception as e:
            print(f"Ошибка отправки админу {admin_id}: {e}")


def forward_to_all_admins(message):
    for admin_id in ADMINS:
        try:
            bot.forward_message(admin_id, message.chat.id, message.message_id)
        except Exception as e:
            print(f"Ошибка пересылки админу {admin_id}: {e}")


# 🚀 Старт
@bot.message_handler(commands=['start', 'help'])
def start_cmd(message):
    user = message.from_user

    if is_admin(user.id):
        response = (
            f"Админ\nID: {user.id}\n"
            f"Всего админов: {len(ADMINS)}"
        )
    else:
        response = (
            f"Привет, {user.first_name}!\n"
            f"Отправь сообщение — я передам администраторам."
        )

    bot.reply_to(message, response)


# 📝 Текст
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user = message.from_user

    if is_admin(user.id):
        bot.reply_to(message, "Получено")
        return

    text = (
        f"📩 Новое сообщение\n\n"
        f"👤 {user.first_name}\n"
        f"🆔 {user.id}\n"
        f"🕒 {time.strftime('%H:%M:%S')}\n\n"
        f"{message.text}"
    )

    send_to_all_admins(text)
    bot.reply_to(message, "Сообщение отправлено ✅")


# 📷 Фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user = message.from_user

    if is_admin(user.id):
        bot.reply_to(message, "Фото получено")
        return

    send_to_all_admins(f"📷 Фото от {user.first_name} ({user.id})")

    for admin_id in ADMINS:
        bot.send_photo(admin_id, message.photo[-1].file_id)

    bot.reply_to(message, "Фото отправлено ✅")


# 📎 Всё остальное
@bot.message_handler(content_types=['video', 'document', 'audio', 'voice'])
def handle_media(message):
    user = message.from_user

    if is_admin(user.id):
        bot.reply_to(message, "Получено")
        return

    send_to_all_admins(f"📎 Медиа от {user.first_name} ({user.id})")
    forward_to_all_admins(message)

    bot.reply_to(message, "Файл отправлен ✅")


# 🔄 Запуск с автоперезапуском
def main():
    while True:
        try:
            print("Бот запускается...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Ошибка: {e}")
            print("Перезапуск через 5 секунд...")
            time.sleep(5)


if __name__ == "__main__":
    main()