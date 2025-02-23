from sqlalchemy import select

from db.database import Base, async_engine, async_session_factory
from db.models import UsersORM, SpicyUsersRefreshTokensORM

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
    async def insert_refresh_token(spicy_user_id: str, refresh_token: str) -> None:
        spicy_user_refresh_token = SpicyUsersRefreshTokensORM(
            id = spicy_user_id,
            refresh_token = refresh_token
        )
        async with async_session_factory() as session:
            session.add(spicy_user_refresh_token)
            await session.commit()