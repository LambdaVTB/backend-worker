import neo4j

import asyncio
from datetime import datetime
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from worker.news_gatherer.graph import Graph

from migrations.models.news import News
from migrations.models.tags import Tags
from migrations.models.tags_news import TagsNews
from migrations.models.raw import Raw
from migrations.connection.session import get_session
from migrations.enums.news_types import NewsTypes


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

async def common_tag_procedure(tags: list[str], id_news: str):
    async for session in get_session():
        coroutines = [await add_tag(el) for el in tags]
        # await asyncio.gather(*coroutines)
    async for session in get_session():
        coroutines = [await add_tags_news(el, id_news) for el in tags]
        # await asyncio.gather(*coroutines)

    cypher = """create (i: Item{identifier: $identifier})"""
    try:
        await Graph.write(cypher, identifier=str(id_news))
    except neo4j.exceptions.ConstraintError as e:
        raise BadRequest('News is already exists', e)


async def add_new_news(
    title: str,
    url: str,
    raw_text: str,
    tags: list[str],
    created_at: datetime
):
    async for session in get_session():
        query = insert(Raw).values(
            text = raw_text,
            url = url,
            created_at = created_at
        ).returning(Raw.id)
        id_raw = (await session.execute(query)).scalars().first()
        await session.commit()
    async for session in get_session():
        query = insert(News).values(
            title = title,
            news_type = NewsTypes.DIGEST,
            created_at = created_at,
            original = str(id_raw)
        ).returning(News.id)
        id_news = (await session.execute(query)).scalars().first()
        await session.commit()
    await common_tag_procedure(tags, id_news) 
