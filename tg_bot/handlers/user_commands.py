from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from core.spicy.objs import spicy_api
from db.database import async_session_factory
from db.models import UsersORM

from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.keyboards import reply

import config
from logging import getLogger

logger = getLogger(__name__)
router = Router()



@router.message(CommandStart())
async def start(message: Message):
    '''Creates a new conversation if the user is not registered'''

    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if user:
            await message.answer('Вы уже смешарик', reply_markup=reply.menu_rkb)
            logger.info(f'{start.__name__} is handled: user is already registered {UserForLogs.log_name(message)}')
            return
        
        bot_message, new_conv_id = await spicy_api.create_conversation('Привет!', config.SPICY_DEFAULT_AI_BOT_ID, message.from_user.full_name)

        user = UsersORM(
            id = message.chat.id,
            username = message.chat.full_name,
            char_id = config.SPICY_DEFAULT_AI_BOT_ID,
            conv_id = new_conv_id
        )

        session.add(user)
        await session.commit()

        await message.answer(bot_message, reply_markup=reply.menu_rkb)

        logger.info(f'{start.__name__} is handled {UserForLogs.log_name(message)}: {new_conv_id=}')