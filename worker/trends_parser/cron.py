import asyncio

import sys
sys.path.insert(0, sys.path[0]+'/../..')

from pytz import timezone
from datetime import datetime
from worker.configs.get_settings import get_postgres_settings
from worker.news_gatherer.graph import Graph
from worker.trends_parser.db import add_new_trend, get_all_unprocessed 
from worker.trends_parser.get_trends import Lemmatizer, NERParser, get_trends

async def main():
    await Graph.connect_db()
    news = await get_all_unprocessed()
    lemmatizer = Lemmatizer()
    ner = NERParser(
        r"worker/trends_parser/navec_news_v1_1B_250K_300d_100q.tar",
        r"worker/trends_parser/slovnet_ner_news_v1.tar",
    )
    print(news)
    news = [{**el.__dict__, **{'raw_text': el.text}} for el in news]
    trends = get_trends(news, ner, lemmatizer)
    # gen_tags = ['Финансы', 'Экономика', 'Маркетинг', 'PR', 'HR',  'Компании', 'Рынки', 'Бизнес', 'Технологии', 'Автоматизация', 'Мобилизация',  'Работодателю', 'Кредитование', 'Инвестиции', 'Санкции 2022',  'Общее', 'Карьера',  'Экономика России', 'IT-компании',  'Налоги, взносы, пошлины',  'Мошенничество', 'Экономические преступления']
    # buh_tags = ['Финансы', 'Экономика',  'Криптовалюты', 'Учет и налогообложение', 'Бизнес', 'Бухгалтеру',  'Вебинары для бухгалтеров', 'Банкротство', 'Кредитование', 'Банки',  'Трудовое право', 'Экономика России',  'Электронные трудовые книжки', 'ЕГАИС', 'Налоги, взносы, пошлины', 'ЭДО', 'НДФЛ', 'АУСН', 'Перевозка', 'Отчетность в ПФР', 'Мошенничество', 'Первичные документы', 'Экономические преступления', 'ПСН', 'Онлайн-кассы']

    # get trends by tags
    # gen_trends = get_trends_by_tag(news, gen_tags, ner, lemmatizer)
    # buh_trends = get_trends_by_tag(news, buh_tags, ner, lemmatizer)

    for trend in trends:
        [await add_new_trend(
            el[0],
            str(el[1]),
            "", 
            datetime.now(timezone("UTC")), 
            [],
        ) for el in trend.items()]  
    await Graph.disconnect_db()
    # await asyncio.gather(*coroutines)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
