import requests


from app import settings, local, helper


def websch_uuid_exists():
    uuid = local.get_pickle_uuid()
    frontier_response = requests.patch(
        settings.websch_crawler_url, {"crawler_uuid": uuid}
    )
    if frontier_response.status_code == 200:
        return True
    else:
        return False


def get_frontier(uuid):
    frontier_request_dict = {
        "crawler_uuid": uuid,
    }

    frontier_response = requests.post(
        settings.websch_frontier_url, json=frontier_request_dict,
    )

    frontier_response = frontier_response.json()
    return frontier_response


def create_websch_crawler():
    crawler_name = helper.generate_random_crawler_name()
    create_crawler_dict = {
        "contact": "admin@fetsim.de",
        "name": "Demo-Fetcher #{}".format(crawler_name),
        "location": "Germany",
        "tld_preference": "de",
    }

    new_crawler_response = requests.post(
        settings.websch_crawler_url, json=create_crawler_dict,
    )

    new_crawler_json = new_crawler_response.json()

    local.save_uuid_to_pickle(new_crawler_json["uuid"])


def init_crawler():
    if not local.file_exists("uuid.dat"):
        create_websch_crawler()

    if not websch_uuid_exists():
        create_websch_crawler()

    return local.get_pickle_uuid()
