import sqlite3
from sqlite3 import Error
import re
if __name__ is not None and "." in __name__:
    from .settings import *
else:
    from settings import *
import logging
logger = logging.getLogger("db.sqlite3")


class DBase(object):
    def __init__(self, db_name):
        self.db_name = db_name
    
    def __enter__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to {self.db_name}")
        except Error as e:
            logger.error(f"When connecting to the {self.db_name}, error occurs\n{str(e)}")
        finally:
            return self

    def __exit__(self, exc_type, exc_value, exc_trace_back):
        if self.conn:
            logger.info(f"Closed connection to {self.db_name}")
            self.conn.close()
    
    def create_tables(self, sqls=(SQL_CREATE_TABLE_LOGS, SQL_CREATE_TABLE_METHOD,)):
        try:
            for sql in sqls:
                logger.info(f"Creating table with sql: {sql}")
                self.cursor.execute(sql)
        except Error as e:
            logger.error(f"When creating tables, error occurs\n{str(e)}")
    
    def attribute_exists(self, table, attribute_name, attribute_value):
        try:
            sql = f"SELECT * FROM {table} WHERE {attribute_name} == ?;"
            self.cursor.execute(sql, (attribute_value,))
            logger.info(f"Checking if attribute {attribute_value} exists in table {table} with sql: {sql}")
            return len(self.cursor.fetchall()) > 0
        except Error as e:
            logger.error(f"When checking attribute exists, error occurs\n{str(e)}")

    def insert_into_table(self, sql, values, only_if=None):
        try:
            if callable(only_if):
                if not only_if():
                    return
            self.cursor.execute(sql, values)
            self.conn.commit()
            logger.info(f"Inserted \"{str(values)}\" into table with sql: {sql}")
        except Error as e:
            logger.error(f"When executing \"{sql}\" and inserting \"{str(values)}\", error occurs\n{str(e)}")

    
    def remove_tables(self, sql=SQL_REMOVE_ALL_TABLES):
        try:
            self.cursor.executescript(sql)
            logger.info(f"Removed all the tables with sql: {sql}")
        except Error as e:
            logger.error(f"When removing tables, error occurs\n{str(e)}")

    def select_from_table(self, sql, values):
        try:
            self.cursor.execute(sql, values)
            logger.info(f"Selected \"{str(values)}\" from table with sql: {sql}")
            return self.cursor.fetchall()
        except Error as e:
            logger.error(f"When executing \"{sql}\" and selecting \"{str(values)}\", error occurs\n{str(e)}")


def get_template_corpus(DB_NAME=DB_NAME):
    with DBase(DB_NAME) as db:
        sql = "SELECT template FROM logs;"
        logger.info(f"Getting template corpus with sql: {sql}")
        corpus = db.select_from_table(sql, ())
        corpus = [c[0] for c in corpus]
    return corpus

def get_corpus_id(DB_NAME=DB_NAME):
    with DBase(DB_NAME) as db:
        sql = "SELECT id FROM logs;"
        logger.info(f"Getting corpus id with sql: {sql}")
        IDs = db.select_from_table(sql, ())
        IDs = [c[0] for c in IDs]
    return IDs

pattern = re.compile(r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)")

# replace newlines in the text with spaces
def replace_newlines(text: str, replacement=" "):
    # replace all the comments with spaces
    text = re.sub(pattern, replacement, text)
    return text.strip().replace("\n", replacement)

def get_methods(DB_NAME=DB_NAME, process=None):
    with DBase(DB_NAME) as db:
        process = replace_newlines
        sql = "SELECT code FROM method;"
        cs = db.select_from_table(sql, ())
        logger.info(f"Getting methods with sql: {sql}")
        codes = []
        if callable(process):
            for c in cs:
                codes.append(process(c[0]))
        else:
            codes = [c[0] for c in cs]
    return codes

if __name__ == '__main__':
    with DBase('out/db/test.db') as db:
        # db.create_tables()
        # db.insert_into_table(SQL_INSERT_TABLE_LOGS, ())
        # db.remove_tables()
        # db.attribute_exists('logs', 'template', 'test')
        print(get_template_corpus())