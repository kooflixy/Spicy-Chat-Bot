from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject

from db.database import async_session_factory
from db.models import UsersORM

from core.spicy.classes.special_spicy_user import SpecialSpicyUser
from core.spicy.classes.special_spicy_api import SpecialSpicyAPI
# from spicy_api.api.api import SpicyAPI
from tg_bot.contrib.func_logger import UserForLogs
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


@router.message(Command('bot_profile'))
async def bot_profile(message: Message):
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)
        
        bot_profile = await spicy_api.get_bot_profile(user.char_id)

        await message.reply_photo(
            photo=bot_profile.avatar_url,
            caption=f'''
<b>{bot_profile.name}</b>
{bot_profile.title}
{', '.join(bot_profile.tags)}
'''
        )


@router.message(Command('setbot'))
async def setbot(message: Message, command: CommandObject):
    '''Changes user's sai_bot'''
    async with async_session_factory() as session:
        user = await session.get(UsersORM, message.chat.id)

        if command.args == user.char_id:
            await message.answer('У Вас уже стоит бот с этим айди')
            return
        

        bot_profile = await spicy_api.get_bot_profile(command.args)

        if not bot_profile:
            await message.answer(f'Бота с айди <code>{command.args}</code> не существует')
            logger.info(f'{setbot.__name__} is handled: bot doesn`t exist {UserForLogs.log_name(message)} char_id={command.args}')
            return
        
        await message.reply_photo(
            photo=bot_profile.avatar_url,
            caption=f'''
<b>{bot_profile.name}</b>
{bot_profile.title}
{', '.join(bot_profile.tags)}
''',
            reply_markup=inline.start_to_chat_ask_ikb(bot_profile=bot_profile)
        )
        return
        response = await spicy_api.create_conversation('Привет!', command.args)

        if not response:
            await message.answer(f'Бота с айди <code>{command.args}</code> не существует')
            logger.info(f'{setbot.__name__} is handled: bot doesn`t exist {UserForLogs.log_name(message)} char_id={command.args}')
            return
        
        await spicy_api.delete_conversation(user.conv_id)

        bot_message, new_conv_id = response

        user.conv_id = new_conv_id
        user.char_id = command.args
        await session.commit()

        await message.answer('<b>Бот успешно изменён.</b>\n' + bot_message)

        logger.info(f'{setbot.__name__} is handled {UserForLogs.log_name(message)}: char_id={command.args}, {new_conv_id}')


@router.callback_query(inline.StartToChatAskCD.filter())
async def start_to_chat_resp(callback: CallbackQuery, callback_data: inline.StartToChatAskCD):
    async with async_session_factory() as session:
        user = await session.get(UsersORM, callback.message.chat.id)

        bot_message, new_conv_id = await spicy_api.create_conversation('Привет!', callback_data.char_id, callback.message.from_user.full_name)

        await spicy_api.delete_conversation(user.conv_id)

        user.conv_id = new_conv_id
        user.char_id = callback_data.char_id
        await session.commit()

        await callback.message.answer(bot_message)

        logger.info(f'{start.__name__} is handled {UserForLogs.log_name(callback.message)}: {new_conv_id=}')


@router.message(Command('reset_chat'))
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
