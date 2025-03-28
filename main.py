import asyncio
import logging
from core.spicy.objs import botstart
import config

async def main():
    await botstart(logs=config.SPICY_LOGS)

    from tg_bot import bot
    await bot.main()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename=".log",filemode="w", encoding='utf-8',
                        format="%(asctime)s %(levelname)s:%(name)s %(message)s")
    
    print('start')
    
    asyncio.run(main())
