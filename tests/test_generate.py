from common import generate
from common import pyd_models as pyd
from datetime import datetime

def test_get_random_existing_url():
    single_random_existing_url = generate.get_random_existing_url()
    assert isinstance(single_random_existing_url, pyd.Url)


def test_get_random_crawl_delay():
    crawl_delay_list = [generate.random_crawl_delay() for _ in range(200)]
    print(crawl_delay_list)
    assert isinstance(crawl_delay_list[0], int) or crawl_delay_list[0] is None


# def test_random_entity_tag():
#     etag = generate.page_change()
#     print(etag)
#     assert len(etag) == 18
#     assert isinstance(etag, str)
#     assert etag.islower()

def test_random_datetime():
    random_datetime = generate.random_datetime()
    for _ in range(100):
        print(generate.random_datetime())
    assert isinstance(random_datetime, datetime)
