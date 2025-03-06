from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import config
from tg_bot.handlers import sai_communication, sai_accs_setts

async def main():
    bot = Bot(config.TG_BOT_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(
        sai_accs_setts.router,
        sai_communication.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)