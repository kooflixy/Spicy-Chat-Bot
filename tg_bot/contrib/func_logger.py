import time
from aiogram.types import Message
from logging import getLogger

logger = getLogger(__name__)

class UserForLogs:
    @staticmethod
    def log_name(msg: Message):
        info_list = []
        info_list.append(f'username="{msg.from_user.full_name}"')
        info_list.append(f'user_id="{msg.from_user.id}"')
        if msg.chat.type != 'private':
            info_list.append(f'{msg.chat.type}_name={msg.chat.title}')
            info_list.append(f'{msg.chat.type}_id={msg.chat.id}')
        return f'<TgUser {', '.join(info_list)}>'

# def msg_func_logger(logger):
def msg_func_logger(function):
    async def wrapped(*args, **kwargs):
        start_time = time.time()

        res = await function(*args, **kwargs)
        
        busy_time = time.time() - start_time
        logger.info(f'{function.__name__} completed in {busy_time} s for ')
        return res
    return wrapped
    # return log