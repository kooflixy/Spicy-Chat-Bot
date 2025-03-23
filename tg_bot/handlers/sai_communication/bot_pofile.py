from logging import getLogger
from aiogram import Router, F
from aiogram.types import Message

from db.models import UsersORM
from db.database import async_session_factory

from core.spicy.objs import spicy_api
from tg_bot.keyboards import reply
from tg_bot.contrib.generator import generate_sai_bot_desc
from tg_bot.contrib.func_logger import UserForLogs

router = Router()
logger = getLogger(__name__)

@router.message(F.text.casefold().in_(['/bot_profile', 'бот', '👤бот']))
async def get_bot_profile(message: Message):
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)
        
        bot_profile = await spicy_api.get_bot_profile(user.char_id, message.from_user.full_name)

        await message.reply_photo(
            photo=bot_profile.avatar_url,
            caption=generate_sai_bot_desc(bot_profile),
            reply_markup=reply.menu_rkb
        )

        logger.info(f'{get_bot_profile.__name__} is handled {UserForLogs.log_name(message)}')