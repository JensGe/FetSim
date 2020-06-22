import logging

# Endpoints
websch_crawler_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/fetchers/"
)
websch_frontier_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/frontiers/"
)
websch_urls_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/urls/"
)
websch_settings_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/settings/"
)
websch_stats_endpoint = (
    "http://ec2-18-185-96-23.eu-central-1.compute.amazonaws.com/stats/"
)



# Files & Folders
uuid_file = "uuid.dat"
settings_file = "settings.dat"
log_dir = "logs"


# Fetching Simulator
min_links_per_page = 2                      # Check Literature
max_links_per_page = 5

internal_vs_external_threshold = 0.85       # Check Literature
new_vs_existing_threshold = 0.35


parallel_processes = 10
crawling_speed = 10.0
default_crawl_delay = 10


iterations = 100
amount = 30
length = 0
