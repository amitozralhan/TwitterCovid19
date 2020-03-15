from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text


def clusterData(data):
    print('creating vectorizer')
    my_stop_words = text.ENGLISH_STOP_WORDS.union([])
    vectorizer = TfidfVectorizer(ngram_range=(2, 3), stop_words=my_stop_words)
# print(vectorizer.get_feature_names())
    print('fitting data')
    X = vectorizer.fit_transform(data)

# model = MultinomialNB().fit(
#     X, ['positive', 'negative', 'positive', 'negative'])
# print(model.predict(X))
    print('starting kmeans')
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    print(kmeans.labels_[34])
