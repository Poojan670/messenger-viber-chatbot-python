from enum import Enum

from sqlalchemy import (Column, String,
                        Text, DateTime)
from sqlalchemy.dialects.postgresql import ENUM

from src.db.base import Base
from sqlalchemy.sql import func


class MessageLog(Base):
    __tablename__ = 'message_log'

    id = Column(String(100), primary_key=True)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LanguageEnum(Enum):
    english = 'ENGLISH'
    nepali = 'NEPALI'


class UserInfo(Base):
    __tablename__ = "app_user"

    id = Column(String(100), primary_key=True)
    user_id = Column(String(255))

    language = Column(ENUM(LanguageEnum), nullable=False)
