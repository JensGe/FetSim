from systems import fetch
from common import pyd_models as pyd
from common import settings as s
from common.pyd_models import HttpUrl

import pytest
from typing import List


@pytest.fixture
def example_frontier_partition():
    return {
        "uuid": "12345678-90ab-cdef-0000-000000000000",
        "url_frontiers": [
            {
                "fqdn": "www.abc.de",
                "tld": "de",
                "fqdn_last_ipv4": "123.456.78.91",
                "fqdn_last_ipv6": "2001:DB8::1234",
                "fqdn_pagerank": 0.00001,
                "fqdn_crawl_delay": 5,
                "fqdn_url_count": 4,
                "url_list": [
                    {
                        "url": "http://www.abc.de/html/index",
                        "fqdn": "www.abc.de",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T06:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                    {
                        "url": "http://www.abc.de/html/contact",
                        "fqdn": "www.abc.de",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T07:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                    {
                        "url": "http://www.abc.de/html/start.html",
                        "fqdn": "www.abc.de",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T08:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                    {
                        "url": "http://www.abc.de/html/people.html",
                        "fqdn": "www.abc.de",
                        "url_discovery_date": "2020-04-10T08:55:58",
                        "url_last_visited": None,
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                ],
            },
            {
                "fqdn": "www.bac.com",
                "tld": "com",
                "fqdn_last_ipv4": "123.45.678.90",
                "fqdn_last_ipv6": "2001:DB8::2345",
                "fqdn_pagerank": 0.00002,
                "fqdn_crawl_delay": 5,
                "fqdn_url_count": 2,
                "url_list": [
                    {
                        "url": "http://www.bac.com/html/mission",
                        "fqdn": "www.bac.com",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T10:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                    {
                        "url": "http://www.bac.com/blue",
                        "fqdn": "www.bac.com",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T11:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                ],
            },
            {
                "fqdn": "www.cba.com",
                "tld": "com",
                "fqdn_last_ipv4": "123.45.678.90",
                "fqdn_last_ipv6": "2001:DB8::2345",
                "fqdn_pagerank": 0.00002,
                "fqdn_crawl_delay": 5,
                "fqdn_url_count": 2,
                "url_list": [
                    {
                        "url": "http://www.abc.com/html/index",
                        "fqdn": "www.abc.com",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T10:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                    {
                        "url": "http://www.abc.com/html/contact",
                        "fqdn": "www.abc.com",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T11:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                ],
            },
        ],
    }


def test_simulate_parse_url():
    url = pyd.Url(
        url="http://www.abc.de/html/index",
        fqdn="www.abc.de",
        url_discovery_date=None,
        url_last_visited="2020-01-01T06:00:00",
        rl_blacklisted=False,
        url_bot_excluded=False,
    )

    parsed_list = fetch.simulate_parse_url(url)
    assert isinstance(parsed_list[0].url, HttpUrl)
    assert parsed_list[0].url_discovery_date is None
    assert parsed_list[0].url_last_visited != "2020-01-01T06:00:00"
    assert isinstance(parsed_list[1].url, HttpUrl)


def test_simulate_fetch():
    frontier_partition = {
        "uuid": "12345678-90ab-cdef-0000-000000000000",
        "response_url": "http://www.example.com/submit",
        "latest_return": "2020-10-10T23:00:00.000000",
        "url_frontiers_count": 1,
        "urls_count": 1,
        "url_frontiers": [
            {
                "fqdn": "www.abc.de",
                "tld": "de",
                "fqdn_last_ipv4": "123.456.78.90",
                "fqdn_last_ipv6": "2001:DB8::1234",
                "fqdn_pagerank": 0.00001,
                "fqdn_crawl_delay": 5,
                "fqdn_url_count": 1,
                "url_list": [
                    {
                        "url": "http://www.abc.de/html/index",
                        "fqdn": "www.abc.de",
                        "url_discovery_date": None,
                        "url_last_visited": "2020-01-01T06:00:00",
                        "url_blacklisted": False,
                        "url_bot_excluded": False,
                    },
                ],
            },
        ],
    }

    processed_list = fetch.simulate_full_fetch(frontier_partition)

    assert processed_list["uuid"] == frontier_partition["uuid"]
    assert isinstance(processed_list["urls_count"], int)

    for i in range(len(processed_list["urls"])):
        assert isinstance(processed_list["urls"][i]["url"], str)
        assert (
            isinstance(processed_list["urls"][i]["url_discovery_date"], str)
            or processed_list["urls"][i]["url_discovery_date"] is None
        )
        assert (
            isinstance(processed_list["urls"][i]["url_last_visited"], str)
            or processed_list["urls"][i]["url_last_visited"] is None
        )
        assert isinstance(
            processed_list["urls"][i]["url_discovery_date"], str
        ) or isinstance(processed_list["urls"][i]["url_last_visited"], str)


def test_simulate_short_term_fetch():
    short_term_frontier = pyd.UrlFrontier(
        fqdn="www.abc.de",
        tld="de",
        fqdn_last_ipv4="123.456.78.91",
        fqdn_last_ipv6="2001:DB8::1234",
        fqdn_pagerank=0.00001,
        fqdn_crawl_delay=5,
        fqdn_url_count=2,
        url_list=[
            pyd.Url(
                url="http://www.abc.de/html/index",
                fqdn="www.abc.de",
                url_discovery_date=None,
                url_last_visited="2020-01-01T06:00:00",
                url_blacklisted=False,
                url_bot_excluded=False,
            ),
            pyd.Url(
                url="http://www.abc.de/html/contact",
                fqdn="www.abc.de",
                url_discovery_date=None,
                url_last_visited="2020-01-01T07:00:00",
                url_blacklisted=False,
                url_bot_excluded=False,
            ),
        ],
    )

    short_term_fetch_result = fetch.simulate_short_term_fetch(short_term_frontier)

    assert isinstance(short_term_fetch_result, List)
    for i in range(len(short_term_fetch_result)):
        assert isinstance(short_term_fetch_result[i], pyd.Url)
        assert isinstance(short_term_fetch_result[i].url, HttpUrl)


def test_condition_functions():
    intern = s.internal_vs_external_threshold / 2
    extern = (
        1 - s.internal_vs_external_threshold
    ) / 2 + s.internal_vs_external_threshold
    new = s.new_vs_existing_threshold / 2
    existing = (1 - s.new_vs_existing_threshold) / 2 + s.new_vs_existing_threshold

    assert fetch.new_internal_cond(intern, new) is True
    assert fetch.existing_internal_cond(intern, existing) is True
    assert fetch.new_external_cond(extern, new) is True
    assert fetch.existing_external_cond(extern, existing) is True


def test_generate_existing_new_url():
    new_url = fetch.generate_existing_url()
    assert isinstance(new_url, pyd.Url)


def test_generate_existing_existing_url():
    fqdn = "www.z1wp7ztzkp6lxmc.cn"

    existing_url = fetch.generate_existing_url(fqdn=fqdn)

    assert isinstance(existing_url, pyd.Url)
    assert existing_url.fqdn == fqdn
