from systems import datsav
import pytest


@pytest.fixture
def submit_list():
    return {
        "uuid": "12345678-90ab-cdef-0000-000000000000",
        "urls_count": 4,
        "urls": [
            {"url": "https://www.example.com/abcefg", "fqdn": "www.example.com"},
            {"url": "https://www.example.com/hijklm", "fqdn": "www.example.com"},
            {"url": "https://www.example.de/abcefg", "fqdn": "www.example.de"},
            {"url": "https://www.example.de/hijklm", "fqdn": "www.example.de"},
        ],
    }


def test_submit_processed_list(submit_list):
    response = datsav.submit_processed_list(submit_list)

    assert response == 202
