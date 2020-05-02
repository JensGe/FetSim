from common import generate
from common import pyd_models as pyd

# def test_generate_fqdn_from_url():
#     url = "http://www.example.com/xyz/index.html"
#     asserted_fqdn = "www.example.com"
#
#     assert generate.get_fqdn_from_url(url) == asserted_fqdn
#
#
# def test_get_similar_url():
#     url = "http://www.example.com/msdf/index.php"
#     sim_url = generate.get_similar_url(url)
#
#     assert url.split("//")[1].split("/")[0] == sim_url.split("//")[1].split("/")[0]


def test_get_random_existing_url():
    single_random_existing_url = generate.get_random_existing_url()
    assert isinstance(single_random_existing_url, pyd.Url)
