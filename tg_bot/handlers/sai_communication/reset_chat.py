from aiogram import F, Router
from aiogram.types import Message

from core.spicy.objs import spicy_api
from db.database import async_session_factory
from db.models import UsersORM

from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.keyboards import reply

from logging import getLogger

logger = getLogger(__name__)
router = Router()

@router.message(F.text.casefold().in_(['/reset_chat', 'обновить чат', '♻обновить чат']))
async def reset_chat(message: Message):
    '''Resets user's conv with bot'''
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)
        user_char_id = user.char_id
        
        bot_message, new_conv_id = await spicy_api.create_conversation('Привет!', user_char_id, message.from_user.full_name)

        await spicy_api.delete_conversation(user.conv_id)

        user.conv_id = new_conv_id
        await session.commit()
        
        await message.answer('<b>Чат успешно обновлён.</b>\n' + bot_message, reply_markup=reply.menu_rkb)

        logger.info(f'{reset_chat.__name__} is handled {UserForLogs.log_name(message)}: char_id={user_char_id}, {new_conv_id}')