

from bs4 import BeautifulSoup
import requests
import logging


# Parser constants
LOGGING_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=LOGGING_LEVELS["info"],
)

def get_html(url: str) -> str:
    """
    Get html text from url
    :param url: url
    :return: html text
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except (requests.RequestException, ValueError):
        logging.error("Network error")
        return ""


# vc.ru
def get_vc_insights(trend: str) -> list[dict]:
    """
    Get insights from vc.ru
    :param trend: trend
    :return: list of insights
    """
    insights = []
    html = get_html(f"https://vc.ru/search/v2/content/relevant?query={trend}")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        insights = []
        insights_html = soup.find("div", {'class':'search-feed'}).findChildren("div", {'class':'content-feed'}, recursive=False)
        logging.info(f"vc: {len(insights)} insights found.")
        for item in insights_html:
            insights.append(
                {
                    "source": "vc.ru",
                    "title": item.find("div", class_="content-title").text.replace("\n", "").strip(),
                    "url": item.find("a", class_="content-link").get("href"),
                    "summary": item.find("p").text.replace("\xa0", " ").replace("<mark>", " ").replace("</mark>", " ").strip(),
                }
            )
    return insights

# habr
def get_habr_insights(trend: str) -> list[dict]:
    """
    Get insights from habr
    :param trend: trend
    :return: list of insights
    """
    insights = []
    html = get_html(f"https://habr.com/ru/search/?target_type=posts&q={trend}&order=relevance")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        insights = []
        insights_html = soup.find("div", {'class':'tm-articles-list'}).findChildren("article", {'class':'tm-articles-list__item'}, recursive=False)
        logging.info(f"habr: {len(insights)} insights found.")
        for item in insights_html:
            title_elem = item.find("a", class_="tm-article-snippet__title-link")
            insights.append(
                {
                    "source": "habr.com",
                    "url": "https://habr.com/" + title_elem.get("href"),
                    "title": title_elem.text,
                    "summary": '', # habr is on lazyload
                }
            )
    return insights


# Get all insights
def get_insights(trend: str, limit_per_source: int = 0, overall_limit: int = 0) -> list[dict]:
    """
    Get insights from all sources
    :param trend: trend
    :return: list of insights
    """
    insights = []
    sources = [
        get_vc_insights,
        get_habr_insights,
    ]
    if limit_per_source == 0:
        limit_per_source = -1
    if overall_limit == 0:
        overall_limit = -1
    for source in sources:
        insights.extend(source(trend)[:limit_per_source])
    return insights[:overall_limit]


if __name__ == "__main__":
    print(get_insights("nft", limit_per_source=2, overall_limit=3))
