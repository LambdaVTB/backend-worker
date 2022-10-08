import feedparser
from dateutil.parser import parse

SOURCES = {
    # Habr
    'habr': 'https://habr.com/ru/rss/all/all/?fl=ru',

    # Rubase
    ## By companies
    'rb_chance': "https://rb.ru/feeds/tag/chance/",
    # 'rb_vk': "https://rb.ru/feeds/tag/vk/",
    'rb_rvc': "https://rb.ru/feeds/tag/rvc/",
    'rb_yandex': "https://rb.ru/feeds/tag/yandex/",
    'rb_skolkovo': "https://rb.ru/feeds/tag/skolkovo/",
    # 'rb_facebook': "https://rb.ru/feeds/tag/facebook/",
    'rb_mailru': "https://rb.ru/feeds/tag/mailru/",
    # 'rb_microsoft': "https://rb.ru/feeds/tag/microsoft/",

    ## By topics
    'rb_advertising': "https://rb.ru/feeds/tag/advertising/",
    'rb_robotics': "https://rb.ru/feeds/tag/robotics/",
    'rb_it': "https://rb.ru/feeds/tag/it/",
    'rb_bigdata': "https://rb.ru/feeds/tag/bigdata/",
    'rb_china': "https://rb.ru/feeds/tag/china/",
    'rb_finance': "https://rb.ru/feeds/tag/fintech/",
    'rb_cloud': "https://rb.ru/feeds/tag/cloud/",

    # Vedomosti
    'vd_business': "https://www.vedomosti.ru/rss/rubric/business",
    'vd_it_business': "https://www.vedomosti.ru/rss/rubric/it_business",
    'vd_finance': "https://www.vedomosti.ru/rss/rubric/finance",
    'vd_opinion': "https://www.vedomosti.ru/rss/rubric/opinion",
    'vd_analytics': "https://www.vedomosti.ru/rss/rubric/opinion/analytics",


    # RT
    'rt': "https://russian.rt.com/rss/",
}

class RSSParser:
    def __init__(self, sources: dict[str,str]):
        self.sources = sources

    def fetch_entries(self) -> list[dict]:
        entries = []
        for source, url in self.sources.items():
            feed = feedparser.parse(url)
            for entry in feed['entries']:
                entry['source'] = source
                entries.append(entry)
        return entries

    def standardize_general(self, entry: dict) -> dict:
        """ Turns entry to a standardized format
        Args:
            entry (dict): entry from feedparser
        Returns:
            dict: standardized entry in a format:
        {
            'source': str,
            'title': str,
            'url':  str,
            'date': timestamp with zone,
            'tags': list[str],
            'text': str,
        }
        """
        return {
            'source': entry['source'],
            'title': entry['title'],
            'url':  entry['link'],
            'created_at': parse(entry['published']),
            'tags': [tag['term'] for tag in entry['tags']] if 'tags' in entry else [],
            'raw_text': entry['summary'] if 'summary' in entry else '',
        }

    def get_last_standardized_news(self) -> list[dict]:
        entries = self.fetch_entries()
        return [self.standardize_general(entry) for entry in entries]


if __name__ == '__main__':
    parser = RSSParser(SOURCES)
    print(parser.get_last_standardized_news())
