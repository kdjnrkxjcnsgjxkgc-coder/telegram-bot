import telebot
from telebot import types
from openai import OpenAI
import os

# 🔑 КЛЮЧІ З БЕЗПЕКИ (беремо з Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# Кнопки
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("▶ Старт", "ℹ Инфо")
    kb.add("❌ Закрыть")
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет 👋\nЯ AI-бот. Напиши любой вопрос.",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "▶ Старт")
def btn_start(message):
    bot.send_message(message.chat.id, "Я готов 🙂 Спрашивай")

@bot.message_handler(func=lambda m: m.text == "ℹ Инфо")
def info(message):
    bot.send_message(message.chat.id, "Я отвечаю с помощью AI 🤖")

@bot.message_handler(func=lambda m: m.text == "❌ Закрыть")
def close(message):
    bot.send_message(message.chat.id, "Кнопки скрыты", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=["text"])
def ai_answer(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник. Отвечай по-русски."},
                {"role": "user", "content": message.text}
            ]
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка AI 😢")

bot.infinity_polling()
