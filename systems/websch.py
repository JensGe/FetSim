import requests

from common import settings as s, helper, local
from common import pyd_models as pyd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def websch_uuid_exists():
    uuid = local.get_pickle_uuid()
    frontier_response = requests.patch(
        s.websch_crawler_endpoint, json={"uuid": str(uuid)}
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
        "amount": s.amount,
    }

    response = requests.post(
        s.websch_frontier_endpoint, json=frontier_request_dict
    ).json()
    return pyd.FrontierResponse(**response)


def create_websch_crawler():
    crawler_name = helper.generate_random_crawler_name()
    create_crawler_dict = {
        "contact": "admin@fetsim.de",
        "name": "Demo-Fetcher #{}".format(crawler_name),
        "location": "Germany",
        "tld_preference": "de",
    }

    new_crawler_response = requests.post(
        s.websch_crawler_endpoint, json=create_crawler_dict,
    )

    new_crawler_json = new_crawler_response.json()

    local.save_uuid_to_pickle(new_crawler_json["uuid"])


def init_crawler():
    if not local.file_exists(s.uuid_file):
        create_websch_crawler()

    if not websch_uuid_exists():
        create_websch_crawler()

    return local.get_pickle_uuid()
