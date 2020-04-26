import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def submit_processed_list(submission_endpoint, submit_list):
    submit_response = requests.post(url=submission_endpoint, json=submit_list)
    logging.info("Response: {}".format(submit_response))
    return submit_response.status_code
