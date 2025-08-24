from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from bot.commands import start, random, gpt, quiz, translator, image_recognition
from bot.handlers.message_router import message_router
from bot.handlers.quiz_handler import handle_quiz_topic_selection
from bot.handlers.translator_handler import handle_message_router
from bot.handlers.image_recognition_handler import handle_image_recognition_file_load

from db.initializer import DatabaseInitializer
from db.repository import GptThreadRepository
from services import OpenAIClient
from settings.config import config
from src.bot.handlers.image_recognition_handler import image_recognition_command


def main():
    """
    Starts the Telegram bot application.

    This function performs the following steps:
    - Initializes the SQLite database for GPT sessions and messages.
    - Creates an OpenAI client instance for communication with assistants.
    - Registers all command, message, and callback query handlers for the bot.
    - Starts polling Telegram for updates.

    Handlers:
        - /start: Opens the main menu with available features.
        - /random: Sends a random technical fact from the assistant.
        - /gpt: Enters GPT chat mode, allowing users to ask questions.
        - /quiz: Launches the quiz mode with topic selection.
        - /translator: Translate a typed text.
        - /image_recognition: Allows users to upload image and receive details recognition report

        - message_router: Routes user text input to GPT or quiz mode depending on session.
        - CallbackQueryHandler with patterns:
            - ^start$: Reopens main menu.
            - ^random$: Triggers another fact.
            - ^quiz_(python|javascript|docker|web)$: Starts quiz generation for the selected topic.

    Environment:
        Requires configuration values from the `config`:
            - OpenAI API key and model name
            - Telegram bot token
            - SQLite database path

    Raises:
        RuntimeError: If the bot fails to initialize or connect to the Telegram API.
    """
    db_initializer = DatabaseInitializer(config.path_to_db)
    db_initializer.create_tables()

    thread_repository = GptThreadRepository(config.path_to_db)

    openai_client = OpenAIClient(
        openai_api_key=config.openai_api_key,
        model=config.openai_model,
        temperature=config.openai_model_temperature
    )

    app = ApplicationBuilder().token(config.tg_bot_api_key).build()

    app.bot_data["openai_client"] = openai_client
    app.bot_data["thread_repository"] = thread_repository

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random))
    app.add_handler(CommandHandler("gpt", gpt))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("translator", translator))
    app.add_handler(CommandHandler("image_recognition", image_recognition))

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_router))

    app.add_handler(CallbackQueryHandler(start, pattern="^start$"))
    app.add_handler(CallbackQueryHandler(random, pattern="^random$"))
    app.add_handler(CallbackQueryHandler(handle_quiz_topic_selection, pattern="^quiz_(python|javascript|docker|web)$"))
    app.add_handler(CallbackQueryHandler(translator, pattern="^translator$"))
    app.add_handler(CallbackQueryHandler(image_recognition, pattern="^image_recognition_(jpg|web)$"))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
