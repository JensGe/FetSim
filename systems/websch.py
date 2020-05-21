import requests

from common import settings as s
from common import pyd_models as pyd
from common import local
from common import helper
import logging


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
        "amount": local.load_settings("fqdn_amount"),
        "length": local.load_settings("url_amount"),
        "long_term_mode": local.load_settings("long_term_mode"),
        "short_term_mode": local.load_settings("short_term_mode"),
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


def init_fetcher():
    if not local.file_exists(s.uuid_file):
        create_websch_crawler()

    if not websch_uuid_exists():
        create_websch_crawler()

    return local.get_pickle_uuid()


def init_fetcher_settings():
    local.save_settings_to_pickle(requests.get(s.websch_settings_endpoint).json())


def get_instance_id():
    rv = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    print(rv.text)
    print(rv.json())
    return rv.text

