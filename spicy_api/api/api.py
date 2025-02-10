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