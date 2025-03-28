from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import config
from tg_bot.handlers import admin, bot_messages, post, sai_communication
from tg_bot.handlers import user_commands

async def main():
    bot = Bot(config.TG_BOT_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(
        user_commands.router,
        bot_messages.router,
        admin.router,
        post.router,

        sai_communication.set_bot.router,
        sai_communication.bot_pofile.router,
        sai_communication.history.router,
        sai_communication.search.router,
        sai_communication.reset_chat.router,
        sai_communication.talk.router #should always be at the end 
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)