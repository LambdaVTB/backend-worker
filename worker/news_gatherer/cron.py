import asyncio
from db import add_new_news
from pytz import timezone
from datetime import datetime

async def main():
    await add_new_news(
        "Новость дня",
        "https://google.com",
        "Очень длинный текст новости будет здесь",
        ["Генеральный директор",],
        datetime.now(timezone("UTC"))
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
