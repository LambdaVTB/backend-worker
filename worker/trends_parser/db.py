from typing import Optional
from sqlalchemy import insert
from datetime import datetime
from worker.news_gatherer.db import common_tag_procedure
from migrations.connection.session import get_session
from migrations.models.news import News
from migrations.enums.news_types import NewsTypes



async def add_new_trend(
    title: str,
    summary: str,
    source: str, 
    created_at: datetime, 
    tags: list[str],
    id_raw: Optional[str] = None
) -> None:
    async for session in get_session():
        query = insert(News).values(
            title = title,
            summary = summary,
            news_type = NewsTypes.TREND,
            created_at = created_at,
            source = source,
            **({'original': id_raw} if id_raw else {})
        ).returning(News.id)
        id_news = (await session.execute(query)).scalars().first()
        await session.commit()
    await common_tag_procedure(tags, id_news)

