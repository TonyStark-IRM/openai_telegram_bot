from telegram import (
    Update,
    InputFile,
    BotCommand,
    BotCommandScopeChat,
    MenuButtonCommands
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def send_html_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        text: str,
) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
    )


async def send_image_bytes(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        image_bytes: bytes,
        image_name: str = "image.jpg",
        caption: str = None,
        parse_mode: str = ParseMode.HTML
) -> None:
    await context.bot.send_photo(
        
    )