from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class AppConfig(BaseSettings):
    openai_api_key: str
    tg_bot_api_key: str

openai_model: str = "gpt_3.5-turbo"
openai_model_temperature: float = 1.5

path_to_messages: BASE_DIR/"resources"/"messages"
path_to_images: BASE_DIR/"resources"/"images"
path_to_menus: BASE_DIR/"resources"/"menus"
path_to_promts: BASE_DIR/"resources"/"prompts"

path_to_logs: BASE_DIR/"logs"

path_to_db: BASE_DIR/"storage"/"chat_sessions.db"

model_config = SettingsConfigDict(
    env_file=str(BASE_DIR / ".env"),
    env_file_encoding = "utf-8"
)


config = AppConfig()
