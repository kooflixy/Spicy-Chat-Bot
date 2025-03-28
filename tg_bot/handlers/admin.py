from datetime import datetime
from aiogram import F, Router
from aiogram.types import Message
import config
from tg_bot.contrib.active_chat_sesses_checker import active_chats_sesses_checker
from tg_bot.filters.is_admin import IsAdmin

router = Router()

@router.message(F.text.casefold().in_(['/getstats', '!стата']), IsAdmin(config.TG_ADMINS))
async def getstats(message: Message):
    await message.answer(text=f'''
Статистика {str(datetime.now())[:-7]}

Активных пользователей: {active_chats_sesses_checker.count()}
''')