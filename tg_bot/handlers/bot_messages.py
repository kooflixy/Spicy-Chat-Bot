from logging import getLogger
from aiogram import F, Router
from aiogram.types import Message

from tg_bot.contrib.func_logger import UserForLogs

logger = getLogger(__name__)
router = Router()

@router.message(F.text.casefold().in_(['🔍поиск', 'поиск']))
async def search_rkb_ans(message: Message):
    await message.answer('Для поиска напишите "!поиск [имя бота]"\nДля просмотра рекомендаций пропишите просто "!поиск"')
    logger.info(f'{search_rkb_ans.__name__} is handled {UserForLogs.log_name(message)}')

@router.message(F.text.casefold().in_(['⚙настройки', 'настройки']))
async def setts_rkb_ans(message: Message):
    await message.answer('Язык: RU🇷🇺')
    logger.info(f'{search_rkb_ans.__name__} is handled {UserForLogs.log_name(message)}')