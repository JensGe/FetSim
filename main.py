from systems import fetch, websch, datsav
from common import settings as s
import s3_upload

import logging
import time
import os


def main():

    i = 0

    while i < s.iterations:
        uuid = websch.init_crawler()

        if not os.path.exists(s.log_dir):
            os.makedirs(s.log_dir)
        start_time = time.strftime("%Y-%m-%d", time.gmtime())
        logging.basicConfig(
            filename="{}/{} {}.log".format(s.log_dir, start_time, uuid),
            filemode="a",
            level=logging.INFO,
            format="%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        frontier_response = websch.get_frontier_partition(uuid)
        logging.info(
            "Frontier Stats: FQDN Amount: {}".format(
                frontier_response.url_frontiers_count)
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

