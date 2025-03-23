from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from core.spicy.objs import spicy_api
from db.database import async_session_factory

from db.models import UsersORM
from tg_bot.contrib.generator import generate_sai_bot_desc, exs_edit_search_bot_profile
from tg_bot.keyboards import fabrics, inline
from tg_bot.keyboards import reply
from logging import getLogger

logger = getLogger(__name__)
router = Router()


@router.message(F.text.lower().startswith('!поиск'))
async def search_bots(message: Message):
    bot_name = message.text[7:]
    if not bot_name: return

    search_res = (await spicy_api.search_bots(bot_name))[0]

    await message.reply_photo(
        photo = search_res.avatar_url,
        caption = generate_sai_bot_desc(search_res),
        reply_markup=fabrics.pagination_ikb(bot_name, search_res.id, 1)
    )

@router.callback_query(fabrics.SearchListPagination.filter(F.action.in_(['prev','next'])))
async def search_pagination(callback: CallbackQuery, callback_data: fabrics.SearchListPagination):
    if callback_data.action == 'next':
        page_num = callback_data.page + 1
    else:
        if callback_data.page == 1: return
        page_num = callback_data.page - 1


    await exs_edit_search_bot_profile(
        message=callback.message,
        callback_data=callback_data,
        page_num=page_num,
        spicy_api=spicy_api,
    )

@router.callback_query(fabrics.SearchSuggestBotCD.filter())
async def ask_to_con_chat_with_search_bot(callback: CallbackQuery, callback_data: fabrics.SearchSuggestBotCD):
    async with async_session_factory() as session:
        user = await session.get(UsersORM, callback.message.chat.id)

        if callback_data.char_id == user.char_id:
            await callback.message.answer('У Вас уже стоит бот с этим айди', reply_markup=reply.menu_rkb)
            return
        

        bot_profile = await spicy_api.get_bot_profile(callback_data.char_id, callback.message.from_user.full_name)

        if not bot_profile:
            await callback.message.answer(f'Этого бота не существует', reply_markup=reply.menu_rkb)
            return
        
        await callback.message.answer(text=bot_profile.greeting, reply_markup=inline.start_to_chat_ask_ikb(bot_profile=bot_profile))