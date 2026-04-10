import time
import telebot
from telebot import types

# 🔑 ВСТАВЬ НОВЫЙ ТОКЕН (обязательно обнови в BotFather)
BOT_TOKEN = "7774651689:AAEDDVX6QhBdlDQFRxdfDQ5ubexztx8NF4E"

# 👑 ID админов
ADMINS = [6144666275,1723545550 ]

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

print("=" * 50)
print("🚀 БОТ УСПЕШНО ЗАПУЩЕН")
print("=" * 50)


# ─────────────────────────────
# 👑 Проверка админа
# ─────────────────────────────
def is_admin(user_id):
    return user_id in ADMINS


# ─────────────────────────────
# 👤 Информация о пользователе
# ─────────────────────────────
def user_info(user):
    username = f"@{user.username}" if user.username else "нет username"

    return (
        f"👤 <b>Имя:</b> {user.first_name}\n"
        f"🔹 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
    )


# ─────────────────────────────
# 🕒 Время
# ─────────────────────────────
def now():
    return time.strftime("%d.%m.%Y %H:%M:%S")


# ─────────────────────────────
# 📩 Отправка всем админам
# ─────────────────────────────
def send_to_admins(text):
    for admin_id in ADMINS:
        try:
            bot.send_message(admin_id, text)
        except Exception as e:
            print(f"Ошибка отправки админу {admin_id}: {e}")


# ─────────────────────────────
# 📦 Пересылка сообщения
# ─────────────────────────────
def forward_to_admins(message):
    for admin_id in ADMINS:
        try:
            bot.forward_message(admin_id, message.chat.id, message.message_id)
        except Exception as e:
            print(f"Ошибка пересылки: {e}")


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
@bot.message_handler(commands=['start', 'help'])
def start(message):
    user = message.from_user

    if is_admin(user.id):
        bot.reply_to(message,
            "👑 <b>Админ-панель</b>\n"
            f"🆔 Ваш ID: <code>{user.id}</code>\n"
            f"👥 Всего админов: <b>{len(ADMINS)}</b>"
        )
    else:
        bot.reply_to(message,
            "👋 <b>Привет!</b>\n\n"
            "Отправь сообщение, фото, видео или файл —\n"
            "я красиво передам это администраторам 📩"
        )


# ─────────────────────────────
# 💬 ТЕКСТ
# ─────────────────────────────
@bot.message_handler(content_types=['text'])
def text_handler(message):
    user = message.from_user

    if is_admin(user.id):
        bot.reply_to(message, "✔ Принято")
        return

    text = (
        "📩 <b>НОВОЕ СООБЩЕНИЕ</b>\n\n"
        f"{user_info(user)}"
        f"🕒 <b>Время:</b> {now()}\n\n"
        f"💬 <b>Текст:</b>\n{message.text}"
    )

    send_to_admins(text)
    bot.reply_to(message, "✅ <b>Сообщение доставлено</b>")


# ─────────────────────────────
# 📷 ФОТО
# ─────────────────────────────
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    user = message.from_user

    if is_admin(user.id):
        bot.reply_to(message, "📷 Получено")
        return

    caption = (
        "📷 <b>НОВОЕ ФОТО</b>\n\n"
        f"{user_info(user)}"
        f"🕒 <b>Время:</b> {now()}"
    )

    send_to_admins(caption)

    for admin_id in ADMINS:
        bot.send_photo(admin_id, message.photo[-1].file_id)

    bot.reply_to(message, "✅ Фото отправлено")


# ─────────────────────────────
# 📦 МЕДИА (всё остальное)
# ─────────────────────────────
@bot.message_handler(content_types=['video', 'document', 'voice', 'audio', 'animation'])
def media_handler(message):
    user = message.from_user

    if is_admin(user.id):
        bot.reply_to(message, "✔ Получено")
        return

    media_names = {
        "video": "🎥 Видео",
        "document": "📎 Документ",
        "voice": "🎤 Голосовое",
        "audio": "🎵 Аудио",
        "animation": "🎞 GIF"
    }

    title = media_names.get(message.content_type, "📦 Медиа")

    text = (
        f"{title}\n\n"
        f"{user_info(user)}"
        f"🕒 <b>Время:</b> {now()}"
    )

    send_to_admins(text)
    forward_to_admins(message)

    bot.reply_to(message, "✅ Файл отправлен")


# ─────────────────────────────
# 🔄 АВТОПЕРЕЗАПУСК
# ─────────────────────────────
def main():
    while True:
        try:
            print("🤖 Бот работает...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
