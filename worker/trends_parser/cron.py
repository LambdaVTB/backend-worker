import asyncio

import sys
sys.path.insert(0, sys.path[0]+'/../..')

from pytz import timezone
from datetime import datetime
from worker.configs.get_settings import get_postgres_settings
from worker.news_gatherer.graph import Graph
from worker.trends_parser.db import add_new_trend 

async def main():
    await Graph.connect_db()
    await add_new_trend(
        "Короткий",
        "Длинный текст",
        "vc.ru", 
        datetime.now(timezone("UTC")), 
        ["a",]
    ) 
    await Graph.disconnect_db()
    # await asyncio.gather(*coroutines)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
