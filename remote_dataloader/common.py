import json
import pickle
import random
import string

import logging

formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


CODE_INIT = 'init'
CODE_POLL = 'poll'


def random_string(string_length=10):
    """
    Generate a random string of fixed length
    ref : https://pynative.com/python-generate-random-string/
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def byte_message(myid, code, message):
    return pickle.dumps({
        'myid': myid,
        'code': code,
        'message': message
    }, protocol=pickle.HIGHEST_PROTOCOL)
