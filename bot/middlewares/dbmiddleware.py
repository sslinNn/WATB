from typing import Callable, Awaitable, Dict, Any

import sqlalchemy
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from bot.model.connection import get_connetion_with_db
import sqlalchemy as db


class DBSession(BaseMiddleware):
    def __init__(self, engine: sqlalchemy.Engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine, class_=Session)


    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        conn = self.engine.connect()
        data['request'] = conn
        return await handler(event, data)
