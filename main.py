import sys

from systems import fetch, websch, datsav
from common import settings as s
from common import local
import s3_upload

import logging
import time
import os


def main():
    i = 0
    websch.init_fetcher_settings()

    uuid = websch.init_fetcher()

    if not os.path.exists(s.log_dir):
        os.makedirs(s.log_dir)

    start_time = time.strftime("%Y-%m-%d", time.gmtime())
    logging.basicConfig(
        level=s.logging_level,
        format="%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        # stream=sys.stderr
        filename="{}/{} {}.log".format(s.log_dir, start_time, uuid),
        filemode="a",
    )

    while i < local.load_settings("iterations"):
        it = {"begin": time.time()}
        frontier_response = websch.get_frontier_partition(uuid)
        it["frontier_loaded"] = time.time()

        logging.info(
            "Frontier Stats: {} FQDNs, {} URLs".format(
                frontier_response.url_frontiers_count,
                sum(
                    [
                        url_frontier.fqdn_url_count
                        for url_frontier in frontier_response.url_frontiers
                    ]
                ),
            )
        )
        for url_frontier in frontier_response.url_frontiers:
            logging.debug(
                "Frontier {} URL Amount: {}".format(
                    url_frontier.fqdn, url_frontier.fqdn_url_count
                )
            )

        it["fetch_begin"] = time.time()
        simulated_urls = fetch.simulate_full_fetch(frontier_response)
        it["fetch_finished"] = time.time()

        logging.info(
            "Response Stats: {} FQDNs, {} URLs".format(
                simulated_urls.fqdn_count, simulated_urls.url_count
            )
        )

        it["submission_begin"] = time.time()
        datsav.submit_processed_list(
            submission_endpoint=frontier_response.response_url,
            submit_list=simulated_urls,
        )
        it["submission_finished"] = time.time()

        logging.info(
            "Iteration Stats: Load ({} ms), Fetch ({} ms), Submit ({} ms).".format(
                round((it["frontier_loaded"] - it["begin"]) * 1000, 3),
                round((it["fetch_finished"] - it["fetch_begin"]) * 1000, 3),
                round((it["submission_finished"] - it["submission_begin"]) * 1000, 3),
            )
        )

        i += 1

    s3_upload.upload()
    logging.info("Terminating Program")


if __name__ == "__main__":
    main()
