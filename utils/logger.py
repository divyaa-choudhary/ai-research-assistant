import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger. Call this at the top of any file:
        logger = get_logger(__name__)
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO) #there are 5 logging levels -> DEBUG, INFO, WARNING, ERROR, CRITICAL

        log_format = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        #log to console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        #log to a file too, so your data persists
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger