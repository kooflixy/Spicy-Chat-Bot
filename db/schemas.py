import datetime
from pydantic import BaseModel


class UsersAddDTO(BaseModel):
    id: int
    username: str
    char_id: str
    conv_id: str

class UsersDTO(UsersAddDTO):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SpicyUsersRefreshTokensAddDTO(BaseModel):
    id: str
    refresh_token: str

class SpicyUsersRefreshTokensDTO(SpicyUsersRefreshTokensAddDTO):
    created_at: datetime.datetime
    updated_at: datetime.datetime