import random
import string
import requests
from datetime import datetime

from common import settings as s
from common import pyd_models as pyd


def random_ipv4():
    return "{}.{}.{}.{}".format(
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
    )


def random_hex():
    return random.choice(string.digits + "ABCDEF")


def random_example_ipv6():
    return "2001:DB8::{}{}{}{}".format(
        random_hex(), random_hex(), random_hex(), random_hex()
    )


def get_fqdn_from_url(url: pyd.Url):
    fqdn = url.url.split("//")[1].split("/")[0]
    return fqdn


def get_random_tld():
    return random.choice(["de", "com", "org", "se", "fr"])


def get_random_fqdn():
    return "www." + get_random_sld() + "." + get_random_tld()


def get_random_url(fqdn=None) -> pyd.Url:
    applied_fqdn = get_random_fqdn() if fqdn is None else fqdn
    return pyd.Url(
        url="http://{}/{}{}".format(
            applied_fqdn, get_random_german_text(), get_random_web_filename()
        ),
        fqdn=applied_fqdn,
        url_discovery_date=datetime.now()
    )


def get_random_existing_url(fqdn: str = None) -> pyd.Url:
    if fqdn is None:
        random_url = requests.get(s.websch_urls_endpoint, json={"amount": 1}).json()

    else:
        random_url = requests.get(
            s.websch_urls_endpoint, json={"amount": 1, "fqdn": fqdn}
        ).json()

    if random_url is None:
        random_url = get_random_url()

    return pyd.Url(
        url=random_url["url_list"][0]["url"], fqdn=random_url["url_list"][0]["fqdn"]
    )


def get_similar_url(url: pyd.Url) -> pyd.Url:
    fqdn = get_fqdn_from_url(url)
    return get_random_url(fqdn=fqdn)


def get_random_web_filename():
    file = random.choice(["/index", "/home", "/impressum", "/contact"])
    extension = random.choice([".php", ".html", ".aspx", "", "/"])
    return file + extension


def get_random_sld():
    first_char = random.choice(string.ascii_lowercase)
    random_allowed_characters = string.ascii_lowercase + "0123456789-"
    last_char = random.choice(random_allowed_characters[:-1])
    sld = (
        first_char
        + "".join(
            random.choice(random_allowed_characters)
            for _ in range(random.randint(8, 15) - 1)
        )
        + last_char
    )
    return sld


def get_random_german_text(length: int = None):
    chars = [
        "e",
        "n",
        "i",
        "s",
        "r",
        "a",
        "t",
        "d",
        "h",
        "u",
        "l",
        "c",
        "g",
        "m",
        "o",
    ]
    distribution = [
        0.1740,
        0.0978,
        0.0755,
        0.0758,
        0.0700,
        0.0651,
        0.0615,
        0.0508,
        0.0476,
        0.0435,
        0.0344,
        0.0306,
        0.0301,
        0.0253,
        0.0251,
    ]

    if length is None:
        length = random.randint(10, 16)

    return "".join(random.choices(population=chars, weights=distribution, k=length))


def random_pagerank(rank: int = random.randint(0, 14470000000)):
    # Source Springer: Inf Retrieval (2006) 9: 134 Table 1

    if rank <= 10:
        random_pagerank = random.uniform(8.0, 10.0)
    elif rank <= 100:
        random_pagerank = random.uniform(4.0, 8.0)
    elif rank <= 1000:
        random_pagerank = random.uniform(2.0, 4.0)
    elif rank <= 10000:
        random_pagerank = random.uniform(1.0, 2.0)
    elif rank <= 100000:
        random_pagerank = random.uniform(0.2, 1.0)
    elif rank <= 1000000:
        random_pagerank = random.uniform(0.01, 0.2)
    elif rank <= 10000000:
        random_pagerank = random.uniform(0.001, 0.01)
    elif rank <= 100000000:
        random_pagerank = random.uniform(0.0001, 0.001)
    elif rank <= 1000000000:
        random_pagerank = random.uniform(0.00001, 0.0001)
    else:
        random_pagerank = random.uniform(0.0, 0.00001)

    return random_pagerank


def random_crawl_delay():
    # Source: (Kolay et al. 2008, S. 1171 f.)

    crawl_delays = [None, 1, 2, 3, 5, 10, 15, 20, 30, 45, 50, 60, 120, 200, 300, 600, 1000]
    distibution = [
        0.80000,
        0.00800,
        0.00450,
        0.00450,
        0.01950,
        0.05400,
        0.00450,
        0.01900,
        0.01500,
        0.00800,
        0.00100,
        0.01800,
        0.00800,
        0.00450,
        0.00300,
        0.00150,
        0.00080,
    ]

    return random.choices(population=crawl_delays, weights=distibution)[0]
