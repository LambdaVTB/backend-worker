import asyncio

import sys
sys.path.insert(0, sys.path[0]+'/../..')

from db import add_new_news
from pytz import timezone
from datetime import datetime
from rss_parser import RSSParser, SOURCES
from worker.configs.get_settings import get_postgres_settings
from worker.news_gatherer.graph import Graph

async def main():
    await Graph.connect_db()
    parser = RSSParser(SOURCES)
    news = parser.get_last_standardized_news()
    if get_postgres_settings().DEBUG:
        news = news[:50]
    coroutines = [await add_new_news(
        el["title"], el["url"], el["raw_text"], el["tags"], el["created_at"] 
    ) for el in news]
    await Graph.disconnect_db()
    # await asyncio.gather(*coroutines)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
