import requests
from common import settings


def submit_processed_list(submit_list):
    submit_response = requests.post(url=settings.datsav_submit_url, json=submit_list)
    print(submit_response)
    return submit_response.status_code
