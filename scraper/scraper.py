from typing import List
import requests
from json import dump, load, loads

API_KEY = "pub_172363ab3a9e0d9baad7f443feba04fc43dbc"
SCRAPE_URL_TEMPLATE = "https://newsdata.io/api/1/news?apikey={api_key}&language=he&domain={source}"


def scrape_source(source: str) -> bool:
    source_url = SCRAPE_URL_TEMPLATE.format(api_key=API_KEY, source=source)
    rsp = requests.get(source_url)
    if not rsp.ok:
        return False
    with open(f"scraping_data/{source}.json", 'w', encoding='utf-8') as scrape_data:
        dump(loads(rsp.text)['results'], scrape_data)
    return True


def scrape_all_sources() -> None:
    with open("sources.json") as sources:
        sources = load(sources).keys()
    for source in sources:
        if scrape_source(source):
            print(f"* Scraped {source}")
        else:
            print(f"* Error scraping {source}")

# Those functions are responsible to convert a news site url to arcticles

def map_article(url: str) -> List[str]:
    '''
    This function gets a url to a news site then returns a list of
    all the urls of articles currently in the sites.
    '''
    pass


def is_article(url: str) -> bool:
    '''
    This function checks if certain url contains an arcticle
    '''
    pass
