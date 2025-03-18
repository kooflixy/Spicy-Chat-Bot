from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👤Бот'),
        ],
        [
            KeyboardButton(text='♻Обновить чат'),
            KeyboardButton(text='📃История')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)