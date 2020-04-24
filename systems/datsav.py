import requests
import logging

from common import settings


def submit_processed_list(submit_list):
    submit_response = requests.post(url=settings.datsav_submit_url, json=submit_list)
    logging.debug("Response Code: {}".format(submit_response.status_code))
    return submit_response.status_code
