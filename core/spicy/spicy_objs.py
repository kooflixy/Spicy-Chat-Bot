import asyncio
from spicy_api import SpicyAPI
from core.spicy.classes.special_spicy_user import SpecialSpicyUser
import config

async def activate_spicy():
    global user, spicy_api

    user = SpecialSpicyUser()
    await user.activate(config.SPICY_ACTIVE_USER_ID)
    spicy_api = SpicyAPI(user)

asyncio.run(activate_spicy())