# Обробник зображень /image_recognition

import os
import openai
from openai import OpenAIError

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import types

bot = Bot(token="TG_BOT_API_KEY")
dp = Dispatcher(bot)

# Встановлюємо API ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Обробник команда /image_recognition
async def image_recognition_command(message: types.Message):
    await message.reply("Надішліть зображення або залиште URL до зображення після символу |.")

dp.message.register(image_recognition_command, Command(commands=["image_recognition"]))

@dp.message(Command(commands=["image_recognition"]))
async def image_recognition_command(message: types.Message):
    await message.reply("Надішліть зображення або URL.")

# Обробка вхідного зображення або URL
@dp.message(content_types=["photo"])
async def image_recognition_process_photo(message: types.Message):
    photo = message.photo[-1]
    file = await photo.get_file()
    file_path = f"tmp_{photo.file_id}.jpg"
    await file.download(destination=file_path)

    await _process_image_file(message, file_path)

@dp.message()
async def image_recognition_process_url(message: types.Message):
    # Припустимо, користувач надіслав URL у тексті повідомлення
    if message.text and message.text.startswith("http"):
        url = message.text.strip()
        await _process_image_url(message, url)

async def _process_image_file(message: types.Message, file_path: str):
    try:
        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

        description = await _describe_image(image_bytes=image_bytes)
        if description:
            await message.reply(f"Опис зображення: {description}")
        else:
            await message.reply("Не вдалося отримати опис зображення.")
    except Exception as e:
        await message.reply(f"Помилка перекладу: {e}")
    finally:
        try:
            os.remove(file_path)
        except OSError:
            pass

async def _process_image_url(message: types.Message, url: str):
    try:
        description = await _describe_image_from_url(image_url=url)
        if description:
            await message.reply(f"Опис зображення за URL:\n{description}")
        else:
            await message.reply("Не вдалося отримати опис зображення за URL.")
    except Exception as e:
        await message.reply(f"Помилка перекладу: {e}")

async def _describe_image(image_bytes: bytes) -> str:
    try:
        response = openai.Image.create(
            image=image_bytes,
            caption=True,
            response_format="json"
        )
        # Обробка відповіді
        if isinstance(response, dict):
            return response.get("description") or response.get("caption") or None
        return None
    except OpenAIError as e:
        raise e

async def _describe_image_from_url(image_url: str) -> str:
    try:
        response = openai.Image.create(
            image_url=image_url,
            caption=True,
            response_format="json"
            )
            if isinstance(response, dict):
                return (response.get("description") or
                response.get("caption") or
                response.get("text") or
                None)
            return None
    except OpenAIError as e:
        raise e