import logging
import aiohttp

from spicy_api import settings
from spicy_api.auth.exceptions import SpicyUserIsNotActivated
from spicy_api.contrib.repeats import async_retry

logger = logging.getLogger('spicy')

class SpicyAuth:
    @staticmethod
    @async_retry
    async def get_bearer_n_refresh(refresh_token: str, client_id: str) -> dict:
        async with aiohttp.ClientSession() as session:
            payload = {
                'client_id': client_id,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }

            response = await session.post(
                url=settings.SPICY_USER_AUTH_URL,
                data=payload,
            )

            data = await response.json()
            # logger.info("Bearer and refresh token were got")
            return data

class SpicyUserProfile:
    @staticmethod
    @async_retry
    async def get_profile(bearer: str) -> dict:
        headers = {
                    "Authorization": f"Bearer {bearer}",
                }
        
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url = settings.SPICY_USER_DETAILS_URL,
                headers = headers,
            )
            data = await response.json()
            # logger.info('Profile info was got')
            return data




class SpicyUser:
    '''This class represents a logged-in SpicyChat user.

    Usage example:
    async def login():
        user = SpicyUser()
        await user.activate(refresh_token=YOUR_REFRESH_TOKEN)
    '''

    _is_activated = False

    def __getattr__(self, attr: str):
        if attr == 'bearer' or attr == 'refresh_token':
            raise SpicyUserIsNotActivated(f'{self} hasn\'t bearer and refresh_token. To get it, please, activate your SpicyUser: "await SpicyUser().activate(refresh_token=YOUR_REFRESH_TOKEN)"')

    def __str__(self):
        if self._is_activated:
            return f'SpicyUser({self.username})'
        return 'SpicyUser'


    async def _get_tokens(self, refresh_token: str, client_id: str):
        '''Gets Bearer and refresh_token'''
        data = await SpicyAuth.get_bearer_n_refresh(refresh_token, client_id)
        self.client_id: str = client_id
        self.bearer: str = data['access_token']
        self.refresh_token: str = data['refresh_token']
    
    async def _get_profile(self):
        '''Gets user info'''
        profile_info = await SpicyUserProfile.get_profile(self.bearer)
        profile_info = profile_info['user']
        self.name: str = profile_info['name']
        self.username: str = profile_info['username']



    async def activate(self, refresh_token: str, client_id: str):
        '''Activates the user by receiving a Bearer and updating the refresh_token if necessary. Gets user profile.'''
        await self._get_tokens(refresh_token, client_id)
        await self._get_profile()
        
        self._is_activated = True
        logger.info(f'{self} was activated')
    
    
    async def update_bearer(self):
        '''Updates the Bearer and updates the refresh_token if necessary.'''
        await self._get_tokens(self.refresh_token, self.client_id)

        logger.info(f"{self}: Bearer and refresh token were updated")