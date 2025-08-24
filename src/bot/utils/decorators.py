from functools import wraps
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from db.enums import SessionMode


def with_clean_keyboard(func):
    """
    Decorator that clears the reply keyboard and quiz state when switching out of quiz mode.

    This decorator checks if the user was previously in QUIZ mode. If so, it sends a message
    removing the quiz keyboard and clears any stored quiz progress in context.user_data.

    Args:
        func (Callable): The async handler function to wrap.

    Returns:
        Callable: A wrapped async function with keyboard cleanup logic.
    """
