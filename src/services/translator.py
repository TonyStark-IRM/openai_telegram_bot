# Обробник відповіді translator для користувача
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import openai
from aiogram import types

bot = Bot(token="TG_BOT_API_KEY")
dp = Dispatcher(bot)

async def translator_process(message: types.Message):
    try:
        text, target_lang = [part.strip() for part in message.text.split("|", 1)]
        prompt = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Ти профі-перекладач з чіткими поясненнями контексту і зразками використання."},
                {"role": "user", "content": f"Translate the following text to {target_lang}:\n\"{text}\""}
            ],
            "max_tokens": 1000,
            "temperature": 0.8,
        }
        resp = openai.ChatCompletion.create(**prompt)
        translated = resp.choices[0].message.content.strip()

        await message.reply(f"Переклад ({target_lang}):\n{translated}\n\nКонтекст використання та приклади можна додати за потреби.")
    except Exception as e:
        await message.reply(f"Помилка перекладу: {e}")

# dp.message.register(translator_process, lambda m: m.text and "|" in m.text)