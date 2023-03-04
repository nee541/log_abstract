import logging

logger = logging.getLogger("main")

import configparser
config = configparser.ConfigParser()
config.read("app/config.ini")
FILE_VECTORIZER = config["file_path"]["FILE_VECTORIZER"]
FILE_MATRIX = config["file_path"]["FILE_MATRIX"]

from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def dump_index(corpus, kwargs, f_vectorizer=FILE_VECTORIZER, f_matrix=FILE_MATRIX):
    vectorizer = TfidfVectorizer(**kwargs)
    matrix = vectorizer.fit_transform(corpus)
    logger.info("Dumping index to %s and %s", f_vectorizer, f_matrix)
    
    with open(f_vectorizer, "wb") as f:
        pickle.dump(vectorizer, f)
    
    with open(f_matrix, "wb") as f:
        pickle.dump(matrix, f)

def load_index(f_vectorizer=FILE_VECTORIZER, f_matrix=FILE_MATRIX):
    logger.info("Loading index from %s and %s", f_vectorizer, f_matrix)
    with open(f_vectorizer, 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open(f_matrix, 'rb') as f:
        matrix = pickle.load(f)
    
    return vectorizer, matrix


if __name__ == "__main__":
    from app.match.tfidf_matching import match_tfidf
    
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
    dump_index(corpus=corpus, kwargs=kwargs)
    vectorizer, matrix = load_index()
    query = "the second document"
    for i, score in match_tfidf(query=query, vectorizer=vectorizer, matrix=matrix, top_n=10, min_score=0.0):
        print("Document:", i)
        print("Cosine similarity score:", score)
        print(corpus[i])