import requests


def submit_processed_list(submit_list):
    submit_response = requests.post(submit_list.json())

    return submit_response.status_code
