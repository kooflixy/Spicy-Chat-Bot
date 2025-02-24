from spicy_api.auth.user import SpicyUser
from db.queries.orm import AsyncORM

class SpecialSpicyUser(SpicyUser):
    def __init__(self, logs = True):
        super().__init__(logs)
    
    async def _get_tokens(self, refresh_token, client_id) -> None:
        '''Receives a new refresh token and sends it to the database'''
        res = await super()._get_tokens(refresh_token, client_id)

        await AsyncORM.update_refresh_token(
            spicy_user_id=self.user_id, # is defined at the beginning of activate(), which is supposed to always run first
            new_refresh_token=self.refresh_token # Because refresh_token updates in super()._get_tokens(refresh_token, client_id)
        )
        return res

    async def activate(self, user_id: str) -> None:
        '''Takes refresh_token from the database and activates SpecialSpicyUser'''
        self.user_id = user_id

        spicy_user_refresh_token = await AsyncORM.get_refresh_token(user_id)
        spicy_user_refresh_token = spicy_user_refresh_token.as_dto()
        
        return await super().activate(
            spicy_user_refresh_token.refresh_token,
            spicy_user_refresh_token.client_id
        )