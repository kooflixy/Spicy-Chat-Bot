from datetime import datetime
from logging import getLogger
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
import config
from tg_bot.contrib.active_chat_sesses_checker import active_chats_sesses_checker
from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.filters.is_admin import IsAdmin

logger = getLogger(__name__)
router = Router()

@router.message(F.text.casefold().in_(['/getstats', '!стата']), IsAdmin(config.TG_ADMINS))
async def getstats(message: Message):
    await message.answer(text=f'''
Статистика {str(datetime.now())[:-7]}

Активных пользователей: {active_chats_sesses_checker.count()}
''')
    logger.info(f'{getstats.__name__} is handled {UserForLogs.log_name(message)}')


@router.message(F.text.casefold().in_(['/getlogs', '!логи']), IsAdmin(config.TG_ADMINS))
async def getlogs(message: Message):
    await message.answer_document(FSInputFile('.log', 'logs.log'))
    logger.info(f'{getlogs.__name__} is handled {UserForLogs.log_name(message)}')