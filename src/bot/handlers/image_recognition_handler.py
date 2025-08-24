from __future__ import annotations

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from PIL import Image
import io
import os

# Приклад імпорту сервісу розпізнавання
# from services.image_recognition_service import analyze_image

async def image_recognition_command(message: Message):
    await message.reply("Надішліть зображення, яке потрібно розпізнати.")

async def image_recognition_process(message: Message):
    # Обробка отриманого зображення
    if not message.photo:
        await message.reply("Будь ласка, надішліть зображення.")
        return

    photo = message.photo[-1]
    file = await photo.get_file()
    path = f"tmp/{photo.file_id}.jpg"
    await file.download(destination=path)

    try:
        # Тут можна викликати ваш сервіс розпізнавання
        # description = analyze_image(path)
        description = "Опис зображення: предмети на столі, можлива взаємодія."  # Заглушка
        await message.reply(description)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
