from __future__ import annotations

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from PIL import Image
import io
import os

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
        description = "Опис зображення: предмети на столі, можлива взаємодія."
        await message.reply(description)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
