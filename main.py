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

    logging.basicConfig(
        level=local.load_settings("logging_mode"),
        format="%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="{}/{}.log".format(s.log_dir, uuid),
        filemode="a",
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().setLevel(local.load_settings("logging_mode"))

    while i < local.load_settings("iterations"):
        times = {"begin": time.time()}
        frontier_response = websch.get_frontier_partition(uuid)
        times["frontier_loaded"] = time.time()

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

        times["fetch_begin"] = time.time()
        time.process_time()
        simulated_urls = fetch.simulate_full_fetch(frontier_response)
        times["fetch_finished"] = time.time()
        cpu_time = time.process_time()

        logging.info(
            "Response Stats: {} FQDNs, {} URLs".format(
                simulated_urls.fqdn_count, simulated_urls.url_count
            )
        )

        times["submission_begin"] = time.time()
        datsav.submit_processed_list(
            submission_endpoint=frontier_response.response_url,
            submit_list=simulated_urls,
        )
        times["submission_finished"] = time.time()

        logging.info(
            "Iteration Stats: "
            "Load ({} ms), Fetch ({} s), Fetch CPU ({} s), Submit ({} ms).".format(
                round((times["frontier_loaded"] - times["begin"]) * 1000, 3),
                round((times["fetch_finished"] - times["fetch_begin"]), 3),
                round(cpu_time, 3),
                round(
                    (times["submission_finished"] - times["submission_begin"]) * 1000, 3
                ),
            )
        )

        i += 1

    s3_upload.upload()
    logging.info("Terminating Program")


if __name__ == "__main__":
    main()
