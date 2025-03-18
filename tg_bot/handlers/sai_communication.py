from datetime import datetime, timezone
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject

from db.database import async_session_factory
from db.models import UsersORM, SpicyBotHistoryORM

from core.spicy.classes.special_spicy_user import SpecialSpicyUser
from core.spicy.classes.special_spicy_api import SpecialSpicyAPI
# from spicy_api.api.api import SpicyAPI
from db.queries.orm import AsyncORM
from tg_bot.contrib.func_logger import UserForLogs
from tg_bot.contrib.generator import get_random_smile, generate_sai_bot_desc
from tg_bot.keyboards import inline

import config
from logging import getLogger

logger = getLogger(__name__)
router = Router()


@router.message(Command('sapiaccstart'))
async def sapiaccstart(message: Message):
    '''Activates SpicyAPI in this file'''
    global spicy_api, spicy_user

    spicy_user = SpecialSpicyUser()
    await spicy_user.activate(config.SPICY_ACTIVE_USER_ID)
    spicy_api = SpecialSpicyAPI(spicy_user)

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
        
        bot_message, new_conv_id = await spicy_api.create_conversation('Привет!', config.SPICY_DEFAULT_AI_BOT_ID, message.from_user.full_name)

        user = UsersORM(
            id = message.chat.id,
            username = message.chat.full_name,
            char_id = config.SPICY_DEFAULT_AI_BOT_ID,
            conv_id = new_conv_id
        )

        session.add(user)
        await session.commit()

        await message.answer(bot_message)

        logger.info(f'{start.__name__} is handled {UserForLogs.log_name(message)}: {new_conv_id=}')


@router.message(F.text.casefold().in_(['/bot_profile', 'бот']))
async def bot_profile(message: Message):
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)
        
        bot_profile = await spicy_api.get_bot_profile(user.char_id, message.from_user.full_name)

        await message.reply_photo(
            photo=bot_profile.avatar_url,
            caption=generate_sai_bot_desc(bot_profile)
        )




@router.message(Command('setbot'))
async def setbot(message: Message, command: CommandObject):
    '''Changes user's sai_bot'''
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if command.args == user.char_id:
            await message.answer('У Вас уже стоит бот с этим айди')
            return
        

        bot_profile = await spicy_api.get_bot_profile(command.args, message.from_user.full_name)

        if not bot_profile:
            await message.answer(f'Бота с айди <code>{command.args}</code> не существует')
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
        
        bot_profile = await spicy_api.get_bot_profile(callback_data.char_id, callback.from_user.full_name)

        user.conv_id = new_conv_id
        user.char_id = callback_data.char_id
        await AsyncORM.add_conv_in_history(session, callback.message, callback_data.char_id, new_conv_id, bot_profile.name, spicy_api)

        await session.commit()

        await callback.message.answer(bot_message)

        logger.info(f'{start_to_chat_resp.__name__} is handled {UserForLogs.log_name(callback.message)}: char_id={callback_data.char_id}, {new_conv_id=}')





@router.message(F.text.casefold().in_(['/reset_chat', 'обновить чат']))
async def reset_chat(message: Message):
    '''Resets user's conv with bot'''
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)
        user_char_id = user.char_id
        
        bot_message, new_conv_id = await spicy_api.create_conversation('Привет!', user_char_id, message.from_user.full_name)

        await spicy_api.delete_conversation(user.conv_id)

        user.conv_id = new_conv_id
        await session.commit()
        
        await message.answer('<b>Чат успешно обновлён.</b>\n' + bot_message)

        logger.info(f'{reset_chat.__name__} is handled {UserForLogs.log_name(message)}: char_id={user_char_id}, {new_conv_id}')




@router.message(F.text.casefold().in_(['/history', 'история']))
async def history(message: Message):
    async with async_session_factory() as session:
        res = await AsyncORM.get_conv_history(session=session, message=message)

        await message.answer(
            text='Ваши чаты:',
            reply_markup=inline.show_spicy_bot_history(res)
        )

@router.callback_query(inline.SpicyBotHistoryListCD.filter())
async def ask_to_continue_chat_with_bot(callback: CallbackQuery, callback_data: inline.SpicyBotHistoryListCD):

    bot_profile = await spicy_api.get_bot_profile(callback_data.char_id, callback.message.from_user.full_name)

    await callback.message.reply_photo(
        photo=bot_profile.avatar_url,
        caption=generate_sai_bot_desc(bot_profile),
        reply_markup=inline.ask_to_continue_chat(callback_data.bot_history_id)
    )


@router.callback_query(inline.SpicyBotAskToContinueCD.filter())
async def continue_chat_with_bot(callback: CallbackQuery, callback_data: inline.SpicyBotAskToContinueCD):
    async with async_session_factory() as session:
        bot = await session.get(SpicyBotHistoryORM, callback_data.bot_id)
        user = await session.get(UsersORM, callback.message.chat.id)

        user.char_id = bot.char_id
        user.conv_id = bot.conv_id
        bot.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await session.commit()

        await callback.message.answer(f'Чат успешно изменен')


@router.message()
async def talk_with_sai_bot(message: Message):
    '''Sends users's message to SpicyChat and gets response message'''

    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if message.chat.type == 'private':
            bot_message = await spicy_api.send_message(message=message.text, char_id=user.char_id, conv_id=user.conv_id, username=message.from_user.full_name)

            await message.answer(bot_message)
        else:
            bot_message = await spicy_api.send_message(message=message.text, char_id=user.char_id, conv_id=user.conv_id, username=message.from_user.full_name)

            await message.reply(bot_message)
        
        logger.info(f'{talk_with_sai_bot.__name__} is handled {UserForLogs.log_name(message)}')
