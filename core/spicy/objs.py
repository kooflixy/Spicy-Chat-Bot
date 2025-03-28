from logging import getLogger

from spicy_api.api import SpicyAPI
from core.spicy.classes.special_spicy_user import SpecialSpicyUser
from core.spicy.classes.special_spicy_api import SpecialSpicyAPI

import config

logger = getLogger(__name__)

spicy_api: SpicyAPI = None

async def botstart(logs: bool = True):
    '''Activate SpicyAPI for all project'''
    global spicy_api, spicy_user

    spicy_user = SpecialSpicyUser(logs=logs)
    await spicy_user.activate(config.SPICY_ACTIVE_USER_ID)
    spicy_api = SpecialSpicyAPI(spicy_user, logs=logs)