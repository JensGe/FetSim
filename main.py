from systems import fetch, websch, datsav


def main():
    uuid = websch.init_crawler()

    print("Get Frontier Partition ...")
    frontier_partition = websch.get_frontier_partition(uuid)

    print("Simulate Fetching ...")
    response_url_list = fetch.simulate_full_fetch(frontier_partition)

    print("Submit Fetching Results...")
    datsav.submit_processed_list(response_url_list)


if __name__ == "__main__":
    main()
