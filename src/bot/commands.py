from openai import OpenAIError
from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import get_menu_buttons
from bot.message_sender import send_html_message, send_image_bytes, show_menu
from bot.resource_loader import load_message, load_image, load_menu
from bot.utils.decorators import with_clean_keyboard
from bot.utils.openai_threads import get_or_create_thread_id
from db.enums import SessionMode, MessageRole
from db.repository import GptThreadRepository
from services import OpenAIClient
from settings import config, get_logger

logger = get_logger(__name__)