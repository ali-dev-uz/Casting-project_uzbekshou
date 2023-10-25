from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.users.archive import monthly_arxiv, daily_arxiv, weekly_arxiv
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    sched = AsyncIOScheduler()
    await db.create()
    # await db.drop_users()
    await db.create_table_users()
    await db.create_data_static()
    # Default commands (/star and /help)
    sched.add_job(monthly_arxiv, 'interval', days=30)
    sched.add_job(daily_arxiv, 'interval', days=1)
    sched.add_job(weekly_arxiv, 'interval', days=7)
    sched.start()
    await set_default_commands(dispatcher)

    # Notify the admin that the bot has started
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
