import json
import pickle
import random
import string


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
