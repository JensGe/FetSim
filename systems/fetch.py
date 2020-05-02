from common import generate
from common import settings as s
from common import pyd_models as pyd

from multiprocessing import Pool
from time import sleep
from datetime import datetime
from typing import List

import random
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def new_internal_cond(internal_vs_external_randomness, known_vs_unknown_randomness):
    return (
        internal_vs_external_randomness < s.internal_vs_external_threshold
        and known_vs_unknown_randomness < s.new_vs_existing_threshold
    )


def existing_internal_cond(internal_vs_external_randomness, known_vs_unknown_randomness):
    return (
            internal_vs_external_randomness < s.internal_vs_external_threshold
            and known_vs_unknown_randomness >= s.new_vs_existing_threshold
        )


def new_external_cond(internal_vs_external_randomness, known_vs_unknown_randomness):
    return (
        internal_vs_external_randomness >= s.internal_vs_external_threshold
        and known_vs_unknown_randomness < s.new_vs_existing_threshold
    )


def existing_external_cond(internal_vs_external_randomness, known_vs_unknown_randomness):
    return (
            internal_vs_external_randomness >= s.internal_vs_external_threshold
            and known_vs_unknown_randomness >= s.new_vs_existing_threshold
        )


def generate_new_internal_url(url: pyd.Url):
    return pyd.Url(
        url=generate.get_similar_url(url).url,
        fqdn=generate.get_fqdn_from_url(url),
        url_discovery_date=str(datetime.now()),
        url_last_visited=None,
        url_blacklisted=False,
        url_bot_excluded=False,
    )


def generate_existing_url(fqdn: str = None):
    url = generate.get_random_existing_url(fqdn=fqdn)

    return pyd.Url(
        url=url.url,
        fqdn=url.fqdn,
        url_discovery_date=str(datetime.now()),
        url_last_visited=None,
        url_blacklisted=False,
        url_bot_excluded=False,
    )


def simulate_parse_url(url: pyd.Url) -> List[pyd.Url]:
    parsed_list = [url]

    simulated_link_amount = random.randint(s.min_links_per_page, s.max_links_per_page)
    for _ in range(simulated_link_amount):
        internal_external_rand = random.random()
        known_unknown_rand = random.random()

        if new_internal_cond(internal_external_rand, known_unknown_rand):
            parsed_list.append(generate_new_internal_url(url))

        if existing_internal_cond(internal_external_rand, known_unknown_rand):
            parsed_list.append(generate_existing_url(fqdn=url.fqdn))

        if new_external_cond(internal_external_rand, known_unknown_rand):
            parsed_list.append(generate.get_random_url())

        if existing_external_cond(internal_external_rand, known_unknown_rand):
            parsed_list.append(generate_existing_url())

    return parsed_list


def simulate_short_term_fetch(url_frontier_list: pyd.UrlFrontier) -> List[pyd.Url]:
    cumulative_parsed_list = []
    for url in url_frontier_list.url_list:
        cumulative_parsed_list.extend(simulate_parse_url(url))

        sleep(url_frontier_list.fqdn_crawl_delay / s.crawling_speed)

    return cumulative_parsed_list


def simulate_full_fetch(frontier_response: pyd.FrontierResponse):
    p = Pool(processes=s.parallel_processes)
    url_data = p.map(simulate_short_term_fetch, frontier_response.url_frontiers)
    p.close()

    logging.info(url_data[0])

    return pyd.SimulatedParsedList(
        uuid=frontier_response.uuid, urls_count=len(url_data[0]), urls=url_data[0]
    )
