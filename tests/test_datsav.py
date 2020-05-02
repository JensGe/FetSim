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
        urls_count=4,
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
        "urls_count": 4,
        "urls": [
            {
                "url": "https://www.example.com/abcefg",
                "fqdn": "www.example.com",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
            },
            {
                "url": "https://www.example.com/hijklm",
                "fqdn": "www.example.com",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
            },
            {
                "url": "https://www.example.de/abcefg",
                "fqdn": "www.example.de",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
            },
            {
                "url": "https://www.example.de/hijklm",
                "fqdn": "www.example.de",
                "url_discovery_date": None,
                "url_last_visited": None,
                "url_blacklisted": None,
                "url_bot_excluded": None,
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
    }
