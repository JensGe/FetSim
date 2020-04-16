from datetime import datetime
from time import sleep
from app import settings as s, generate
import random
from multiprocessing import Pool


def generate_new_internal_url(url):
    return {
        "url": generate.get_similar_url(url),
        "url_discovery_date": datetime.now(),
    }


def generate_new_url():
    return {
        "url": generate.get_random_url(),
        "url_discovery_date": datetime.now(),
        "url_last_visited": None,
    }


def simulate_parse_url(url):
    parsed_list = [
        {
            "url": url["url"],
            "url_discovery_date": url["url_discovery_date"],
            "url_last_visited": datetime.now(),
        }
    ]

    urls_found = s.url_discoveries
    for _ in range(urls_found):
        if random.random() < s.internal_discovery_ratio:
            parsed_list.extend(generate_new_internal_url(url))
        else:
            parsed_list.append(generate_new_url())

    return parsed_list


def simulate_short_term_fetch(url_frontier):
    cumulative_parsed_list = []
    for url in url_frontier["url_list"]:
        cumulative_parsed_list.extend(simulate_parse_url(url))
        # sleep(url_frontier["fqdn_crawl_delay"] + random.random())

    return cumulative_parsed_list


def simulate_full_fetch(frontier_list):

    p = Pool(processes=s.parallel_processes)
    data = p.map(
        simulate_short_term_fetch,
        [url_frontier for url_frontier in frontier_list["url_frontiers"]],
    )
    p.close()

    return data
