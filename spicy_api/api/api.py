import aiohttp
import logging
from spicy_api.contrib.for_logging import do_log
from spicy_api import settings
from spicy_api.api.base import BaseSpicyAPI
from spicy_api.auth.user import SpicyUser
from spicy_api.api.classes import convs, bot_profile

logger = logging.getLogger('spicy')

class SpicyAPI(BaseSpicyAPI):
    def __init__(self, user: SpicyUser, logs = True):
        super().__init__(user, logs)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.user.username}>'
    
    @do_log
    async def get_convesations(self, char_id: str) -> list[convs.SpicyConv]:
        '''Gets a list of all conversations with the bot.'''

        data = await self._get_response(
            request_type = self.RequestType.GET,
            url = settings.SPICY_GET_CONVERSATIONS_URL.format(char_id = char_id),
            headers = self.headers,
        )
        data = convs.dict_to_SpicyConv(data)

        return data
    
    @do_log
    async def delete_conversation(self, conv_id: str) -> dict:
        '''Deletes the specified conversation'''
        
        data = await self._get_response(
            request_type=self.RequestType.DELETE,
            url = settings.SPICY_DELETE_CONVERSATION_URL.format(conv_id=conv_id),
            headers=self.headers,
        )
        
        return data

    @do_log
    async def create_conversation(self, message: str, char_id: str) -> tuple[str, str]:
        '''Returns tuple[bot_msg:str, new_conv_id: str] 
        Sends user's message to new SpicyChat Bot's conversation and returns its answer and id of new conversation'''

        data = await self._get_response(
            url = settings.SPICY_SEND_MESSAGE_URL,
            payload = self._create_payload(message=message, character_id=char_id),
            headers = self.headers
        )
        if data == 403:
            return
        
        bot_msg: str = data['message']['content']
        new_conv_id: str = data['message']['conversation_id']

        return bot_msg, new_conv_id
    
    @do_log
    async def send_message(self, message: str, char_id: str, conv_id: str) -> str:
        '''Sends user's message to SpicyChat Bot and return its response'''

        data = await self._get_response(
            url = settings.SPICY_SEND_MESSAGE_URL,
            payload = self._create_payload(message=message, character_id=char_id, conversation_id=conv_id),
            headers = self.headers
        )

        bot_msg = data["message"]["content"]

        return bot_msg
    
    @do_log
    async def get_bot_profile(self, char_id: str):
        '''Gets information about the bot's profile'''
        
        data = await self._get_response(
            request_type=self.RequestType.GET,
            url = settings.SPICY_GET_BOT_PROFILE_URL.format(char_id = char_id),
            headers=self.headers,
        )

        if not data:
            return
        if data == 403:
            return
        
        bot = bot_profile.SpicyBotProfile(**data)

        bot.avatar_url = 'https://ndsc.b-cdn.net/' + bot.avatar_url

        return bot

    @do_log
    async def search_bots(self, bot_name: str = None):
        '''Search bots'''
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url = settings.SPICY_SEARCH_BOTS_URL,
                json=settings.genereate_search_data(bot_name)
            )
        
        data = response['results'][0]['hits']
        data = bot_profile.dict_to_spicybotdto(data)

        return data