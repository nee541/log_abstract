# -*- coding: utf-8 -*-
import sys, importlib
from pathlib import Path

def import_parents(level=1):
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]
    
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__) # won't be needed after that

import_parents()

import logging
from app.helper import logging_config
logging_config.setup_logging()
logger = logging.getLogger("interact")

import argparse

# from .helper import settings, db
from .reader import reader
db = reader.db
settings = reader.settings

from .match.corpus_indexing import load_index, dump_index
from .match.tfidf_matching import match_tfidf

# from app.reader import reader
# from app.helper import settings
# import app.helper.db as db
# from app.match.corpus_indexing import load_index, dump_index
# from app.match.tfidf_matching import match_tfidf
import re
# match all the comments in java code

# replace newlines in the text with spaces
def replace_newlines(text: str, replacement=" "):
    pattern = re.compile(r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)")
    # replace all the comments with spaces
    text = re.sub(pattern, replacement, text)
    return text.strip().replace("\n", replacement)
    # return text.strip().replace("\n", replacement)
    

def prepare():
    logger.info("Parse Hadoop Source Code and store in sqlite3 ...")
    reader.scheduler(settings.FOLDER_PATH, settings.FILE_PATTERN, settings.OPTION_RESET)
    corpus = db.get_template_corpus()
    kwargs = {}
    logger.info("Calculate TF-IDF and dump index ...")
    dump_index(corpus, kwargs)

def main():    
    # prepare()
    logger.info("Finish preparing")
    vectorizer, matrix = load_index()
    query = "get mount point"
    corpus = db.get_template_corpus()
    for i, score in match_tfidf(query=query, vectorizer=vectorizer, matrix=matrix, top_n=10, min_score=0.0):
        print("Document:", i)
        print("Cosine similarity score:", score)
        print(corpus[i])
    
    print("Started")
    # methods = db.get_methods()
    # print("Finished")
    # with open("out/methods.txt", "w") as f:
    #     for m in methods:
    #         f.write(m + "\n")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Abstraction")
    
    main()
    
    
