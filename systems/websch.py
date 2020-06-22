import requests

from common import settings as s
from common import generate as gen
from common import pyd_models as pyd
from common import local
from common import helper
import logging


def websch_uuid_exists():
    uuid = local.get_pickle_uuid()
    frontier_response = requests.patch(
        s.websch_fetcher_endpoint, json={"uuid": str(uuid)}
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
        "fetcher_uuid": uuid,
        "amount": local.load_setting("fqdn_amount"),
        "length": local.load_setting("url_amount"),
        "long_term_mode": local.load_setting("long_term_mode"),
        "short_term_mode": local.load_setting("short_term_mode"),
    }

    response = requests.post(
        s.websch_frontier_endpoint, json=frontier_request_dict
    ).json()
    return pyd.FrontierResponse(**response)


def create_websch_fetcher():
    fetcher_name = helper.generate_random_fetcher_name()
    create_fetcher_dict = {
        "contact": "admin@fetsim.de",
        "name": "Demo-Fetcher #{}".format(fetcher_name),
        "location": "Germany",
        "tld_preference": gen.random_tld(),
    }

    new_fetcher_response = requests.post(
        s.websch_fetcher_endpoint, json=create_fetcher_dict,
    )

    new_fetcher_json = new_fetcher_response.json()

    local.save_uuid_to_pickle(new_fetcher_json["uuid"])


def init_fetcher():
    if not local.file_exists(s.uuid_file):
        create_websch_fetcher()

    if not websch_uuid_exists():
        create_websch_fetcher()

    return local.get_pickle_uuid()


def init_fetcher_settings():
    local.save_settings_to_pickle(requests.get(s.websch_settings_endpoint).json())


def get_instance_id():
    rv = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    return rv.text


def get_db_stats():
    return requests.get(s.websch_stats_endpoint).json()
