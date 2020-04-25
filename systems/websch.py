import requests

from common import settings, helper, local
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def websch_uuid_exists():
    uuid = local.get_pickle_uuid()
    frontier_response = requests.patch(
        settings.websch_crawler_url, json={"uuid": str(uuid)}
    )
    if frontier_response.status_code == 200:
        return True
    elif frontier_response.status_code == 404:
        logging.debug("Crawler with UUID: {} not found".format(uuid))
        return False
    else:
        logging.error(frontier_response)


def get_frontier_partition(uuid):
    frontier_request_dict = {
        "crawler_uuid": uuid,
        "amount": 1,
    }

    frontier_response = requests.post(
        settings.websch_frontier_url, json=frontier_request_dict,
    )

    frontier_response = frontier_response.json()
    return frontier_response


def create_websch_crawler():
    crawler_name = helper.generate_random_crawler_name()
    create_crawler_dict = {
        "contact": "admin@fetsim.de",
        "name": "Demo-Fetcher #{}".format(crawler_name),
        "location": "Germany",
        "tld_preference": "de",
    }

    new_crawler_response = requests.post(
        settings.websch_crawler_url, json=create_crawler_dict,
    )

    new_crawler_json = new_crawler_response.json()

    local.save_uuid_to_pickle(new_crawler_json["uuid"])


def init_crawler():
    if not local.file_exists(settings.uuid_file):
        create_websch_crawler()

    if not websch_uuid_exists():
        create_websch_crawler()

    return local.get_pickle_uuid()
