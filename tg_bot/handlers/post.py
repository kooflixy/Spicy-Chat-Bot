from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
import config
from aiogram.fsm.state import StatesGroup, State
from db.database import async_session_factory
from db.models import UsersORM

from tg_bot.filters.is_admin import IsAdmin

router = Router()

class Post(StatesGroup):
    message = State()

@router.message(F.text.casefold().in_(['/post', '!пост']), IsAdmin(config.TG_ADMINS))
async def post(message:Message, state:FSMContext):
    await state.set_state(Post.message)
    await message.answer(text='Отправьте пост')

@router.message(Post.message, IsAdmin(config.TG_ADMINS))
async def send_post(message:Message, state:FSMContext):
    await state.clear()

    async with async_session_factory() as session:
        users = await session.execute(select(UsersORM.id))
        users = users.scalars().all()
    
    count = 0
    for user in users:
        try:
            await message.send_copy(chat_id=user)
            count+=1
        except: ...
    await message.answer(text=f'Пост был отправлен в {count} чатов')