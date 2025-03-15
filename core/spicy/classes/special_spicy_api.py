from spicy_api.api.api import SpicyAPI

class SpecialSpicyAPI(SpicyAPI):
    def __init__(self, user, logs=True):
        super().__init__(user, logs)
    
    async def send_message(self, message, char_id, conv_id, username: str):
        resp = await super().send_message(message, char_id, conv_id)
        resp = resp.replace(self.user.name, username)
        return resp
    
    async def create_conversation(self, message, char_id, username: str):
        resp = await super().create_conversation(message, char_id)
        msg = resp[0].replace(self.user.name, username)
        return msg, resp[1]