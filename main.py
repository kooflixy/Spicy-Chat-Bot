import asyncio
import logging
from tg_bot import bot

async def main():
    await bot.main()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename=".log",filemode="w", encoding='utf-8',
                        format="%(asctime)s %(levelname)s:%(name)s %(message)s")
    
    print('start')
    
    asyncio.run(main())
