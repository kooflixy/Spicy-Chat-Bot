from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from db.database import async_session_factory
from db.queries.orm import AsyncORM
from db.models import UsersORM

from tg_bot.handlers.sai_accs_setts import spicy_api

import config

router = Router()

@router.message(CommandStart())
async def start(message: Message):

    # async with async_session_factory() as session:
    #     user = await session.get(UsersORM, message.chat.id)
    #     print(user)
    #     msg, new_conv_id = await spicy_api.create_conversation('Привет', config.SPICY_DEFAULT_AI_BOT_ID)
    #     await message.answer(msg)

    user = await AsyncORM.get_user(message.chat.id)

    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if user:
            await message.answer('Вы уже смешарик')
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