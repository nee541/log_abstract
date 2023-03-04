from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?',
]

def filter(text):
    return "After filter " + text

vectorizer = TfidfVectorizer(lowercase=True)
matrix = vectorizer.fit_transform(corpus)
tf_idf = pd.DataFrame(matrix.toarray(), columns=vectorizer.get_feature_names_out())

# add the frequency of each term
# tf_idf.loc["Frequency"] = (tf_idf > 0).sum()
# tf_idf = tf_idf.append(pd.Series((tf_idf > 0).sum(), name='Frequency'))
# tf_idf = tf_idf.drop("Frequency", errors="ignore")

# reorganize the dataframe
# tf_idf = tf_idf.stack().reset_index()
# tf_idf = tf_idf.rename(columns={0:'tfidf', 'level_0': 'corpus','level_1': 'term', 'level_2': 'term'})
# tf_idf = tf_idf.sort_values(by=['corpus','tfidf'], ascending=[True,False]).groupby(['corpus']).head(10)

query = "the second document"

query_tfidf = vectorizer.transform([query])

cosine_similarities = cosine_similarity(query_tfidf, matrix).flatten()
ranking = cosine_similarities.argsort()[::-1]
for i in ranking:
    print("Document:", i)
    print("Cosine similarity score:", cosine_similarities[i])
    print(corpus[i])

# print(vectorizer.get_stop_words())
# print(vectorizer.get_feature_names_out())
# # print(vector.toarray())
# print(tf_idf)