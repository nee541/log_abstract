if __name__ is not None and "." in __name__:
    from .corpus_indexing import load_index, dump_index
    from .tfidf_matching import match_tfidf
else:
    from corpus_indexing import load_index, dump_index
    from tfidf_matching import match_tfidf

def main(f_vectorizer, f_matrix):
    corpus = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one.',
        'Is this the first document?',
    ]
    kwargs = {
        "lowercase": True,
        "min_df": 1,
        "max_df": 1.0,
        "ngram_range": (1, 1),
    }
    dump_index(corpus=corpus, kwargs=kwargs, f_vectorizer=f_vectorizer, f_matrix=f_matrix)
    vectorizer, matrix = load_index(f_vectorizer, f_matrix)
    query = "the second document"
    for i, score in match_tfidf(query=query, vectorizer=vectorizer, matrix=matrix, top_n=10, min_score=0.0):
        print("Document:", i)
        print("Cosine similarity score:", score)
        print(corpus[i])

if __name__ == "__main__":
    f_vectorizer = "vectorizer.pickle"
    f_matrix = "matrix.pickle"
    main(f_vectorizer=f_vectorizer, f_matrix=f_matrix)