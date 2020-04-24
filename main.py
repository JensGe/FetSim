from systems import fetch, websch, datsav
from common import settings
import logging



def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    i = 0
    while i < settings.iterations:
        uuid = websch.init_crawler()

        logging.info("Start Downloading Frontier")
        frontier_partition = websch.get_frontier_partition(uuid)
        logging.info("Finished Downloading Frontier")

        # Todo check if frontier_partition is empty
        logging.info("Start Simulating Fetch")
        response_url_list = fetch.simulate_full_fetch(frontier_partition)
        logging.info("Finished Simulating Fetch")

        logging.info("Start Submitting Results")
        datsav.submit_processed_list(response_url_list)
        logging.info("Finished Submitting Results")

        i += 1

    logging.info("Terminating Program")


if __name__ == "__main__":
    main()
