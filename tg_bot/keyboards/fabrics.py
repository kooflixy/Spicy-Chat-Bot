from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class SearchListPagination(CallbackData, prefix='pag'):
    name: str
    action: str
    page: int

class SearchSuggestBotCD(CallbackData, prefix='sbot'):
    char_id: str

def pagination_ikb(name: str, char_id: str, page: int = 1):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️', callback_data=SearchListPagination(page=page, name=name, action='prev').pack()),
                InlineKeyboardButton(text='👁', callback_data=SearchSuggestBotCD(char_id=char_id).pack()),
                InlineKeyboardButton(text='➡️', callback_data=SearchListPagination(page=page, name=name, action='next').pack()),
            ]
        ]
    )

    return kb