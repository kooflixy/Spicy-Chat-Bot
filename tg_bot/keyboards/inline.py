from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from spicy_api.api.classes.bot_profile import SpicyBotProfile
from db.models import SpicyBotHistoryORM
from tg_bot.contrib.generator import get_random_smile, generate_time_from_last_choose_for_botlist

class StartToChatAskCD(CallbackData, prefix='start_to_chat_ask_cd'):
    char_id: str

def start_to_chat_ask_ikb(bot_profile: SpicyBotProfile):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Начать переписку', callback_data=StartToChatAskCD(char_id=bot_profile.id).pack())]
        ]
    )

    return kb


class SpicyBotHistoryListCD(CallbackData, prefix='sbot_his'):
    bot_history_id: int
    char_id: str

def show_spicy_bot_history(bot_history: list[SpicyBotHistoryORM]):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'{get_random_smile()}{bot.bot_name} ({generate_time_from_last_choose_for_botlist(bot.updated_at)})', callback_data=SpicyBotHistoryListCD(bot_history_id=bot.id, char_id=bot.char_id).pack())]
            for bot in bot_history
        ]
    )

    return kb



class SpicyBotAskToContinueCD(CallbackData, prefix='spicy_bot_ask_to_continue_cd'):
    bot_id: int

def ask_to_continue_chat(bot_id: int):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Продолжить переписку', callback_data=SpicyBotAskToContinueCD(bot_id=bot_id).pack())]
        ]
    )

    return kb