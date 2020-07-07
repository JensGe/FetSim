from common import generate
from common import pyd_models as pyd
from datetime import datetime

import requests

session = requests.Session()


def test_get_random_existing_url():
    single_random_existing_url = generate.get_random_existing_url(session=session)
    assert isinstance(single_random_existing_url, pyd.Url)


def test_get_random_crawl_delay():
    crawl_delay_list = [generate.random_crawl_delay() for _ in range(200)]
    print(crawl_delay_list)
    assert isinstance(crawl_delay_list[0], int) or crawl_delay_list[0] is None


def test_random_datetime():
    random_datetime = generate.random_datetime()
    for _ in range(100):
        print(generate.random_datetime())
    assert isinstance(random_datetime, datetime)
