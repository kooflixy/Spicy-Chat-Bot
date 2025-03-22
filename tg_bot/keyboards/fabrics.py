from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class SearchListPagination(CallbackData, prefix='pag'):
    name: str
    action: str
    page: int

def pagination_ikb(name: str, page: int = 1):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️', callback_data=SearchListPagination(page=page, name=name, action='prev').pack()),
                InlineKeyboardButton(text='➡️', callback_data=SearchListPagination(page=page, name=name, action='next').pack()),
            ]
        ]
    )

    return kb