from aiogram import Router
from aiogram.types import Message

from core.spicy.objs import spicy_api
from db.database import async_session_factory
from db.models import UsersORM

from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.contrib.active_chat_sesses_checker import active_chats_sesses_checker

from logging import getLogger

logger = getLogger(__name__)
router = Router()


@router.message()
async def talk_with_sai_bot(message: Message):
    '''Sends users's message to SpicyChat and gets response message'''
    if active_chats_sesses_checker.check(message.chat.id): return

    try:
        async with async_session_factory() as session:
            active_chats_sesses_checker.add(message.chat.id)

            user = await session.get(UsersORM, message.chat.id)

            if message.chat.type == 'private':
                bot_message = await spicy_api.send_message(message=message.text, char_id=user.char_id, conv_id=user.conv_id, username=message.from_user.full_name)
                
                await message.answer(bot_message)
            else:
                bot_message = await spicy_api.send_message(message=message.text, char_id=user.char_id, conv_id=user.conv_id, username=message.from_user.full_name)

                await message.reply(bot_message)
            
            active_chats_sesses_checker.remove(message.chat.id)
            logger.info(f'{talk_with_sai_bot.__name__} is handled {UserForLogs.log_name(message)}')
    except Exception as ex:
        active_chats_sesses_checker.remove(message.chat.id)
        logger.info(f'{talk_with_sai_bot.__name__} is handled {UserForLogs.log_name(message)}: error {ex}')
