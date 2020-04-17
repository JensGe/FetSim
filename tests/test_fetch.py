from systems import fetch


def test_simulate_parse_url():

    url = {
        "url": "http://www.abc.de/html/index",
        "fqdn": "www.abc.de",
        "url_discovery_date": None,
        "url_last_visited": "2020-01-01T06:00:00",
        "url_blacklisted": False,
        "url_bot_excluded": False,
    }

    fetch_list = fetch.simulate_parse_url(url)
    assert fetch_list[0]["url_discovery_date"] is None
    assert fetch_list[0]["url_last_visited"] == "2020-01-01T06:00:00"
    assert len(fetch_list) > 2
    assert len(fetch_list) < 13


def test_simulate_fetch():
    frontier_list = {
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

    processed_list = fetch.simulate_full_fetch(frontier_list)

    assert len(processed_list["url_frontiers"]) >= 1
    assert len(processed_list["url_frontiers"][0]["url_list"]) >= 1


def test_use():
    frontier_list = {
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

    processed_data = fetch.simulate_full_fetch(frontier_list)
    assert frontier_list == processed_data