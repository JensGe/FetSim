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

    while i < local.load_settings("iterations"):
        uuid = websch.init_crawler()

        if not os.path.exists(s.log_dir):
            os.makedirs(s.log_dir)

        start_time = time.strftime("%Y-%m-%d", time.gmtime())
        logging.basicConfig(
            level=s.logging_level,
            format="%(asctime)s.%(msecs)09d %(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename="{}/{} {}.log".format(s.log_dir, start_time, uuid),
            filemode="a",
        )

        frontier_response = websch.get_frontier_partition(uuid)
        logging.info(
            "Frontier Stats: FQDN Amount: {}".format(
                frontier_response.url_frontiers_count
            )
        )
        for url_frontier in frontier_response.url_frontiers:
            logging.info(
                "Frontier {} URL Amount: {}".format(
                    url_frontier.fqdn, url_frontier.fqdn_url_count
                )
            )

        similated_urls = fetch.simulate_full_fetch(frontier_response)
        logging.info("Response Url List Stats:")
        logging.info(
            "  FQDNS: {}, URLS: {}".format(
                similated_urls.fqdn_count, similated_urls.url_count
            )
        )

        datsav.submit_processed_list(
            submission_endpoint=frontier_response.response_url,
            submit_list=similated_urls,
        )
        logging.info("Submission Done")

        i += 1

    s3_upload.upload()
    logging.info("Terminating Program")


if __name__ == "__main__":
    main()
