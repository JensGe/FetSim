from systems import fetch, websch, datsav
from common import settings
import logging


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    i = 0

    while i < settings.iterations:
        uuid = websch.init_crawler()

        logging.info("### Start Downloading Frontier")
        frontier_response = websch.get_frontier_partition(uuid)

        logging.info(
            "### Frontiers Downloaded: {}, {}".format(
                str(len(frontier_response.url_frontiers)),
                [
                    (url_frontier.fqdn, len(url_frontier.url_list))
                    for url_frontier in frontier_response.url_frontiers
                ],
            )
        )

        logging.info("### Start Simulating Fetch")
        similated_urls = fetch.simulate_full_fetch(frontier_response)
        logging.info("#   Response Url List: {}".format(str(similated_urls)))
        logging.info("### Finished Simulating Fetch")

        logging.info("### Start Submitting Results")
        datsav.submit_processed_list(
            submission_endpoint=frontier_response.response_url,
            submit_list=similated_urls,
        )
        logging.info("### Finished Submitting Results")

        i += 1

    logging.info("## Terminating Program")


if __name__ == "__main__":
    main()
