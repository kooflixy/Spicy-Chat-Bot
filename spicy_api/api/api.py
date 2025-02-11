import logging
from spicy_api import settings
from spicy_api.api.base import BaseSpicyAPI
from spicy_api.auth.user import SpicyUser

logger = logging.getLogger('spicy')

class SpicyAPI(BaseSpicyAPI):
    def __init__(self, user: SpicyUser, logs = True):
        super().__init__(user, logs)

    async def send_message(self, message: str, char_id: str, conv_id: str) -> str:
        """Sends user's message to SpicyChat Bot and return its response"""

        self._check_logs_and_do(logger.info(f'The message has been sent to {char_id=}, {conv_id=}'))
        data = await self._get_response(
            url = settings.SPICY_SEND_MESSAGE_URL,
            payload = self._create_payload(message=message, character_id=char_id, conversation_id=conv_id),
            headers = self.headers
        )

        bot_msg = data["message"]["content"]

        self._check_logs_and_do(logger.info(f'The message was successfully responded to {char_id=}, {conv_id=}'))
        return bot_msg
    
    async def create_chat(self, message: str, char_id: str) -> tuple[str, str]:
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