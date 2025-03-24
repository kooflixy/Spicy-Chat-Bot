from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject

from core.spicy.objs import spicy_api
from db.database import async_session_factory
from db.models import UsersORM
from db.queries.orm import AsyncORM

from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.contrib.generator import generate_sai_bot_desc
from tg_bot.keyboards import inline
from tg_bot.keyboards import reply
from logging import getLogger

logger = getLogger(__name__)
router = Router()

@router.message(Command('setbot'))
async def setbot(message: Message, command: CommandObject):
    '''Changes user's sai_bot'''
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if command.args == user.char_id:
            await message.answer('У Вас уже стоит бот с этим айди', reply_markup=reply.menu_rkb)
            return
        

        bot_profile = await spicy_api.get_bot_profile(command.args)

        if not bot_profile:
            await message.answer(f'Бота с айди <code>{command.args}</code> не существует', reply_markup=reply.menu_rkb)
            logger.info(f'{setbot.__name__} is handled: bot doesn`t exist {UserForLogs.log_name(message)} char_id={command.args}')
            return
        
        await message.reply_photo(
            photo=bot_profile.avatar_url,
            caption=generate_sai_bot_desc(bot_profile)
        )
        await message.answer(text=bot_profile.greeting, reply_markup=inline.start_to_chat_ask_ikb(bot_profile=bot_profile))

        logger.info(f'{setbot.__name__} is handled: ask to change {UserForLogs.log_name(message)} char_id={command.args}')

@router.callback_query(inline.StartToChatAskCD.filter())
async def start_to_chat_resp(callback: CallbackQuery, callback_data: inline.StartToChatAskCD):
    async with async_session_factory() as session:
        user = await session.get(UsersORM, callback.message.chat.id)

        bot_message, new_conv_id = await spicy_api.create_conversation('Привет!', callback_data.char_id, callback.message.from_user.full_name)
        
        bot_profile = await spicy_api.get_bot_profile(callback_data.char_id)

        user.conv_id = new_conv_id
        user.char_id = callback_data.char_id
        await AsyncORM.add_conv_in_history(session, callback.message, callback_data.char_id, new_conv_id, bot_profile.name, spicy_api)

        await session.commit()

        await callback.message.answer(bot_message)

        logger.info(f'{start_to_chat_resp.__name__} is handled {UserForLogs.log_name(callback.message)}: char_id={callback_data.char_id}, {new_conv_id=}')