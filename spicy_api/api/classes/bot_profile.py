
from pydantic import BaseModel


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