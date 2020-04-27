import random


# Endpoints
websch_crawler_url = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/crawlers"
)
websch_frontier_url = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/frontiers"
)
websch_urls = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/urls"
)
datsav_submit = "http://ec2-18-195-144-15.eu-central-1.compute.amazonaws.com/submit"

# Files
uuid_file = "uuid.dat"


# Fetching Simulator
max_links_per_page = 10
min_links_per_page = 3
remaining_link_ratio = 0.95                         # Check Literature
outgoing_link_ratio = 1 - remaining_link_ratio

parallel_processes = 10
crawling_speed = 10.0

iterations = 10
amount = 5
