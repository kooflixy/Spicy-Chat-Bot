from sqlalchemy import select

from db.database import Base, async_engine, async_session_factory
from db.models import UsersORM

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    @staticmethod
    async def insert_user(user_id: int, username: str, conv_id: str):
        user = UsersORM(
            id = user_id,
            username= username,
            conv_id = conv_id,
        )
        async with async_session_factory() as session:
            session.add(user)
            await session.commit()
    
    @staticmethod
    async def get_user(user_id: int):
        async with async_session_factory() as session:
            user = await session.get(UsersORM, user_id)
            return user