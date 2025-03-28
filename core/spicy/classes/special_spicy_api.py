from spicy_api.api.api import SpicyAPI
from spicy_api.api.classes.bot_profile import SpicyBotProfile
from core.contrib import replace_asterix_with_italic
from yandexfreetranslate import YandexFreeTranslate

yt = YandexFreeTranslate(api = "ios")

class SpecialSpicyAPI(SpicyAPI):
    def __init__(self, user, logs=True):
        super().__init__(user, logs)
    
    async def send_message(self, message, char_id, conv_id, username: str, lang: str = 'ru'):
        msg = await super().send_message(message, char_id, conv_id)
        msg = msg.replace(self.user.name, 'you')
        msg = yt.translate('en', 'ru', msg)
        # msg = msg.replace('{{user}}', username)
        msg = replace_asterix_with_italic(msg)
        
        return msg
    
    async def create_conversation(self, message, char_id, username: str):
        resp = await super().create_conversation(message, char_id)
        msg = resp[0].replace(self.user.name, username)
        msg = yt.translate('en', 'ru', msg)
        msg = replace_asterix_with_italic(msg)
        return msg, resp[1]
    
    async def get_bot_profile(self, char_id) -> SpicyBotProfile:
        bot =  await super().get_bot_profile(char_id)

        bot.greeting = yt.translate('en', 'ru', replace_asterix_with_italic(bot.greeting.replace('{{char}}', bot.name)))
        bot.title = yt.translate('en', 'ru', replace_asterix_with_italic(bot.title.replace('{{char}}', bot.name)))


        return bot