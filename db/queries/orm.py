from aiogram.types import Message

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import config
from db.database import Base, async_engine, async_session_factory
from db.models import UsersORM, SpicyUsersRefreshTokensORM, SpicyBotHistoryORM

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    #users interactions
    @staticmethod
    async def insert_user(user_id: int, username: str, conv_id: str) -> None:
        user = UsersORM(
            id = user_id,
            username= username,
            conv_id = conv_id,
        )
        async with async_session_factory() as session:
            session.add(user)
            await session.commit()
    
    @staticmethod
    async def get_user(user_id: int) -> UsersORM:
        async with async_session_factory() as session:
            user = await session.get(UsersORM, user_id)
        return user
    
    #spicy user refresh token interactions
    @staticmethod
    async def get_refresh_token(spicy_user_id: str) -> SpicyUsersRefreshTokensORM:
        async with async_session_factory() as session:
            spicy_user_refresh_token = await session.get(SpicyUsersRefreshTokensORM, spicy_user_id)
            return spicy_user_refresh_token
    
    @staticmethod
    async def update_refresh_token(spicy_user_id: str, new_refresh_token: str) -> None:
        async with async_session_factory() as session:
            spicy_user_refresh_token = await session.get(SpicyUsersRefreshTokensORM, spicy_user_id)
            spicy_user_refresh_token.refresh_token = new_refresh_token
            await session.commit()
    
    @staticmethod
    async def insert_refresh_token(spicy_user_id: str, client_id: str, refresh_token: str) -> None:
        spicy_user_refresh_token = SpicyUsersRefreshTokensORM(
            id = spicy_user_id,
            client_id = client_id,
            refresh_token = refresh_token
        )
        async with async_session_factory() as session:
            session.add(spicy_user_refresh_token)
            await session.commit()
    
    @staticmethod
    async def get_conv_history(session: AsyncSession, message: Message):
        query = (
            select(
                SpicyBotHistoryORM
            )
            .filter_by(user_id=message.chat.id)
            .order_by(SpicyBotHistoryORM.updated_at.desc())
        )
        res = await session.execute(query)
        return res.scalars().all()

    @staticmethod
    async def add_conv_in_history(session: AsyncSession, message: Message, char_id: str, conv_id: str, bot_name: str, spicy_api):
        query = (
            select(
                SpicyBotHistoryORM
            )
            .filter_by(user_id=message.chat.id)
            .order_by(SpicyBotHistoryORM.updated_at.asc())
        )
        chats = (await session.execute(query)).scalars().all()

        if len(chats) >= config.MAX_HISTORY_BOTS_COUNT:
            await spicy_api.delete_conversation(chats[0].conv_id)
            await session.delete(SpicyBotHistoryORM, chats[0].id)
        
        new_chat = SpicyBotHistoryORM(
            user_id=message.chat.id,
            char_id=char_id,
            conv_id=conv_id,
            bot_name=bot_name
        )

        session.add(new_chat)