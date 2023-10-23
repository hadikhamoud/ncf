import json
import os
#setup logging to a file and to console
import logging
import sys
from config import LOGGING_DIR

def save_payload_by_query_params(payload, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = "payload.json"
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)



def build_payload_dir_name(path, **kwargs):
    name =  '_'.join(f'{k}-{v}' for k, v in kwargs.items())
    return os.path.join(path, name)




def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    if not os.path.exists(LOGGING_DIR):
        os.makedirs(LOGGING_DIR)

    log_file = os.path.join(LOGGING_DIR, log_file)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file, mode='a')        
    handler.setFormatter(formatter)

    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)

    return logger

