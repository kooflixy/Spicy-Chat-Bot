import datetime
from typing import Annotated
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

import config
from db.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_attp = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_attp = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())")
    )]


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str | None] = mapped_column(String(100))
    char_id: Mapped[str] = mapped_column(default=config.SPICY_DEFAULT_AI_BOT_ID)
    conv_id: Mapped[str]
    created_at: Mapped[created_attp]
    updated_at: Mapped[updated_attp]