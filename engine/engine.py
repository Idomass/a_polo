#! /usr/bin/env python3

import json

import numpy as np
import pandas as pd
# from googletrans import Translator
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy.sparse.csgraph import connected_components
import boto3

SIMILAR_MIN = 4
MIN_ARTICLES = 4


def cluster_matching_articles():
    stop_words = stopwords.words('english')

    def clean_sentence(sentence):
        return [ps.stem(w) for w in wordpunct_tokenize(sentence) if w.lower() not in stop_words and w.isalnum()]

    ps = PorterStemmer()
    pdf = pd.read_json("scraping_temp_data/translated.json")
    pdf['cleaned_title'] = pdf['english_title'].apply(clean_sentence)
    cleaned_titles = pdf['cleaned_title'].to_list()

    output_matrix = np.empty((len(pdf), len(pdf)))
    for i in range(len(pdf)):
        for j in range(len(pdf)):
            if i == j:
                output_matrix[i][j] = np.nan
                continue
            similarity = len(set(cleaned_titles[i]).intersection(set(cleaned_titles[j])))
            if similarity < SIMILAR_MIN:
                output_matrix[i][j] = np.nan
                continue
            output_matrix[i][j] = True

    adj_matrix = pd.DataFrame(output_matrix).fillna(0)
    pdf['labels'] = connected_components(adj_matrix.to_numpy())[1]

    def to_article(row):
        return {
            'title': row['title'],
            'date': row['published_date'],
            'link': row['link'],
            'stie': row['clean_url'].split('.')[0]
        }

    pdf['article'] = pdf.apply(to_article, axis=1)

    out_json = pdf[['article', 'labels', 'clean_url']].groupby('labels').agg(
        article=('article', list),
        label_count=('labels', 'count'),
    )

    with open("processed_data.json", 'w') as json_file:
        json_file.write(out_json[out_json['label_count'] >= MIN_ARTICLES]['article'].to_json())


def upload_to_s3():
    client = boto3.client(
        's3',
        aws_access_key_id="AKIAR2UW27JUQOBJX7M6",
        aws_secret_access_key="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",
    )

    with open("processed_data.json", 'rb') as json_file:
        client.put_object(Bucket="hakaton-stereotip", Key="processed_data.json", Body=json_file)


def translate_all_json():
    """
    Adds a field of the translation for each article in the all.json file
    """

    translater = Translator()

    with open('../scraper/scraping_data/all.json', 'r', encoding='utf-8') as src_file:
        src_jsons = json.load(src_file)

    for article_json in src_jsons:
        article_json['english_content'] = translater.translate(article_json['content'], target='en').text
        article_json['english_title'] = translater.translate(article_json['title'], target='en').text
        article_json['english_description'] = translater.translate(article_json['description'], target='en').text

    with open('scraping_temp_data/translated.json', 'w', encoding='utf-8') as f:
        json.dump(src_jsons, f)


if __name__ == '__main__':
    translate_all_json()
