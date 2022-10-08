import asyncio
from db import add_new_news
from pytz import timezone
from datetime import datetime
from rss_parser import RSSParser, SOURCES

async def main():
    parser = RSSParser(SOURCES)
    news = parser.get_last_standardized_news()
    coroutines = [await add_new_news(
        el["title"], el["url"], el["raw_text"], el["tags"], el["created_at"] 
    ) for el in news]
    await session.commit()
    # await asyncio.gather(*coroutines)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
