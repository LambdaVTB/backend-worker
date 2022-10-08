import asyncio
from datetime import datetime
from sqlalchemy import insert, select
import sys
sys.path.insert(0, sys.path[0]+'/../..')

from migrations.models.news import News
from migrations.models.tags import Tags
from migrations.models.tags_news import TagsNews
from migrations.connection.session import get_session

async def add_new_news(
    title: str,
    url: str,
    raw_text: str,
    tags: list[str],
    created_at: datetime
):
    def generate_tag_query(name: str):
        return insert(Tags).values(
            name = name
        )
    async for session in get_session():
        query = insert(News).values(
            raw_text = raw_text,
            url = url,
            title = title,
            created_at = created_at
        ).returning(News.id)
        id_news = (await session.execute(query)).scalars().first()
        coroutines = [session.execute(generate_tag_query(el)) for el in tags]
        await asyncio.gather(*coroutines)
        coroutines = [session.execute(insert(TagsNews).values(
            tag_id = select(Tags.id).where(
                Tags.name == el
            ),
            news_id = id_news
        )) for el in tags]
        await asyncio.gather(*coroutines)
        await session.commit()

