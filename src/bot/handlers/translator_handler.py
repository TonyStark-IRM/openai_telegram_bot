#
# from __future__ import annotations
#
# from aiogram import types
# from aiogram.filters import Command
# from aiogram.types import Message
# from ..templates.prompts import PROMPT_TRANSLATOR_SYSTEM, PROMPT_TRANSLATOR_USER_TEMPLATE
# import openai
#
# # Прямий обробник команди /translator
# async def translator_command(message: Message):
#     await message.reply(
#         "Введіть текст для перекладу та цільову мову у форматі: текст | мова (наприклад: Hello world | en)"
#     )



from openai import OpenAIError
from telegram import Update
from telegram.ext import ContextTypes

from bot.message_sender import send_html_message
from bot.utils.openai_threads import get_or_create_thread_id
from db.enums import SessionMode, MessageRole
from db.repository import GptThreadRepository
from services import OpenAIClient
from settings import config, get_logger

logger = get_logger(__name__)


async def translator_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mode = context.user_data.get("mode")
    if mode != SessionMode.GPT.value:
        return

    user_message = update.message.text
    tg_user_id = update.effective_user.id

    openai_client: OpenAIClient = context.bot_data["openai_client"]
    thread_repository: GptThreadRepository = context.bot_data["thread_repository"]

    thread_id = await get_or_create_thread_id(tg_user_id, mode, thread_repository, openai_client)

    await thread_repository.add_message(thread_id, role=MessageRole.USER.value, content=user_message)

    try:
        assistant_id = config.ai_assistant_fact_spark_id
        reply = await openai_client.ask(
            assistant_id=assistant_id,
            thread_id=thread_id,
            user_message=user_message
        )
    except OpenAIError as e:
        logger.warning(f"Assistant failed in GPT mode: {e}")
        await update.message.reply_text("Assistant failed to respond. Please try again later.")
        return

    await thread_repository.add_message(thread_id, role=MessageRole.ASSISTANT.value, content=reply)

