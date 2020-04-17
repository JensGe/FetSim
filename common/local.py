import pickle
import os.path

from common import settings as s


def file_exists(file_string):
    return os.path.isfile(file_string)


def save_uuid_to_pickle(uuid):
    with open(s.uuid_file, "wb") as file:
        pickle.dump(uuid, file)


def get_pickle_uuid():
    with open(s.uuid_file, "rb") as file:
        return pickle.load(file)









