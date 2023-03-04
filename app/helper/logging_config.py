import logging.config

def setup_logging():
    # Logging configuration
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file-regular": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": "out/log/regular.log",
                "mode": "w"
            },
            "file-db": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": "out/log/db.log",
                "mode": "w"
            },
            "file-parser": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": "out/log/parser.log",
                "mode": "w"
            }
        },
        "loggers": {
            "main": {
                "handlers": ["file-regular"],
                "level": "DEBUG"
            },
            "db.sqlite3": {
                "handlers": ["file-db"],
                "level": "DEBUG"
            },
            "interact": {
                "handlers": ["console" ,"file-regular"],
                "level": "DEBUG"
            },
            "parser": {
                "handlers": ["file-parser"],
                "level": "DEBUG"
            }
        }
    }
    logging.config.dictConfig(LOGGING_CONFIG)