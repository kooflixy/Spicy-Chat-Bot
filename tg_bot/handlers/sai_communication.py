from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject

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


@router.message(Command('setbot'))
async def setbot(message: Message, command: CommandObject):
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if command.args == user.char_id:
            await message.answer('У Вас стоит бот с этим айди')
            return
        
        response = await spicy_api.create_conversation('Привет!', command.args)

        if not response:
            await message.answer(f'Бота с айди <code>{command.args}</code> не существует')
            logger.info(f'{setbot.__name__} is handled: bot doesn`t exist {UserForLogs.log_name(message)} char_id={command.args}')
            return
        
        bot_message, new_conv_id = response

        user.char_id = new_conv_id
        await session.commit()

        await message.answer('<b>Бот успешно изменён.</b>\n' + bot_message)

        logger.info(f'{setbot.__name__} is handled {UserForLogs.log_name(message)}: char_id={command.args}, {new_conv_id}')


@router.message()
async def talk_with_sai_bot(message: Message):
    '''Sends users's message to SpicyChat and gets response message'''

    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)
        user = user.as_dto()

        if message.chat.type == 'private':
            bot_message = await spicy_api.send_message(message=message.text, char_id=user.char_id, conv_id=user.conv_id)

            await message.answer(bot_message)
        else:
            bot_message = await spicy_api.send_message(message=message.text, char_id=user.char_id, conv_id=user.conv_id)

            await message.reply(bot_message)
        
        logger.info(f'{talk_with_sai_bot.__name__} is handled {UserForLogs.log_name(message)}')
