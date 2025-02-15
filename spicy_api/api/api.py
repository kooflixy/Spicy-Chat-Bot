import logging
from spicy_api import settings
from spicy_api.api.base import BaseSpicyAPI
from spicy_api.auth.user import SpicyUser
from spicy_api.api.classes import convs, bot_profile

logger = logging.getLogger('spicy')

class SpicyAPI(BaseSpicyAPI):
    def __init__(self, user: SpicyUser, logs = True):
        super().__init__(user, logs)

    
    async def get_convesations(self, char_id: str) -> list[convs.SpicyConv]:
        '''Gets a list of all conversations with the bot.'''

        self._check_logs_and_do(logger.info(f'Started trying to get conversations {char_id=}'))
        data = await self._get_response(
            request_type = self.RequestType.GET,
            url = settings.SPICY_GET_CONVERSATIONS_URL.format(char_id = char_id),
            headers = self.headers,
        )
        data = convs.dict_to_SpicyConv(data)

        self._check_logs_and_do(logger.info(f'Conversations were successfully received {char_id=}'))
        return data
    
    async def delete_conversation(self, conv_id: str) -> dict:
        '''Deletes the specified conversation'''
        
        self._check_logs_and_do(logger.info(f'Started trying to delete conversation {conv_id=}'))
        data = await self._get_response(
            request_type=self.RequestType.DELETE,
            url = settings.SPICY_DELETE_CONVERSATION_URL.format(conv_id=conv_id),
            headers=self.headers,
        )
        
        self._check_logs_and_do(logger.info(f'Conversations was successfully deleted {conv_id=}'))
        return data

    async def create_conversation(self, message: str, char_id: str) -> tuple[str, str]:
        '''Returns tuple[bot_msg:str, new_conv_id: str] 
        Sends user's message to new SpicyChat Bot's conversation and returns its answer and id of new conversation'''

        self._check_logs_and_do(logger.info(f'Trying to send a message and create a new conversation {char_id=}'))
        data = await self._get_response(
            url = settings.SPICY_SEND_MESSAGE_URL,
            payload = self._create_payload(message=message, character_id=char_id),
            headers = self.headers
        )

        bot_msg: str = data['message']['content']
        new_conv_id: str = data['message']['conversation_id']

        self._check_logs_and_do(logger.info(f'The message was sent successfully and the conversation was successfully created. {char_id=}, {new_conv_id=}'))
        return bot_msg, new_conv_id
    
    async def send_message(self, message: str, char_id: str, conv_id: str) -> str:
        '''Sends user's message to SpicyChat Bot and return its response'''

        self._check_logs_and_do(logger.info(f'The message has been sent to {char_id=}, {conv_id=}'))
        data = await self._get_response(
            url = settings.SPICY_SEND_MESSAGE_URL,
            payload = self._create_payload(message=message, character_id=char_id, conversation_id=conv_id),
            headers = self.headers
        )

        bot_msg = data["message"]["content"]

        self._check_logs_and_do(logger.info(f'The message was successfully responded to {char_id=}, {conv_id=}'))
        return bot_msg
    
    async def get_bot_profile(self, char_id: str):
        '''Gets information about the bot's profile'''
        
        self._check_logs_and_do(logger.info(f'Starting an attempt to get the bot\'s profile {char_id=}'))
        data = await self._get_response(
            request_type=self.RequestType.GET,
            url = settings.SPICY_GET_BOT_PROFILE_URL.format(char_id = char_id),
            headers=self.headers,
        )
        bot = bot_profile.SpicyBotProfile(**data)

        self._check_logs_and_do(logger.info(f'The bot profile was successfully received {char_id=}'))
        return bot