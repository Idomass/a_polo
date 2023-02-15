import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt


with open('all.json', encoding = "utf-8") as f:
	json_acceses = json.load(f)

	# breakpoint()
	contents = [access['english_content'] for access in json_acceses if access['english_content'] != None]
	subjects = [access['english_title'] for access in json_acceses if access['english_content'] != None]

	# print(contents)d

	vectorizer = TfidfVectorizer()

	fitness_scores = vectorizer.fit_transform(contents)
	print(fitness_scores)
	
	features = vectorizer.get_feature_names_out()
	# arr = np.empty(shape = [len(contents), len(features)])
	

	pca = PCA()
	x = pca.fit_transform(fitness_scores.toarray())

	print(pca)

	plt.scatter(x[:,0], x[:,1])
	plt.xlabel('PC1')
	plt.ylabel('PC2')
	plt.show()

	breakpoint()


	# for i in fitness_scores:
	# 	print()

	kmeans = KMeans(n_clusters=10, random_state=0, n_init="auto").fit(fitness_scores)

	print(kmeans.labels_)

	ordered = [[] for i in range(0,10)]

	for i,label in enumerate(kmeans.labels_):
		ordered[label].append(subjects[i])

	for cluster in ordered:
		print("Cluester" + str(cluster))
		print("\n")