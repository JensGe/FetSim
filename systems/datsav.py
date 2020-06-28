import requests
import logging
from common import pyd_models as pyd

logger = logging.getLogger("FETSIM")


def url_dict(url: pyd.Url) -> dict:
    discovery_date = (
        url.url_discovery_date
        if url.url_discovery_date is None
        else url.url_discovery_date.isoformat()
    )
    last_visited = (
        url.url_last_visited
        if url.url_last_visited is None
        else url.url_last_visited.isoformat()
    )

    return {
        "url": str(url.url),
        "fqdn": url.fqdn,
        "url_pagerank": url.url_pagerank,
        "url_discovery_date": discovery_date,
        "url_last_visited": last_visited,
        "url_blacklisted": url.url_blacklisted,
        "url_bot_excluded": url.url_bot_excluded,
    }


def fqdn_dict(fqdn: pyd.Frontier) -> dict:
    return {
        "fqdn": fqdn.fqdn,
        "tld": fqdn.tld,
        "fqdn_last_ipv4": fqdn.fqdn_last_ipv4,
        "fqdn_last_ipv6": fqdn.fqdn_last_ipv6,
        "fqdn_avg_pagerank": fqdn.fqdn_avg_pagerank,
        "fqdn_crawl_delay": fqdn.fqdn_crawl_delay,
        "fqdn_url_count": fqdn.fqdn_url_count,
        "url_list": [],
    }


def convert_parsed_list_to_dict(submit_list: pyd.SimulatedParsedList):
    return {
        "uuid": str(submit_list.uuid),
        "fqdn_count": submit_list.fqdn_count,
        "fqdns": [fqdn_dict(fqdn) for fqdn in submit_list.fqdns],
        "url_count": submit_list.url_count,
        "urls": [url_dict(url) for url in submit_list.urls],
    }


def submit_processed_list(submission_endpoint, submit_list: pyd.SimulatedParsedList):

    submit_dict = convert_parsed_list_to_dict(submit_list)

    submit_response = requests.post(url=submission_endpoint, json=submit_dict)

    logger.debug("Submission Endpoint: {}".format(submission_endpoint))
    logger.debug("Submission: {}".format(submit_dict))
    return submit_response.status_code
