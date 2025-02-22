from db.database import Base, async_engine, async_session_factory
from db.models import UsersORM

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    @staticmethod
    async def insert_user(id: int, username: str, conv_id: str):
        user = UsersORM(
            id = id,
            username= username,
            conv_id = conv_id,
        )
        async with async_session_factory() as session:
            session.add(user)
            await session.commit()