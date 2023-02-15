import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import TruncatedSVD

with open('all.json', encoding = "utf-8") as f:
	json_acceses = json.load(f)

	contents = [access['description'] for access in json_acceses['results'] if access['description'] != None]


	# print(contents)d

	vectorizer = TfidfVectorizer()

	fitness_scores = vectorizer.fit_transform(contents)
	print(fitness_scores)
	
	features = vectorizer.get_feature_names_out()
	# arr = np.empty(shape = [len(contents), len(features)])
	

	# pca = TruncatedSVD(n_components=2)
	# pca.fit(fitness_scores)

	# breakpoint()

	# print(pca)

	# for i in fitness_scores:
	# 	print()

	kmeans = KMeans(n_clusters=6, random_state=0, n_init="auto").fit(X)




	
