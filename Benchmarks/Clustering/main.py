# Kommentar von Marius
"""
Dies Clustering basiert auf TF-IDF in Kombination mit KMeans -> siehe ggf. Theoriebereich der Studienarbeit.
Anzumerken ist, dass die Cluster nicht eindeutig sein werden, da bspw. ein Call for Paper von den "Keywords"
ähnlich sein kann wie ein anderer Bereich.
Link: https://medium.com/mlearning-ai/text-clustering-with-tf-idf-in-python-c94cd26a31e7
"""
# ===================
import numpy as np
import pandas as pd
from msvcrt import getch

# import sklearn library's
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# string manipulation library's
import re
import string
import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Visualization Library's'
import matplotlib.pyplot as plt
import seaborn as sns

# Import own .py files
import process


def preprocess(text: str, r_stopwords: bool) -> str:
    # remove links from text
    text = re.sub(r"http\S+", "", text)
    # remove numbers and special characters from text
    text = re.sub("[^A-Za-z]+", " ", text)
    # remove stopwords
    if r_stopwords:
        # 1. creates tokens
        tokens = nltk.word_tokenize(text)
        # 2. checks if token is a stopword and removes it
        tokens = [w for w in tokens if not w.lower() in stopwords.words("english")]
        # 3. joins all tokens again
        text = " ".join(tokens)
    # returns cleaned text
    text = text.lower().strip()
    return text


# for each row of the dataframe, find the n terms that have the highest tf idf score
def k_means(vec, df, name, vectorizer):
    # initialize KMeans with 4 clusters
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(vec)
    clusters = kmeans.labels_
    # initialize PCA with 2 components
    pca = PCA(n_components=2, random_state=42)
    # pass X to the pca
    pca_vecs = pca.fit_transform(vec.toarray())
    # save the two dimensions in x0 and x1
    x0 = pca_vecs[:, 0]
    x1 = pca_vecs[:, 1]

    # get top N Keywords from each Cluster
    n = 20
    df_key = pd.DataFrame(vec.todense()).groupby(clusters).mean()  # groups tf idf vector per cluster
    terms = vectorizer.get_feature_names_out()  # access to tf idf terms
    for i, r in df_key.iterrows():
        print('\nCluster {}'.format(i))
        print(','.join([terms[t] for t in np.argsort(r)[-n:]]))

    # assign clusters and PCA vectors to columns in the original dataframe
    df['cluster'] = clusters
    df['x0'] = x0
    df['x1'] = x1


    cluster_map = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6"}  # mapping found through get_top_keywords
    df['cluster'] = df['cluster'].map(cluster_map)

    # set image size
    plt.figure(figsize=(12, 7))
    # set title
    plt.title("TF-IDF and KMeans using Mail-{}".format(name), fontdict={"fontsize": 18})
    # set axes names
    plt.xlabel("X0", fontdict={"fontsize": 16})
    plt.ylabel("X1", fontdict={"fontsize": 16})
    #  create scatter plot with seaborn, where hue is the class used to group the data
    sns.scatterplot(data=df, x='x0', y='x1', hue='cluster', palette="viridis")
    plt.show(block=False)
    print('Continue')


def main():
    # Import DataSet and preprocess
    dataset = process.import_data()

    # initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, max_df=0.95)

    # Cluster with Only Subject
    df_subject = pd.DataFrame(data=dataset['Subject'], columns=['Subject'])
    df_subject['clean'] = df_subject['Subject'].apply(lambda x: preprocess(x, r_stopwords=True))
    # fit_transform is used to apply TF-IDF to our cleaned Text, then the Vector of arrays gets saved in vec
    vec = vectorizer.fit_transform(df_subject['clean'])
    # Call k_means Function with Vector and DataFrame
    k_means(vec, df_subject, 'Subject', vectorizer)

    # Cluster with Only Body
    df_body = pd.DataFrame(data=dataset['Body'], columns=['Body'])
    df_body['clean'] = df_body['Body'].apply(lambda x: preprocess(x, r_stopwords=True))
    # fit_transform is used to apply TF-IDF to our cleaned Text, then the Vector of arrays gets saved in vec
    vec = vectorizer.fit_transform(df_body['clean'])
    # Call k_means Function with Vector and DataFrame
    k_means(vec, df_body, 'Body', vectorizer)

    # Cluster with Subject and Body
    df_both = pd.DataFrame(dataset['Subject']+dataset['Body'], columns=['Both'])
    df_both['clean'] = df_both['Both'].apply(lambda x: preprocess(x, r_stopwords=True))
    # fit_transform is used to apply TF-IDF to our cleaned Text, then the Vector of arrays gets saved in vec
    vec = vectorizer.fit_transform(df_both['clean'])
    # Call k_means Function with Vector and DataFrame
    k_means(vec, df_both, 'Both', vectorizer)

    print("Press any key to exit...")
    junk = getch()
    return 0


if __name__ == "__main__":
    main()
