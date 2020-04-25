import random


# Endpoints
websch_crawler_url = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/crawlers"
)
websch_frontier_url = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/frontiers"
)



# Files
uuid_file = "uuid.dat"


# Fetching Simulator

url_discoveries = random.randint(2, 3)
internal_discovery_ratio = 0.0

parallel_processes = 10
crawling_speed = 10.0

iterations = 2
