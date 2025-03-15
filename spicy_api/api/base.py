import logging
import aiohttp

from spicy_api.auth.exceptions import SpicyUserIsNotActivated
from spicy_api.auth.user import SpicyUser

logger = logging.getLogger('spicy')

class BaseSpicyAPI:
    def __init__(self, user: SpicyUser, logs: bool = True):
        if not user._is_activated:
            raise SpicyUserIsNotActivated(f'{user} hasn\'t bearer and refresh_token. To get it, please, activate your SpicyUser: "await SpicyUser().activate(refresh_token=YOUR_REFRESH_TOKEN)"')
        self.user = user
        self._logs = logs
        self.headers = {
                    "Authorization": f"Bearer {user.bearer}",
                }

    class RequestType:
        GET = 'get'
        POST = 'post'
        DELETE = 'delete'

    def _create_payload(self, **kwargs):
        return kwargs
    
    def _check_logs_and_do(self, function):
        '''Checks whether logs need to be done and executes the passed function if necessary.
        
        Usage example:
        self._check_logs_and_do(logger.info("Some log"))
        '''
        def wrapped(*args, **kwargs):
            if self._logs: function(*args, **kwargs)
        return wrapped

    def _bearer_observer(function):
        '''A decorator whose role is to update the Bearer token if it gets old.'''
        async def wrapped(*args, **kwargs):
            try:
                return await function(*args, **kwargs)
            except:
                self: BaseSpicyAPI = args[0]
                await self.user.update_bearer()
                self.headers = {
                    "Authorization": f"Bearer {self.user.bearer}",
                }

                if self._logs: logger.info('Bearer and headers in SpicyAPI have been updated.')
                return await function(*args, **kwargs)
        return wrapped

    @_bearer_observer
    async def _get_response(self, url: str, headers: dict, payload: dict = {}, request_type: RequestType = RequestType.POST) -> dict:
        '''Receives a response using aiohttp. Designed to avoid writing the same action over and over again.'''
        
        async with aiohttp.ClientSession() as session:

            if request_type == self.RequestType.POST:
                response = await session.post(url, headers=headers, json=payload)
            elif request_type == self.RequestType.GET:
                response = await session.get(url, headers=headers, json=payload)
            elif request_type == self.RequestType.DELETE:
                response = await session.delete(url, headers=headers, json=payload)
                
            data = await response.json()
            if response.status == 200:
                return data
                # raise Exception('NADO OBNOVIT BEARER')
            else:
                logger.error(f'response error: {response.status}')
                return response.status