import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from tgbot.config import load_config
from tgbot.handlers.admin import admin_router
from tgbot.handlers.echo import echo_router
from tgbot.handlers.user import user_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.misc.refresh_rates import refresh_data
from tgbot.services import broadcaster
from tgbot.services.set_def_commands import set_default_commands



logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int], schedule: AsyncIOScheduler):
    await set_default_commands(bot)
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")
    schedule.start()

def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))
    

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    schedule = AsyncIOScheduler()
    
    schedule.add_job(refresh_data,trigger='interval', hours=1, timezone=utc)

    
    for router in [
        admin_router,
        user_router,
        echo_router
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config)
    await on_startup(bot, config.tg_bot.admin_ids, schedule)
    


    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
