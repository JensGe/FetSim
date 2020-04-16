from app import websch, fetch, datsav


def main():
    while True:
        uuid = websch.init_crawler()

        frontier_list = websch.get_frontier(uuid)

        processed_list = fetch.simulate_full_fetch(frontier_list)

        datsav.submit_processed_list(processed_list)


if __name__ == "__main__":
    main()
