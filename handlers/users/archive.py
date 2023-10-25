from loader import db

CHANNELS = []
ADMIN_S = [5397857416]


async def weekly_arxiv():
    await db.update_weekly(weekly=0,
                           data_id=1)


async def daily_arxiv():
    await db.update_day(days=0,
                        data_id=1)


async def monthly_arxiv():
    await db.update_monthly(monthly=0,
                            data_id=1)
