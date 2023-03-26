import os
import secrets

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    API_STR: str = ""
    SECRET_KEY: str = secrets.token_urlsafe(32)

    SERVER_HOST: str = os.getenv("SERVER_HOST")
    SERVER_PORT: int = os.getenv("SERVER_PORT")

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    MESSENGER_BOT_NAME: str = os.getenv("MESSENGER_BOT_NAME")

    """
    Facebook Config
    """

    FB_PAGE_TOKEN: str = os.getenv("FB_PAGE_TOKEN")
    CALLBACK_VERIFY_TOKEN: str = os.getenv("CALLBACK_VERIFY_TOKEN")

    SECONDARY_RECEIVER_ID: str = os.getenv("SECONDARY_RECEIVER_ID")
    PRIMARY_RECEIVER_ID: str = os.getenv("PRIMARY_RECEIVER_ID")

    """
    Viber Config
    """
    VIBER_BOT_NAME: str = os.getenv("VIBER_BOT_NAME")
    VIBER_AUTH_TOKEN: str = os.getenv("VIBER_AUTH_TOKEN")
    WEBHOOK_SERVER_URL: str = os.getenv("WEBHOOK_SERVER_URL")

    class Config:
        case_sensitive = True


settings = Settings()

API = "https://graph.facebook.com/v13.0/me/messages?access_token=" + settings.FB_PAGE_TOKEN

SETUP_PROFILE_API = "https://graph.facebook.com/v13.0/me/messenger_profile?access_token=" + settings.FB_PAGE_TOKEN

THREAD_CONTROL_API = "https://graph.facebook.com/v13.0/me/pass_thread_control?access_token=" + settings.FB_PAGE_TOKEN
