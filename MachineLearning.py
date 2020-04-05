from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score


def clusterData(data):
    print('creating vectorizer')
    my_stop_words = text.ENGLISH_STOP_WORDS.union([])
    vectorizer = TfidfVectorizer(ngram_range=(2, 2), stop_words=my_stop_words)
# print(vectorizer.get_feature_names())
    print('fitting data')
    X = vectorizer.fit_transform(data)
    print('starting kmeans')
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    print(kmeans.labels_[34])


def TrainClassifier(data, labels, type):
    my_stop_words = text.ENGLISH_STOP_WORDS.union([])
    vectorizer = TfidfVectorizer(
        ngram_range=(2, 2), stop_words=my_stop_words)
    X = vectorizer.fit_transform(data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.20)
    # print(X_train)
    # print(y_train)

    if(type == "NB"):
        model = MultinomialNB(alpha=0, fit_prior=False).fit(
            X_train, y_train)
    elif(type == "SVM"):
        model = SVC().fit(X_train, y_train)
    elif(type == "KNN"):
        model = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)

    prediction = model.predict(
        X_test)
    print('###################################################')
    print(f'Metrics for {type} classifier')
    print(metrics.confusion_matrix(prediction, y_test))
    print(metrics.accuracy_score(prediction, y_test))
    print(metrics.classification_report(prediction, y_test))

    print('###################################################')
    #scores = cross_val_score(model, X, y, cv=5)
    return model, vectorizer


def Predict(model, data):

    Y = model[1].transform(data)

    predictedData = model[0].predict(Y)
    return predictedData
