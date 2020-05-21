from common import generate as gen
from common import local
from common import pyd_models as pyd

from time import sleep
from datetime import datetime
from typing import List

import multiprocessing as mp
import random
import logging
import requests


def new_internal_cond(internal_vs_external_randomness, known_vs_unknown_randomness):
    return internal_vs_external_randomness < local.load_setting(
        "internal_vs_external_threshold"
    ) and known_vs_unknown_randomness < local.load_setting("new_vs_existing_threshold")


def existing_internal_cond(
    internal_vs_external_randomness, known_vs_unknown_randomness
):
    return internal_vs_external_randomness < local.load_setting(
        "internal_vs_external_threshold"
    ) and known_vs_unknown_randomness >= local.load_setting(
        "new_vs_existing_threshold"
    )


def new_external_cond(internal_vs_external_randomness, known_vs_unknown_randomness):
    return internal_vs_external_randomness >= local.load_setting(
        "internal_vs_external_threshold"
    ) and known_vs_unknown_randomness < local.load_setting("new_vs_existing_threshold")


def existing_external_cond(
    internal_vs_external_randomness, known_vs_unknown_randomness
):
    return internal_vs_external_randomness >= local.load_setting(
        "internal_vs_external_threshold"
    ) and known_vs_unknown_randomness >= local.load_setting(
        "new_vs_existing_threshold"
    )


def generate_new_internal_url(url: pyd.Url):
    return pyd.Url(
        url=gen.get_similar_url(url).url,
        fqdn=gen.get_fqdn_from_url(url),
        url_discovery_date=str(datetime.now()),
        url_last_visited=None,
        url_blacklisted=False,
        url_bot_excluded=False,
    )


def generate_existing_url(session: requests.Session, fqdn: str = None):
    url = gen.get_random_existing_url(session=session, fqdn=fqdn)

    return pyd.Url(
        url=url.url,
        fqdn=url.fqdn,
        url_discovery_date=str(datetime.now()),
        url_last_visited=None,
        url_blacklisted=False,
        url_bot_excluded=False,
    )


def simulate_parse_url(url: pyd.Url, session: requests.Session) -> List[pyd.Url]:
    url.url_last_visited = datetime.now()
    parsed_list = [url]

    simulated_link_amount = random.randint(
        local.load_setting("min_links_per_page"),
        local.load_setting("max_links_per_page"),
    )

    logging.debug("{} Next URL: {}".format(mp.current_process(), url.url))

    for _ in range(simulated_link_amount):
        internal_external_rand = random.random()
        known_unknown_rand = random.random()

        if new_internal_cond(internal_external_rand, known_unknown_rand):
            new_url = generate_new_internal_url(url)
            logging.debug(
                "{} New Internal URL: {}".format(mp.current_process(), new_url.url)
            )
            parsed_list.append(new_url)

        if existing_internal_cond(internal_external_rand, known_unknown_rand):
            new_url = generate_existing_url(session=session, fqdn=url.fqdn)
            logging.debug(
                "{} Existing Internal URL: {}".format(mp.current_process(), new_url.url)
            )
            parsed_list.append(new_url)

        if new_external_cond(internal_external_rand, known_unknown_rand):
            new_url = gen.get_random_url()
            logging.debug(
                "{} New External URL: {}".format(mp.current_process(), new_url.url)
            )
            parsed_list.append(new_url)

        if existing_external_cond(internal_external_rand, known_unknown_rand):
            new_url = generate_existing_url(session=session)
            logging.debug(
                "{} Existing External URL: {}".format(mp.current_process(), new_url.url)
            )
            parsed_list.append(new_url)

    return parsed_list


