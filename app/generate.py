import random
import string


def get_random_tld():
    return random.choice(["de", "com", "org", "se", "fr"])


def get_random_fqdn():
    return "www." + get_random_sld() + "." + get_random_tld()


def get_random_url():
    return "http://{}/{}{}".format(
        get_random_fqdn(), get_random_german_text(), get_random_web_filename()
    )


def get_similar_url(url):
    pass


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
