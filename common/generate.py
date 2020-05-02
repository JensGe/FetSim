import random
import string
import requests
from common import settings as s
from common import pyd_models as pyd


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
    )


def get_random_existing_url(fqdn: str = None) -> pyd.Url:

    if fqdn is None:
        random_url = requests.get(s.websch_urls_endpoint, json={"amount": 1}).json()

    else:
        random_url = requests.get(
            s.websch_urls_endpoint, json={"amount": 1, "fqdn": fqdn}
        ).json()

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
