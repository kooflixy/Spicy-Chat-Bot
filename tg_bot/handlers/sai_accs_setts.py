from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from spicy_api.api import SpicyAPI
from core.spicy.classes.special_spicy_user import SpecialSpicyUser

import config

router = Router()

spicy_api: SpicyAPI = None

@router.message(Command('sapiaccstart'))
async def botstart(message: Message):
    global spicy_api, spicy_user

    spicy_user = SpecialSpicyUser()
    await spicy_user.activate(config.SPICY_ACTIVE_USER_ID)
    spicy_api = SpicyAPI(spicy_user)

    await message.answer('SpicyAPI activated')