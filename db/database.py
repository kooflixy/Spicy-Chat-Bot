from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import config

database_url_asyncpg = f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

async_engine = create_async_engine(
    url = database_url_asyncpg
)

async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    ...