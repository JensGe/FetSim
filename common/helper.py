import string
import random


def generate_random_crawler_name():
    chars = string.ascii_lowercase + "1234567890-_"
    return "".join(random.choice(chars) for _ in range(15)).title()
