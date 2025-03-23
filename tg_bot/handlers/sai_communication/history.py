from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from core.spicy.objs import spicy_api
from db.database import async_session_factory
from db.models import UsersORM, SpicyBotHistoryORM
from db.queries.orm import AsyncORM

from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.contrib.generator import generate_sai_bot_desc
from tg_bot.keyboards import inline
from tg_bot.keyboards import reply

from datetime import datetime, timezone
from logging import getLogger

logger = getLogger(__name__)
router = Router()



@router.message(F.text.casefold().in_(['/history', 'история', '📃история']))
async def history(message: Message):
    '''Show users's bot history'''
    async with async_session_factory() as session:
        res = await AsyncORM.get_conv_history(session=session, message=message)

        await message.answer(
            text='Ваши чаты:',
            reply_markup=inline.show_spicy_bot_history(res)
        )

        logger.info(f'{history.__name__} is handled {UserForLogs.log_name(message)}')

@router.callback_query(inline.SpicyBotHistoryListCD.filter())
async def ask_to_continue_chat_with_bot(callback: CallbackQuery, callback_data: inline.SpicyBotHistoryListCD):
    '''Asks the user whether to change the active chat'''
    bot_profile = await spicy_api.get_bot_profile(callback_data.char_id, callback.message.from_user.full_name)

    await callback.message.reply_photo(
        photo=bot_profile.avatar_url,
        caption=generate_sai_bot_desc(bot_profile),
        reply_markup=inline.ask_to_continue_chat(callback_data.bot_history_id)
    )

@router.callback_query(inline.SpicyBotAskToContinueCD.filter())
async def continue_chat_with_bot(callback: CallbackQuery, callback_data: inline.SpicyBotAskToContinueCD):
    '''Changes the user's active chat'''
    async with async_session_factory() as session:
        bot = await session.get(SpicyBotHistoryORM, callback_data.bot_id)
        user = await session.get(UsersORM, callback.message.chat.id)

        user.char_id = bot.char_id
        user.conv_id = bot.conv_id
        bot.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await session.commit()

        await callback.message.answer(f'Чат успешно изменен', reply_markup=reply.menu_rkb)