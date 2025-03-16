import datetime
from typing import Annotated
from sqlalchemy import ForeignKey, String, text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

import config
from db.schemas import UsersDTO, SpicyUsersRefreshTokensDTO
from db.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_attp = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_attp = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())")
    )]


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(100))
    char_id: Mapped[str]
    conv_id: Mapped[str]
    created_at: Mapped[created_attp]
    updated_at: Mapped[updated_attp]

    repr_cols_num = 2

    dto_schema = UsersDTO

    def as_dto(self) -> UsersDTO:
        return super().as_dto()


class SpicyUsersRefreshTokensORM(Base):
    '''С этой моделью предполагается такая работа:
    Запуск программы -> активация SpicyUser(или дочерних ему классов) -> в методе активации сначала из базы извлекается refresh token и далее передается на активацию
    Истечение срока refresh token`а -> получение нового -> запись нового токена в бд
    В теории, т.к. программа будет запускаться один раз и срок токена будет истекать раз в день, последовательность выше будет исполняться ОЧЕНЬ редко
    '''
    __tablename__ = 'spicy_users_refresh_tokens'

    id: Mapped[str] = mapped_column(primary_key=True)
    refresh_token: Mapped[str]
    client_id: Mapped[str]
    created_at: Mapped[created_attp]
    updated_at: Mapped[updated_attp]
    
    repr_cols_num = 2

    dto_schema = SpicyUsersRefreshTokensDTO

    def as_dto(self) -> SpicyUsersRefreshTokensDTO:
        return super().as_dto()


class SpicyBotHistoryORM(Base):
    __tablename__ = 'spicy_bot_history'

    id: Mapped[intpk]
    user_id: Mapped[BigInteger] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    char_id: Mapped[str]
    conv_id: Mapped[str]
    created_at: Mapped[created_attp]

    repr_cols_num = 4