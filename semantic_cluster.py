# semantic_cluster.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_anchors(anchor_list, k=5):
    texts = [a["expression"] for a in anchor_list]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)

    clusters = [[] for _ in range(k)]
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(anchor_list[idx])
    return clusters
