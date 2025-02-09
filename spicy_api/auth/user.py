import logging
import aiohttp

from spicy_api import settings
from spicy_api.contrib.repeats import async_retry

logger = logging.getLogger(__name__)

class SpicyAuth:
    @staticmethod
    @async_retry
    async def get_bearer_n_refresh(refresh_token: str) -> str:
        async with aiohttp.ClientSession() as session:
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }

            response = await session.post(
                url=settings.SPICY_USER_AUTH_URL,
                data=payload,
            )

            data = await response.json()
            logger.info("Bearer and refresh token were got")
            return data




class SpicyUser:
    '''This class represents a logged-in SpicyChat user.

    Usage example:
    async def login():
        user = SpicyUser()
        await user.activate(refresh_token=YOUR_REFRESH_TOKEN)
    '''

    _is_activated = False


    async def _get_tokens(self, refresh_token: str):
        data = await SpicyAuth.get_bearer_n_refresh(refresh_token)
        self.bearer = data['access_token']
        self.refresh_token = data['refresh_token']


    async def activate(self, refresh_token: str):
        await self._get_tokens(refresh_token)

        self._is_activated = True
        logger.info('SpicyUser was activated')
    
    
    async def update_bearer(self):
        await self._get_tokens(self.refresh_token)

        logger.info("Bearer and refresh token were updated")