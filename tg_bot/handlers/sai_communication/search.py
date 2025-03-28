from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from core.spicy.objs import spicy_api
from db.database import async_session_factory

from db.models import UsersORM
from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.contrib.generator import generate_sai_bot_desc, exs_edit_search_bot_profile
from tg_bot.keyboards import fabrics, inline
from tg_bot.keyboards import reply
from logging import getLogger

logger = getLogger(__name__)
router = Router()


@router.message(F.text.lower().startswith('!поиск'))
async def search_bots(message: Message):
    '''Looking for bots in SpicyChat'''

    bot_name = message.text[7:]
    if not bot_name: bot_name = '*'

    search_res = await spicy_api.search_bots(bot_name)
    if not search_res:
        await message.answer(
            text=f'<code>{bot_name}</code>\nТаких ботов не существует'
        )

        logger.info(f'{search_bots.__name__} is handled: bot doesn`t found {UserForLogs.log_name(message)}, {bot_name=}')
        return

    search_res = search_res[0]

    await message.reply_photo(
        photo = search_res.avatar_url,
        caption = generate_sai_bot_desc(search_res),
        reply_markup=fabrics.pagination_ikb(bot_name, search_res.id, 1)
    )
    logger.info(f'{search_bots.__name__} is handled {UserForLogs.log_name(message)}, {bot_name=}')

@router.callback_query(fabrics.SearchListPagination.filter(F.action.in_(['prev','next'])))
async def search_pagination(callback: CallbackQuery, callback_data: fabrics.SearchListPagination):
    '''Shows the past or next bot and sends its profile'''

    if callback_data.action == 'next':
        page_num = callback_data.page + 1
    else:
        if callback_data.page == 1: return
        page_num = callback_data.page - 1


    await exs_edit_search_bot_profile(
        callback=callback,
        callback_data=callback_data,
        page_num=page_num,
        spicy_api=spicy_api,
    )
    logger.info(f'{search_pagination.__name__} is handled: {page_num=}, action={callback_data.action} {UserForLogs.log_name(callback.message)}')

@router.callback_query(fabrics.SearchSuggestBotCD.filter())
async def ask_to_con_chat_with_search_bot(callback: CallbackQuery, callback_data: fabrics.SearchSuggestBotCD):
    '''Asks the user whether to start a chat with the bot'''

    async with async_session_factory() as session:
        user = await session.get(UsersORM, callback.message.chat.id)

        if callback_data.char_id == user.char_id:
            await callback.message.answer('У Вас уже стоит бот с этим айди', reply_markup=reply.menu_rkb)

            logger.info(f'{ask_to_con_chat_with_search_bot.__name__} is handled: bot is already in use {UserForLogs.log_name(callback.message)}')
            return
        

        bot_profile = await spicy_api.get_bot_profile(callback_data.char_id)

        if not bot_profile:
            await callback.message.answer(f'Этого бота не существует', reply_markup=reply.menu_rkb)

            
            logger.info(f'{ask_to_con_chat_with_search_bot.__name__} is handled: bot doesn`t exist {UserForLogs.log_name(callback.message)}')
            return
        
        await callback.message.answer(text=bot_profile.greeting, reply_markup=inline.start_to_chat_ask_ikb(bot_profile=bot_profile))
    logger.info(f'{ask_to_con_chat_with_search_bot.__name__} is handled {UserForLogs.log_name(callback.message)}')