from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class SearchListPagination(CallbackData, prefix='pag'):
    action: str
    page: int

def pagination_ikb(page: int = 0):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️', callback_data=SearchListPagination(page=page, action='prev').pack()),
                InlineKeyboardButton(text='➡️', callback_data=SearchListPagination(page=page, action='next').pack()),
            ]
        ]
    )

    return kb