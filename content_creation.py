import string
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import getopt, sys
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
from scipy.spatial.distance import cdist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


#####################################################################
######################## Auxilary Functions #########################
#####################################################################

def process_text(text):

    ##REMOVE PUNCTUATION
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)

    ##LOWERCASE
    text = text.lower()

    ##TOKENIZE
    tokens = word_tokenize(text)

    ##STEM
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]

    return tokens

def plot_optimal_k(texts):
    ##CREATE TERM -DOCUMENT MATRIX
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 lowercase=True)
    tdm = vectorizer.fit_transform(texts)

    ##CALCULATE AVERAGE DISTANCE TO CLUSTER
    avg_distance_to_cluster = []
    k_values = range(1, tdm.shape[0] - 1, 10)
    for k in k_values:
        print(str(k) + " of " + str(tdm.shape[0] - 1))
        kmeanModel = KMeans(n_clusters = k ).fit(tdm)
        kmeanModel.fit(tdm)
        avg_distance_to_cluster.append(sum(np.min(cdist(tdm.toarray(), kmeanModel.cluster_centers_, 'euclidean'), axis=1))/tdm.shape[0])

    ##PLOT RESULTS
    plt.plot(k_values, avg_distance_to_cluster, 'bx-')
    plt.xlabel('K')
    plt.ylabel('Average Distance to Cluster')
    plt.title('Elbow Method Showing Optimal K')
    plt.show()

def cluster_texts(texts, clusters=None):

    ##CREATE TERM -DOCUMENT MATRIX
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 lowercase=True)
    tdm = vectorizer.fit_transform(texts)


    ##DETERMINE CLUSTER COUNT
    if clusters is None:
        clusters = int((tdm.shape[0] * tdm.shape[1])/tdm.count_nonzero())

    ##PERFORM KMEANS
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tdm)

    ##CREATE RETURN VALUE
    clustering = collections.defaultdict(list)
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)

    return clustering

def sentiment_analysis(text):
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(text)
    return score

def print_topics(model, vectorizer, top_n=10):
    for idx, topic in enumerate(model.components_):
        print("Topic %d:" % (idx))
        print([(vectorizer.get_feature_names()[i], topic[i])for i in topic.argsort()[:-top_n - 1:-1]])





########################################################################
##Problem 1:  Identify topics trending with news outlets and bloggers ##
########################################################################
def bloggersTrendingTopics():

    ##GET DATA
    data = pd.read_csv("./data/blogData.csv", encoding='latin-1')
    text = data["Article"]

    ##CLUSTER TEXT
    num_of_clusters = None
    clusters = cluster_texts(text, num_of_clusters)


    ##FILTER FOR CLUSTER GROUPS
    clusters_new = []
    for cluster_index in range(0, len(clusters)):
        if(len(clusters[cluster_index]) > 1):
            clusters_new.append(clusters[cluster_index])
    clusters = clusters_new

    ##FILTER FOR VARIOUS SITES
    clusters_new = []
    for cluster_index in range(0, len(clusters)):
        if (not all(data.Source[j].strip() == data.Source[clusters[cluster_index][0]].strip() for j in clusters[cluster_index])):
            clusters_new.append(clusters[cluster_index])
    clusters = clusters_new


    ##GET TOPICS FOR CLUSTERS
    cluster_articles = []
    for cluster_index in range(0, len(clusters)):
        cluster_articles.append([data.Article[i] for i in clusters[cluster_index]])

    NUM_TOPICS = 1
    cluster_topics = []
    for d in cluster_articles:
        article_text = d
        vectorizer = CountVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 lowercase=True)
        data_vectorized = vectorizer.fit_transform(article_text)  ##OUTPUT NOT USED, BUT VECTORIZER NEEDS TO FIT DATA

        ##BUILD LDA
        lda_model = LatentDirichletAllocation(n_components=NUM_TOPICS, max_iter=20, learning_method='online')
        lda_Z = lda_model.fit_transform(data_vectorized)  ##OUTPUT NOT USED, BUT VECTORIZER NEEDS TO FIT DATA

        ##RETRIEVE TOPICS
        top_n = 10
        for idx, topic in enumerate(lda_model.components_):
            cluster_topics.append([(vectorizer.get_feature_names()[i], topic[i])for i in topic.argsort()[:-top_n - 1:-1]])


    ##PRINT CLUSTERS
    for cluster_index in range(0, len(clusters)):
        print("__________________________Cluster Index: " + str(cluster_index) + "__________________________")
        print("Titles:")
        pprint([data.Source[i] + "  (" + str(data.Date[i]) +"): " + data.Title[i] for i in clusters[cluster_index]])
        print("")

        print("Topic:")
        print(cluster_topics[cluster_index])
        print("")



#############################################################################
## PROBLEM 2:  Identify top technology problems users are searching online ##
#############################################################################
def googleTrendingTopics():

    ##GET DATA
    data = pd.read_csv("./data/googleData.csv")
    text = data["query"]

    ##CLUSTER TEXT
    num_of_clusters = None
    clusters = cluster_texts(text, num_of_clusters)

    ##FILTER FOR CLUSTER GROUPS
    clusters_new = []
    for cluster_index in range(0, len(clusters)):
        if(len(clusters[cluster_index]) > 1):
            clusters_new.append(clusters[cluster_index])
    clusters = clusters_new

    ##GET TOPICS FOR CLUSTERS
    cluster_articles = []
    for cluster_index in range(0, len(clusters)):
        cluster_articles.append([text[i] for i in clusters[cluster_index]])


    NUM_TOPICS = 1
    cluster_topics = []
    for d in cluster_articles:
        article_text = d
        vectorizer = CountVectorizer(tokenizer=process_text,
                                 stop_words=stopwords.words('english'),
                                 lowercase=True)
        data_vectorized = vectorizer.fit_transform(article_text)  ##OUTPUT NOT USED, BUT VECTORIZER NEEDS TO FIT DATA

        ##BUILD LDA
        lda_model = LatentDirichletAllocation(n_components=NUM_TOPICS, max_iter=20, learning_method='online')
        lda_Z = lda_model.fit_transform(data_vectorized)  ##OUTPUT NOT USED, BUT VECTORIZER NEEDS TO FIT DATA

        ##RETRIEVE TOPICS
        top_n = 5
        for idx, topic in enumerate(lda_model.components_):
            cluster_topics.append([(vectorizer.get_feature_names()[i], topic[i])for i in topic.argsort()[:-top_n - 1:-1]])



    ##PRINT CLUSTERS
    for cluster_index in range(0, len(clusters)):
        print("__________________________Cluster Index: " + str(cluster_index) + "__________________________")
        print("Google Query Data:")
        pprint([text[i] for i in clusters[cluster_index]])
        print("")

        print("Topic:")
        print(cluster_topics[cluster_index])
        print("")






def main(argv):
    ##GET ARGUMENTS
    try:
        opts, args = getopt.getopt(argv, "c:", ["command="])
    except getopt.GetoptError:
        print("Error")
        sys.exit(1)

    command = None
    for opt, arg in opts:
        if opt in ("-c", "--command"):
            command= arg

    if command == "blogTrendingTopics":
        bloggersTrendingTopics()
    elif command == "googleTrendingTopics":
        googleTrendingTopics()



if __name__ == "__main__":
    main(sys.argv[1:])


