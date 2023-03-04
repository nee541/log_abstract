# TF-IDF Vectorizer stored file path
FILE_VECTORIZER = "out/model/vectorizer.pickle"

# TF-IDF Matrix stored file path
FILE_MATRIX = "out/model/matrix.pickle"

# Folder path of the java source code
FOLDER_PATH = "./../resources/hadoop_source_code"

# The pattern of the java source code
FILE_PATTERN = "**/*hdfs*/**/*.java"

# Log level of slf4j
LOG_LEVEL = ('error', 'warn', 'info', 'debug', 'trace')

# The regex pattern of log level
LOG_LEVEL_PATTERN = r'error|warn|info|debug|trace'

DB_NAME = "out/db/test.db"


# SQL to create table of unresolved logs
# SQL_CREATE_TABLE_UNRESOLVED_LOGS = """
# CREATE TABLE IF NOT EXISTS unresolved_logs (
#     log text PRIMARY KEY,
#     method_id integer NOT NULL REFERENCES method(id)
# )
# """
# SQL to insert into table of unresolved logs
# SQL_INSERT_TABLE_UNRESOLVED_LOGS = """
# INSERT INTO unresolved_logs (log, method_id)
# VALUES (?, ?)
# """


# SQL to create table of logs
SQL_CREATE_TABLE_LOGS ="""
CREATE TABLE IF NOT EXISTS logs (
    template text PRIMARY KEY,
    level text,
    comments text,
    intention text,
    id integer NOT NULL,
    method_id integer NOT NULL REFERENCES method(id)
)
"""
# SQL to select all the logs
SQL_SELECT_FROM_LOGS = """
SELECT * FROM logs
WHERE template == ?
"""
# SQL to insert into table of logs
SQL_INSERT_TABLE_LOGS = """
INSERT INTO logs (template, level, comments, intention, id, method_id)
VALUES (?, ?, ?, ?, ?, ?)
"""

SQL_SELECT_FROM_TABLE_BY = """
SELECT * FROM ?
    WHERE ? == ?;
"""

# SQL to create table of method
SQL_CREATE_TABLE_METHOD = """
CREATE TABLE IF NOT EXISTS method (
    id integer PRIMARY KEY,
    code text,
    file text,
    summary text
)
"""
# SQL to insert into table of method
SQL_INSERT_TABLE_METHOD = """
INSERT INTO method (id, code, file, summary)
VALUES (?, ?, ?, ?)
"""

# SQL to remove all the tables
SQL_REMOVE_ALL_TABLES = """
PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS method;
PRAGMA foreign_keys = ON;
"""

OPTION_RESET = "reset"
