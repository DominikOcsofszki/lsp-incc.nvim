import logging
import os

def prep_logger(file_name: str):
    parent_dir = os.path.join(os.path.dirname(__file__), "logging")
    os.makedirs(parent_dir, exist_ok=True)


    logging.basicConfig(filename=f"{parent_dir}/{file_name}", level=logging.INFO)
    # logging.basicConfig(filename=f"{parent_dir}{file_name}", level=logging.NOTSET)
    logger = logging.getLogger(__name__)
    return logger


# file_name = "log_10_12_24.txt"
file_name = "log.txt"
LOGGING = prep_logger(file_name)