def simulate_short_term_fetch(url_frontier_list: pyd.UrlFrontier) -> List[pyd.Url]:
    crawl_delay = (
        local.load_setting("default_crawl_delay")
        if url_frontier_list.fqdn_crawl_delay is None
        else url_frontier_list.fqdn_crawl_delay
    )
    simulated_crawl_delay = crawl_delay / local.load_setting("crawling_speed_factor")

    session = requests.Session()
    cumulative_parsed_list = []

    for url in url_frontier_list.url_list:
        cumulative_parsed_list.extend(simulate_parse_url(url, session))
        sleep(simulated_crawl_delay)

    logging.info(
        "Short Term Frontier processed. FQDN {}, URLs {}".format(
            url_frontier_list.fqdn, url_frontier_list.fqdn_url_count
        )
    )
    return cumulative_parsed_list


def simulate_fqdn_parse(url_frontier_list: pyd.UrlFrontier) -> pyd.UrlFrontier:
    logging.debug(
        "{} Sim FQDN Parse: {}".format(mp.current_process(), url_frontier_list.fqdn)
    )
    url_frontier_list.fqdn_last_ipv4 = (
        gen.random_ipv4()
        if url_frontier_list.fqdn_last_ipv4 is None
        else url_frontier_list.fqdn_last_ipv4
    )

    url_frontier_list.fqdn_last_ipv6 = (
        gen.random_example_ipv6()
        if url_frontier_list.fqdn_last_ipv6 is None
        else url_frontier_list.fqdn_last_ipv6
    )

    url_frontier_list.fqdn_pagerank = (
        gen.random_pagerank()
        if url_frontier_list.fqdn_pagerank is None
        else url_frontier_list.fqdn_pagerank
    )

    url_frontier_list.fqdn_crawl_delay = (
        gen.random_crawl_delay()
        if url_frontier_list.fqdn_crawl_delay is None
        else url_frontier_list.fqdn_crawl_delay
    )

    return url_frontier_list


def get_tld(fqdn):
    if fqdn.split(".")[-2] == "co":
        tld = ".".join(fqdn.split(".")[-2:])
    else:
        tld = fqdn.split(".")[-1]
    return tld


def fqdns_from_url_list(url_list: List[pyd.Url]) -> List[pyd.UrlFrontier]:
    fqdn_list = []
    for url in url_list:
        fqdn_list.append(pyd.UrlFrontier(fqdn=url.fqdn, tld=get_tld(url.fqdn)))
    return fqdn_list


def unique_fqdn_list(a, b) -> List:
    new = []
    for url in a:
        if url.fqdn not in [url.fqdn for url in new]:
            new.append(url)

    for url in b:
        if url.fqdn not in [url.fqdn for url in new]:
            new.append(url)

    return new


def simulate_full_fetch(long_term_frontier: pyd.FrontierResponse):

    logging.debug("Long Term Frontier: {}".format(long_term_frontier))

    fqdn_pool = mp.Pool(processes=local.load_setting("parallel_process"))
    url_frontier_list = fqdn_pool.map(
        simulate_fqdn_parse, long_term_frontier.url_frontiers
    )
    fqdn_pool.close()

    logging.debug("URL Frontier List ins: {}".format(url_frontier_list))

    url_pool = mp.Pool(processes=local.load_setting("parallel_process"))
    url_data = url_pool.map(simulate_short_term_fetch, url_frontier_list)
    url_pool.close()

    flat_url_data = [url for url_list in url_data for url in url_list]

    logging.debug("Url Data: {}".format(flat_url_data))

    all_new_fqdns = fqdns_from_url_list(flat_url_data)
    extended_url_frontier_list = unique_fqdn_list(url_frontier_list, all_new_fqdns)

    processed_frontier = pyd.FrontierResponse(
        uuid=long_term_frontier.uuid,
        response_url=long_term_frontier.response_url,
        latest_return=long_term_frontier.latest_return,
        url_frontiers_count=long_term_frontier.url_frontiers_count,
        urls_count=long_term_frontier.url_count,
        url_frontiers=extended_url_frontier_list,
    )

    return pyd.SimulatedParsedList(
        uuid=long_term_frontier.uuid,
        fqdn_count=len(processed_frontier.url_frontiers),
        fqdns=processed_frontier.url_frontiers,
        url_count=len(flat_url_data),
        urls=flat_url_data,
    )
