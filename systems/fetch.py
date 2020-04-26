from datetime import datetime
from common import generate
from common import settings as s
import random
from multiprocessing import Pool
from time import sleep


def generate_new_internal_url(url):
    return {
        "url": generate.get_similar_url(url["url"]),
        "fqdn": generate.get_fqdn_from_url(url["url"]),
        "url_discovery_date": str(datetime.now()),
        "url_last_visited": None,
        "url_blacklisted": False,
        "url_bot_excluded": False
    }


def generate_new_url():
    fqdn = generate.get_random_fqdn()
    url = generate.get_random_url(fqdn=fqdn)
    return {
        "url": url,
        "fqdn": fqdn,
        "url_discovery_date": str(datetime.now()),
        "url_last_visited": None,
        "url_blacklisted": False,
        "url_bot_excluded": False
    }


def simulate_parse_url(url):
    parsed_list = [
        {
            "url": url["url"],
            "fqdn": url["fqdn"],
            "url_discovery_date": url["url_discovery_date"],
            "url_last_visited": str(datetime.now()),
            "url_blacklisted": url["url_blacklisted"],
            "url_bot_excluded": url["url_bot_excluded"]
        }
    ]

    urls_found = s.max_links_per_page
    for _ in range(urls_found):
        if random.random() < s.remaining_link_ratio:
            parsed_list.extend(generate_new_internal_url(url))
        else:
            parsed_list.append(generate_new_url())

    return parsed_list


def simulate_short_term_fetch(short_term_frontier):
    cumulative_parsed_list = []
    for url in short_term_frontier["url_list"]:
        cumulative_parsed_list.extend(simulate_parse_url(url))
        sleep(short_term_frontier["fqdn_crawl_delay"] / s.crawling_speed)

    return cumulative_parsed_list


def get_list_of_frontiers(frontier_list):
    return [url_frontier for url_frontier in frontier_list["url_frontiers"]]


def simulate_full_fetch(frontier_partition):
    p = Pool(processes=s.parallel_processes)
    url_data = p.map(simulate_short_term_fetch, get_list_of_frontiers(frontier_partition))
    p.close()

    return {
        "uuid": frontier_partition["uuid"],
        "urls_count": len(url_data[0]),
        "urls": url_data[0],
    }
