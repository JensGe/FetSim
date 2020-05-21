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


def save_settings_to_pickle(settings):
    with open(s.settings_file, "wb") as file:
        pickle.dump(settings, file)


def load_setting(setting):
    with open(s.settings_file, "rb") as file:
        return pickle.load(file)[setting]


def load_all_settings():
    with open(s.settings_file, "rb") as file:
        return pickle.load(file)
