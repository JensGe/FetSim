import random


# Endpoints
websch_crawler_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/crawlers"
)
websch_frontier_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/frontiers"
)
websch_urls_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/urls"
)

# Files
uuid_file = "uuid.dat"


# Fetching Simulator
max_links_per_page = 10
min_links_per_page = 10

internal_vs_external_threshold = 0.5       # Check Literature
new_vs_existing_threshold = 0.2


parallel_processes = 10
crawling_speed = 10.0


iterations = 1
amount = 2
