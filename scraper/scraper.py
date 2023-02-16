from json import dump
from time import sleep

from newscatcherapi import NewsCatcherApiClient

API_KEY = "83RbYyEcVztqs2j75C04Mmu8IRNrANAaiX2SIpA9zxo"
ARTICLES_PER_PAGE = 100
BASE_CONFIG = dict(lang='he', countries='il', topic='news')


class Scraper:
    def __init__(self):
        self.api = NewsCatcherApiClient(x_api_key=API_KEY)
        self.sources = None
        self._init_sources()

    def _init_sources(self):

        # Limited to 30 sources since the free plan is limited to 50 requests.
        self.sources = self.api.get_sources(**BASE_CONFIG)['sources'][:30]

    def scrape_source(self, source: str):
        response = self.api.get_latest_headlines(**BASE_CONFIG, sources=source, page_size=100)
        return response['articles']

    def save_all_sources(self):
        all_articles = []

        # Getting top 100 articles from every source instead of top 3000 of all articles.
        for source in self.sources:
            try:
                all_articles.extend(self.scrape_source(source))
            except Exception:
                print(f"* Problem scraping {source}")
            else:
                print(f"* Scraped {source}")

                # Free plan is limited to 1 call/second.
                sleep(1.1)

        with open("scraping_data/all.json", 'w') as json_file:
            dump(all_articles, json_file)


if __name__ == '__main__':
    s = Scraper()
    s.save_all_sources()
