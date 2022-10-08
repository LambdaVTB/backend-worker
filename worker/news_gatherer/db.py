import asyncio
from datetime import datetime
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import sys
sys.path.insert(0, sys.path[0]+'/../..')

from migrations.models.news import News
from migrations.models.tags import Tags
from migrations.models.tags_news import TagsNews
from migrations.connection.session import get_session


async def add_tag(name: str):
    async for session in get_session():
        try:
            await session.execute(insert(Tags).values(name = name))
            await session.commit()
        except IntegrityError as e:
            pass

async def add_tags_news(name: str, id_news: str):
    async for session in get_session():
        try:
            await session.execute(insert(TagsNews).values(
                tag_id = select(Tags.id).where(
                    Tags.name == name
                ),
                news_id = id_news
            ))
            await session.commit()
        except IntegrityError as e:
            pass


async def add_new_news(
    title: str,
    url: str,
    raw_text: str,
    tags: list[str],
    created_at: datetime
):
    async for session in get_session():
        query = insert(News).values(
            raw_text = raw_text,
            url = url,
            title = title,
            created_at = created_at
        ).returning(News.id)
        id_news = (await session.execute(query)).scalars().first()
        await session.commit()
    async for session in get_session():
        coroutines = [await add_tag(el) for el in tags]
        # await asyncio.gather(*coroutines)
    async for session in get_session():
        coroutines = [await add_tags_news(el, id_news) for el in tags]
        # await asyncio.gather(*coroutines)
