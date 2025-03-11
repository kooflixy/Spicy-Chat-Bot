from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from db.database import async_session_factory
from db.queries.orm import AsyncORM
from db.models import UsersORM

from core.spicy.classes.special_spicy_user import SpecialSpicyUser
from spicy_api.api.api import SpicyAPI
# from tg_bot.handlers.sai_accs_setts import spicy_api
from tg_bot.contrib.func_logger import UserForLogs

import config
from logging import getLogger

logger = getLogger(__name__)
router = Router()


@router.message(Command('sapiaccstart'))
async def sapiaccstart(message: Message):
    global spicy_api, spicy_user

    spicy_user = SpecialSpicyUser()
    await spicy_user.activate(config.SPICY_ACTIVE_USER_ID)
    spicy_api = SpicyAPI(spicy_user)

    await message.answer('SpicyAPI activated')
    logger.info(f'{sapiaccstart.__name__} is handled {UserForLogs.log_name(message)}: activated {spicy_api=}, {spicy_user=}')

@router.message(CommandStart())
async def start(message: Message):
    '''Creates a new conversation if the user is not registered'''

    user = await AsyncORM.get_user(message.chat.id)

    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if user:
            await message.answer('Вы уже смешарик')
            logger.info(f'{start.__name__} is handled: user is already registered {UserForLogs.log_name(message)}')
            return
        
        bot_message, new_conv_id = await spicy_api.create_conversation('Привет!', config.SPICY_DEFAULT_AI_BOT_ID)

        user = UsersORM(
            id = message.chat.id,
            username = message.chat.full_name,
            conv_id = new_conv_id
        )

        session.add(user)
        await session.commit()

        await message.answer(bot_message)

        logger.info(f'{start.__name__} is handled {UserForLogs.log_name(message)}: {new_conv_id=}')