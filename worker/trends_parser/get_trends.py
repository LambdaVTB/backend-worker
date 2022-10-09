

import sys
sys.path.insert(0, sys.path[0]+'/../..')


import pandas as pd
from ner_parser import NERParser
from worker.news_gatherer.rss_parser import RSSParser, SOURCES
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)

class Lemmatizer:
    def __init__(self) -> None:
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)


    def lemmatize(self, text: str) -> list[str]:
        """ Lemmatizes a text
        Args:
            text (str): text to lemmatize
        Returns:
            list[str]: list of lemmas
        """
        # Use this function with pandarallel's parallel_apply
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)
        return [_.lemma for _ in doc.tokens]


def make_lemmatize(lemmatizer: Lemmatizer):
    def lemmatize_word(word: str) -> str:
        # Название в два слова должно остаться названием в два слова
        if len(word.split(' ')) > 1:
            return ' '.join([ lemmatizer.lemmatize(word)[0] for word in word.split(' ') ])
        else:
            return lemmatizer.lemmatize(word)[0]

    return lemmatize_word



# def get_trends(news_: pd.DataFrame, ner: NERParser, lemmatizer: Lemmatizer) -> pd.DataFrame:
def get_trends(news_: list[dict[str,str]], ner: NERParser, lemmatizer: Lemmatizer, convert_to_df: bool = True) -> list[dict[str, int]]:
    """ Get trends from news"""
    news = news_.copy()
    if convert_to_df:
        news = sorted(news, key=lambda x: x['created_at'], reverse=True)
        news = pd.DataFrame(news)
    # 1. Get NERs and nouns
        news = pd.DataFrame(news)
    news['ners'] = news['raw_text'].apply(ner.get_ners_dict)

    # 2. Split extracted words
    for ner_type in ['ORGs', 'PERs', 'LOCs', 'NOUs']:
        news[ner_type] = news['ners'].apply(lambda x: x[ner_type])

    # 3. Lemmatize extracted words
    lemmatize_word = make_lemmatize(lemmatizer)
    for ner_type in ['ORGs', 'PERs', 'LOCs', 'NOUs']:
        news[ner_type] = news[ner_type].apply(lambda x: [lemmatize_word(word) for word in x])

    # 4. Get trends
    trends = []

    for ner_type in ['ORGs', 'PERs', 'LOCs', 'NOUs']:
        trends.append(
            news[ner_type].explode().value_counts().to_dict()
        )

    return trends


def get_trends_by_tag(news_: list[dict[str,str]], tags:list[str],  ner: NERParser, lemmatizer: Lemmatizer):
    """ Get trends from news"""
    news = news_.copy()
    news = sorted(news, key=lambda x: x['created_at'], reverse=True)
    news = pd.DataFrame(news)

    # 0. Filter by tags
    news = news[news['tags'].apply(lambda x: len(set(x) & set(tags)) > 0)]

    # 1. Pass df to get_trends
    return get_trends(news, ner, lemmatizer, convert_to_df=False)


if __name__ == '__main__':
    # Load models
    parser = RSSParser(SOURCES)
    lemmatizer = Lemmatizer()
    ner = NERParser(
        r"./worker/trends_parser/navec_news_v1_1B_250K_300d_100q.tar",
        r"./worker/trends_parser/slovnet_ner_news_v1.tar",
    )
    news = []
    news = parser.get_last_standardized_news()
    # Pls reference TIS_defining_whats_in_trend.ipynb ending for better understanding
    trends = get_trends(news, ner, lemmatizer)

    # Get trends by tags
    gen_tags = ['Финансы', 'Экономика', 'Маркетинг', 'PR', 'HR',  'Компании', 'Рынки', 'Бизнес', 'Технологии', 'Автоматизация', 'Мобилизация',  'Работодателю', 'Кредитование', 'Инвестиции', 'Санкции 2022',  'Общее', 'Карьера',  'Экономика России', 'IT-компании',  'Налоги, взносы, пошлины',  'Мошенничество', 'Экономические преступления']
    buh_tags = ['Финансы', 'Экономика',  'Криптовалюты', 'Учет и налогообложение', 'Бизнес', 'Бухгалтеру',  'Вебинары для бухгалтеров', 'Банкротство', 'Кредитование', 'Банки',  'Трудовое право', 'Экономика России',  'Электронные трудовые книжки', 'ЕГАИС', 'Налоги, взносы, пошлины', 'ЭДО', 'НДФЛ', 'АУСН', 'Перевозка', 'Отчетность в ПФР', 'Мошенничество', 'Первичные документы', 'Экономические преступления', 'ПСН', 'Онлайн-кассы']

    # get trends by tags
    gen_trends = get_trends_by_tag(news, gen_tags, ner, lemmatizer)
    buh_trends = get_trends_by_tag(news, buh_tags, ner, lemmatizer)

    # print
    print('Director trends')
    print(gen_trends)
    print('Buhgalter trends')
    print(buh_trends)
    print('General trends')
    print(trends)
