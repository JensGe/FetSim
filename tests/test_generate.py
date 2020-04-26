from common import generate


def test_generate_fqdn_from_url():
    url = "http://www.example.com/xyz/index.html"
    asserted_fqdn = "www.example.com"

    assert generate.get_fqdn_from_url(url) == asserted_fqdn


def test_get_similar_url():
    url = "http://www.example.com/msdf/index.php"
    sim_url = generate.get_similar_url(url)

    assert url.split("//")[1].split("/")[0] == sim_url.split("//")[1].split("/")[0]



