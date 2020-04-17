from datetime import datetime
from common import generate
from common import settings as s
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
        "url_last_ipv4": None,
        "url_last_ipv6": None,
    }


def simulate_parse_url(url):
    parsed_list = [
        {
            "url": url["url"],
            "url_discovery_date": url["url_discovery_date"],
            "url_last_visited": str(datetime.now()),
            "url_last_ipv4": None,
            "url_last_ipv6": None,
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
    for url in url_frontier:
        cumulative_parsed_list.extend(simulate_parse_url(url))
        # sleep(url_frontier["fqdn_crawl_delay"] + random.random())

    return cumulative_parsed_list


def get_list_of_urls(frontier_list):
    return [
        url
        for url_frontier in frontier_list["url_frontiers"]
        for url in url_frontier["url_list"]
    ]


def simulate_full_fetch(frontier_list):
    p = Pool(processes=s.parallel_processes)
    data = p.map(simulate_short_term_fetch, get_list_of_urls(frontier_list),)
    p.close()

    return {
        "uuid": frontier_list["uuid"],
        "urls_count": len(data),
        "urls": data,
    }
