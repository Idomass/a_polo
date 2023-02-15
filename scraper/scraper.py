from json import dump
from time import sleep

from newscatcherapi import NewsCatcherApiClient

API_KEY = "83RbYyEcVztqs2j75C04Mmu8IRNrANAaiX2SIpA9zxo"
ARTICLES_PER_PAGE = 100


class Scraper:
    def __init__(self):
        self.api = NewsCatcherApiClient(x_api_key=API_KEY)
        self.sources = None
        self._init_sources()

    def _init_sources(self):
        self.sources = self.api.get_sources(lang='he', countries='il', topic='news')['sources'][:30]

    def scrape_source(self, source: str):
        data = self.api.get_latest_headlines(lang='he', countries='il', topic='news', sources=source, page_size=100)[
            'articles']
        return data

    def save_all_sources(self):
        all_data = []
        for source in self.sources:
            try:
                all_data.extend(self.scrape_source(source))
            except Exception:
                print(f"* Problem scraping {source}")
            else:
                print(f"* Scraped {source}")
                sleep(1.1)

        with open("scraping_data/all.json", 'w') as json_file:
            dump(all_data, json_file)
