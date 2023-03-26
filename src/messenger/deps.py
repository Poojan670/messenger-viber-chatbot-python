from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.messenger.helper import send_message
from src.db.base import get_db
from src.models.models import LanguageEnum, UserInfo
from src.messenger.msg import back_to_process_menu
from src.messenger.templates import template_messages


class Language:
    def __init__(self, sender_id: str, language: LanguageEnum, db: Session = Depends(get_db)):
        self.sender_id = sender_id
        self.language = language
        self.db = db

    async def change_language_prompt(self):
        user = self.db.query(UserInfo).filter(UserInfo.user_id == self.sender_id).first()
        user.language = self.language
        self.db.commit()

    async def select_english_language(self):
        await send_message(self.sender_id, {"text": "English language selected successfully"})
        await self.change_language_prompt()
        await back_to_process_menu(self.sender_id, self.language)

    async def select_nepali_language(self):
        await send_message(self.sender_id, {"text": "नेपाली भाषा सफलतापूर्वक चयन गरियो"})
        await self.change_language_prompt()
        await self.back_to_language_choices()

    async def send_language_choices(self):
        response = template_messages.language_template(self.language)
        await send_message(self.sender_id, response)

    async def back_to_language_choices(self):
        await self.send_language_choices()


