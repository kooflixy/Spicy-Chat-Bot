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