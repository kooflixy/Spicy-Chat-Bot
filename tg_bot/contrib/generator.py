from datetime import datetime, timezone
from spicy_api.api.classes.bot_profile import SpicyBotProfile
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