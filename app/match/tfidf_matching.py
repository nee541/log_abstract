from sklearn.metrics.pairwise import cosine_similarity

def match_tfidf(query, vectorizer, matrix, top_n=10, min_score=0.0):
    query_tfidf = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_tfidf, matrix).flatten()
    ranking = cosine_similarities.argsort()[::-1]
    for i in range(min(top_n, len(ranking))):
        if cosine_similarities[ranking[i]] < min_score:
            break
        else:
            yield ranking[i], cosine_similarities[ranking[i]]


def match_template(template, query):
    pass