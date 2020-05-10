from systems import websch
from common import pyd_models as pyd
from common import settings as s

import requests


def test_get_frontier_partition():

    response = websch.get_frontier_partition(uuid="12345678-90ab-cdef-0000-000000000000")

    assert isinstance(response, pyd.FrontierResponse)
    assert len(response.url_frontiers) == s.amount


def test_request_settings():
    response_dict = requests.get(s.websch_settings_endpoint).json()
    print(response_dict)
    assert isinstance(response_dict, dict)


