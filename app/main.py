import requests
import pickle
import os.path
import random
import string


def save_uuid(uuid):
    with open("uuid", "wb") as file:
        pickle.dump(uuid, file)


def get_uuid():
    with open("uuid", "rb") as file:
        return pickle.load(file)


def generate_random_crawler_name():
    chars = string.ascii_lowercase + "1234567890-_"
    return "".join(random.choice(chars) for _ in range(15)).title()


def init_crawler():
    crawler_name = generate_random_crawler_name()
    create_crawler_dict = {
        "contact": "admin@fetsim.de",
        "name": "Mister {}".format(crawler_name),
        "location": "Germany",
        "tld_preference": "de",
    }

    new_crawler_response = requests.post(
        "http://ec2-3-16-31-169.us-east-2.compute.amazonaws.com/crawlers",
        json=create_crawler_dict,
    )

    new_crawler_json = new_crawler_response.json()

    save_uuid(new_crawler_json["uuid"])


def get_frontier(uuid):
    frontier_request_dict = {
        "crawler_uuid": uuid,
        "amount": 5,
        "length": 5
    }
    frontier_response = requests.post(
        "http://ec2-3-16-31-169.us-east-2.compute.amazonaws.com/frontiers",
        json=frontier_request_dict,
    )

    frontier_response = frontier_response.json()
    return frontier_response


if not os.path.isfile("uuid"):
    init_crawler()

frontier_response = get_frontier(get_uuid())
print(frontier_response)


