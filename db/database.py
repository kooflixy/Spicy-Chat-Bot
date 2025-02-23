from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

import config

database_url_asyncpg = f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

async_engine = create_async_engine(
    url = database_url_asyncpg
)

async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    
    repr_cols_num = 2
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        
        return f'<{self.__class__.__name__} {','.join(cols)}>'
    

    dto_schema: BaseModel

    def as_dto(self):
        '''Converts ORM class to its DTO schema'''
        return self.dto_schema.model_validate(self.dto_schema, from_attributes=True)