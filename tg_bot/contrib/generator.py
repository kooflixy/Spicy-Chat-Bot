from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from tg_bot.keyboards import fabrics
from datetime import datetime, timezone
from spicy_api.api.classes.bot_profile import SpicyBotProfile
from spicy_api.api.classes.bot_profile import SpicyBotProfileSearchDTO
import random

EMOJI_LIST = ['😀', '😁', '😋', '😎', '😍', '😘', '😏', '😴', '🙃', '😝', 
              '🤑', '🤯', '🤪', '😵', '😇', '🤭', '🧐', '🤓', '👻', '😼', 
              '😻', '🍕', '🍔', '🍟', '🌭', '🍿', '🍧', '🍥', '🍰', '🍷', 
              '🧃', '🍊', '🍋', '🍌', '🍍', '🥭', '🍎', '🍄']

def get_random_smile():
    return random.choice(EMOJI_LIST)

def generate_sai_bot_desc(bot: SpicyBotProfile):
    return f'''
{get_random_smile()}<b>{bot.name}</b>
{bot.title}
<i>{', '.join(bot.tags)}</i>
'''

def generate_time_from_last_choose_for_botlist(date: datetime):
    now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
    dif = now - date

    if dif.days > 0:
        return f'{dif.days} дн.'
    
    hours = dif.seconds//3600
    if hours:
        if dif.seconds%3600 >= 1800:
            hours+=1
        return f'{hours} ч.'
    
    minutes = dif.seconds//60
    if minutes:
        if dif.seconds%60 >= 30:
            minutes+=1
        return f'{minutes} мин.'
    
    return f'{dif.seconds} с.'

async def edit_search_bot_profile(message: Message, bot: SpicyBotProfileSearchDTO, callback_data: fabrics.SearchListPagination, page_num: int):
    
    await message.edit_media(
        media = InputMediaPhoto(
            media = bot.avatar_url,
            caption = generate_sai_bot_desc(bot),
        ),
        reply_markup = fabrics.pagination_ikb(callback_data.name, bot.id, page_num)
    )

async def exs_edit_search_bot_profile(callback: CallbackQuery, callback_data: fabrics.SearchListPagination, page_num: int, spicy_api, try_: int = 0):
    if try_ == 5: return

    bot = await spicy_api.search_bots(callback_data.name, page = page_num)
    if not bot:
        await callback.answer('Ботов с таким именем больше нет')
        return
    bot = bot[0]
    try:
        await edit_search_bot_profile(callback.message, bot, callback_data, page_num)
    except TelegramBadRequest as ex:
        if ex.message == 'Bad Request: wrong type of the web page content':
            if callback_data.action == 'next': await exs_edit_search_bot_profile(callback, callback_data, page_num+1, spicy_api, try_=try_+1)
            else:
                if page_num == 1: return
                await exs_edit_search_bot_profile(callback.message, callback_data, page_num-1, spicy_api, try_=try_+1)