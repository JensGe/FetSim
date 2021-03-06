from systems import fetch, websch, datsav
from common import settings as s
from common import local
from time import sleep
import s3_upload

import logging
import time
import os


def main():
    i = 0
    websch.init_fetcher_settings()

    uuid = websch.init_fetcher()
    ec2_instance_id = websch.get_instance_id()

    if not os.path.exists(s.log_dir):
        os.makedirs(s.log_dir)

    logger = logging.getLogger("FETSIM")
    logger.setLevel(local.load_setting("logging_mode"))

    fh = logging.FileHandler("{}/{}.log".format(s.log_dir, ec2_instance_id))
    fh.setLevel(local.load_setting("logging_mode"))

    ch = logging.StreamHandler()
    ch.setLevel(local.load_setting("logging_mode"))

    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Fetcher Settings: {}".format(local.load_all_settings()))

    while i < local.load_setting("iterations"):
        times = {"begin": time.time()}
        frontier_response = websch.get_frontier_partition(uuid)
        times["frontier_loaded"] = time.time()

        logger.info(
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
            logger.debug(
                "Frontier {} URL Amount: {}".format(
                    url_frontier.fqdn, url_frontier.fqdn_url_count
                )
            )

        times["fetch_begin"] = time.time()
        cpu_time_before = time.process_time()
        simulated_urls = fetch.simulate_full_fetch(frontier_response)
        times["fetch_finished"] = time.time()
        cpu_time = time.process_time() - cpu_time_before

        logger.info(
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

        logger.info(
            "Iteration Stats: "
            "iter_load_duration: {} s, "
            "iter_fetch_start: {}, "
            "iter_fetch_duration: {} s, "
            "iter_fetch_cpu_time: {} s, "
            "iter_submit_duration: {} s".format(
                round((times["frontier_loaded"] - times["begin"]), 3),
                time.strftime(
                    "%Y-%m-%d %H:%M:%S.{}{}".format(
                        int(times["fetch_begin"] * 1000) % 1000, "000"
                    ),
                    time.gmtime(times["fetch_begin"]),
                ),
                round((times["fetch_finished"] - times["fetch_begin"]), 3),
                round(cpu_time, 3),
                round(
                    (times["submission_finished"] - times["submission_begin"]), 3
                ),
            )
        )

        time.sleep(5)
        db_stats = websch.get_db_stats()
        logger.info(
            "DB Stats: "
            "db_frontier_amount: {}, "
            "db_url_amount: {}, "
            "db_avg_freshness: {}, "
            "db_visited_ratio: {}, "
            "db_fqdn_hash_range: {} %".format(
                db_stats["frontier_amount"],
                db_stats["url_amount"],
                db_stats["avg_freshness"],
                db_stats["visited_ratio"],
                db_stats["fqdn_hash_range"],
            )
        )

        i += 1

    s3_upload.upload()
    logger.info("Terminating Program")


def create_fetcher_over_time():
    for j in range(200):
        for i in range(15):
            print("-", end='')
            sleep(1)
        print("")
        websch.create_websch_fetcher()
        print("fetcher_{}".format(j))


if __name__ == "__main__":
    main()
    # create_fetcher_over_time()
