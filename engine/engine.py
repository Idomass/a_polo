#! /usr/bin/env python3

import json
from googletrans import Translator


def translate_all_json():
    """
    Adds a field of the translation for each article in the all.json file
    """

    translater = Translator()

    with open('scraper/scraping_data/all.json', 'r', encoding='utf-8') as src_file:
        src_jsons = json.load(src_file)

    for article_json in src_jsons:
        article_json['english_content'] = translater.translate(article_json['content'], target='en').text
        article_json['english_title'] = translater.translate(article_json['title'], target='en').text
        article_json['english_description'] = translater.translate(article_json['description'], target='en').text

    with open('scraper/scraping_data/all.json', 'w', encoding='utf-8') as f:
        json.dump(src_jsons, f)


if __name__ == '__main__':
    translate_all_json()
