import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from logging import getLogger

from spicy_api.api import SpicyAPI
from core.spicy.classes.special_spicy_user import SpecialSpicyUser
from core.spicy.classes.special_spicy_api import SpecialSpicyAPI

import config

logger = getLogger(__name__)
router = Router()

spicy_api: SpicyAPI = None

async def botstart():
    '''Outdated
    Currently used tg_bot.handlers.sai_communication.sapiaccstart'''
    global spicy_api, spicy_user

    spicy_user = SpecialSpicyUser()
    await spicy_user.activate(config.SPICY_ACTIVE_USER_ID)
    spicy_api = SpecialSpicyAPI(spicy_user)