from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from spicy_api.api.classes.bot_profile import SpicyBotProfile

class StartToChatAskCD(CallbackData, prefix='start_to_chat_ask_cd'):
    char_id: str

def start_to_chat_ask_ikb(bot_profile: SpicyBotProfile):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Начать переписку', callback_data=StartToChatAskCD(char_id=bot_profile.id).pack())]
        ]
    )

    return kb