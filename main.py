import asyncio
import logging
from core.spicy.objs import botstart
from db.queries.orm import AsyncORM
import config

async def main():
    await AsyncORM.add_spicy_refresh_token(config.SPICY_ACTIVE_USER_ID, config.SPICY_CURRENT_REFRESH_TOKEN, config.SPICY_CLIENT_ID)
    await botstart(logs=config.SPICY_LOGS)

    from tg_bot import bot
    await bot.main()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename=".log",filemode="w", encoding='utf-8',
                        format="%(asctime)s %(levelname)s:%(name)s %(message)s")
    
    print('start')
    
    asyncio.run(main())
