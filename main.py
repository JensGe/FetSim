from systems import fetch, websch, datsav
from common import settings
import logging


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    i = 0
    while i < settings.iterations:
        uuid = websch.init_crawler()

        logging.info("### Start Downloading Frontier")
        frontier_partition = websch.get_frontier_partition(uuid)

        logging.info(
            "### Frontiers Downloaded: {}".format(
                str(len(frontier_partition["url_frontiers"]))
            )
        )
        # random_urls = websch.get_random_urls(
        #     frontier_partition["urls_count"]
        #     * settings.max_links_per_page
        #     / settings.outgoing_link_ratio
        # )
        # logging.info("### Random Urls Downloaded: {}".format(str(len(random_urls))))

        logging.info("### Start Simulating Fetch")
        response_url_list = fetch.simulate_full_fetch(frontier_partition)
        logging.info("#   Response Url List: {}".format(str(response_url_list)))
        logging.info("### Finished Simulating Fetch")

        logging.info("### Start Submitting Results")
        datsav.submit_processed_list(
            submission_endpoint=frontier_partition["response_url"],
            submit_list=response_url_list,
        )
        logging.info("### Finished Submitting Results")

        i += 1

    logging.info("## Terminating Program")


if __name__ == "__main__":
    main()
