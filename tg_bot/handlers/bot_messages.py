from aiogram import F, Router
from aiogram.types import Message

router = Router()

@router.message(F.text.casefold().in_(['🔍поиск', 'поиск']))
async def search_rkb_ans(message: Message):
    await message.answer('Для поиска напишите "!поиск [имя бота]"\nДля просмотра рекомендаций пропишите просто "!поиск"')

@router.message(F.text.casefold().in_(['⚙настройки', 'настройки']))
async def search_rkb_ans(message: Message):
    await message.answer('Язык: RU🇷🇺')