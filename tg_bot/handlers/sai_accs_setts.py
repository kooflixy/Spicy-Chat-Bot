from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from logging import getLogger

from spicy_api.api import SpicyAPI
from core.spicy.classes.special_spicy_user import SpecialSpicyUser

import config

logger = getLogger(__name__)
router = Router()

spicy_api: SpicyAPI = None

@router.message(Command('sapiaccstart'))

async def botstart(message: Message):
    '''Outdated
    Currently used tg_bot.handlers.sai_communication.sapiaccstart'''
    global spicy_api, spicy_user

    spicy_user = SpecialSpicyUser()
    await spicy_user.activate(config.SPICY_ACTIVE_USER_ID)
    spicy_api = SpicyAPI(spicy_user)

    await message.answer('SpicyAPI activated')