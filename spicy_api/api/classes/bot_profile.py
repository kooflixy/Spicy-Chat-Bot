
from pydantic import BaseModel

from spicy_api import settings


class SpicyBotProfileSchema(BaseModel):
    id: str
    name: str
    title: str
    visibility: str
    creator_username: str
    creator_user_id: str
    greeting: str
    avatar_url: str
    num_messages: int
    is_nsfw: bool
    avatar_is_nsfw: bool
    definition_visible: bool
    tags: list
    lora_status: str
    token_count: int
    reportsType: list = []

class SpicyBotProfile(SpicyBotProfileSchema):
    '''This class was created for more convenient interaction with the bot profile obtained from a profile request for this particular bot.'''
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)
    
    def __str__(self):
        return f'SpicyBot({self.name})'


class SpicyBotProfileSearchDTO(BaseModel):
    name: str
    id: str
    avatar_url: str
    title: str
    tags: list[str]

    def __str__(self):
        return f'<{self.__class__.__name__} name={self.name}>'

def dict_to_spicybotdto(data: list) -> list[SpicyBotProfileSearchDTO]:
    res = []

    for char in data:
        char = char['document']
        res.append(
            SpicyBotProfileSearchDTO(
                name = char['name'],
                id = char['id'],
                avatar_url = settings.SPICY_AVATAR_URL.format(avatar_slug=char['avatar_url']),
                title = char['title'],
                tags = char['tags'],
            )
        )
    
    return res