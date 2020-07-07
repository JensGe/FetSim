from systems import datsav
from common import settings
from common import pyd_models as pyd
import pytest


datsav_submit_endpoint = (
    "http://ec2-18-195-144-15.eu-central-1.compute.amazonaws.com/submit/"
)


@pytest.fixture
def submit_list():
    return pyd.SimulatedParsedList(
        uuid="12345678-90ab-cdef-0000-000000000000",
        fqdn_count=2,
        url_count=4,
        fqdns=[
            {
                "fqdn": "www.example.fr",
                "tld": "fr",
                "fqdn_last_ipv4": "123.456.789.0",
                "fqdn_last_ipv6": "2001:DB8::CF5C",
                "fqdn_pagerank": 0.00001,
                "fqdn_crawl_delay": 5,
                "fqdn_url_count": 2,
            },
            {
                "fqdn": "www.example.cn",
                "tld": "cn",
                "fqdn_last_ipv4": "126.456.789.2",
                "fqdn_last_ipv6": "2001:DB8::C25C",
                "fqdn_pagerank": 0.0,
                "fqdn_crawl_delay": None,
                "fqdn_url_count": 2,
            },
        ],
        urls=[
            {"url": "https://www.example.fr/abcefg", "fqdn": "www.example.fr"},
            {"url": "https://www.example.fr/hijklm", "fqdn": "www.example.fr"},
            {"url": "https://www.example.cn/abcefg", "fqdn": "www.example.cn"},
            {"url": "https://www.example.cn/hijklm", "fqdn": "www.example.cn"},
        ],
    )


def test_submit_processed_list(submit_list):
    response = datsav.submit_processed_list(
        submission_endpoint=datsav_submit_endpoint, submit_list=submit_list
    )

    assert response == 202


def test_conversion_list_to_dict(submit_list):
    asserted_dict = {
        "uuid": "12345678-90ab-cdef-0000-000000000000",
        "fqdn_count": 2,
        "fqdns": [
            {
                "fqdn": "www.example.fr",
                "tld": "fr",
                "fqdn_last_ipv4": "123.456.789.0",
                "fqdn_last_ipv6": "2001:DB8::CF5C",
                "fqdn_avg_pagerank": None,
                "fqdn_crawl_delay": 5,
                "fqdn_url_count": 2,
                "url_list": [],
            },
            {
                "fqdn": "www.example.cn",
                "tld": "cn",
                "fqdn_last_ipv4": "126.456.789.2",
                "fqdn_last_ipv6": "2001:DB8::C25C",
                "fqdn_avg_pagerank": None,
                "fqdn_crawl_delay": None,
                "fqdn_url_count": 2,
                "url_list": [],
            },
        ],
        "url_count": 4,
        "urls": [
            {
                "url": "https://www.example.fr/abcefg",
                "fqdn": "www.example.fr",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
                "url_pagerank": None,
            },
            {
                "url": "https://www.example.fr/hijklm",
                "fqdn": "www.example.fr",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
                "url_pagerank": None,
            },
            {
                "url": "https://www.example.cn/abcefg",
                "fqdn": "www.example.cn",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
                "url_pagerank": None,
            },
            {
                "url": "https://www.example.cn/hijklm",
                "fqdn": "www.example.cn",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
                "url_pagerank": None,
            },
        ],
    }
    assert datsav.convert_parsed_list_to_dict(submit_list) == asserted_dict


def test_url_to_dict():
    test_url = pyd.Url(url="https://www.example.com/abcefg", fqdn="www.example.com")
    assert datsav.url_dict(test_url) == {
        "url": "https://www.example.com/abcefg",
        "fqdn": "www.example.com",
        "url_discovery_date": None,
        "url_last_visited": None,
        "url_blacklisted": None,
        "url_bot_excluded": None,
        "url_pagerank": None,
    }
