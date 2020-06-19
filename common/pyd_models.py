from pydantic import BaseModel, HttpUrl, EmailStr

from common import enum

from uuid import UUID
from datetime import datetime
from typing import List


class BasisModel(BaseModel):
    class Config:
        orm_mode = True


# Crawler
class Crawler(BasisModel):
    uuid: UUID
    contact: EmailStr
    name: str
    reg_date: datetime
    location: str = None
    tld_preference: str = None


class CreateCrawler(BasisModel):
    contact: EmailStr
    name: str
    location: str = None
    tld_preference: str = None


class UpdateCrawler(BasisModel):
    uuid: UUID
    contact: EmailStr = None
    name: str = None
    location: str = None
    tld_preference: str = None


class DeleteCrawler(BasisModel):
    uuid: UUID


# Frontier
class FrontierRequest(BasisModel):
    crawler_uuid: UUID
    amount: int = 10
    length: int = 0
    short_term_mode: enum.STF = enum.STF.random
    long_term_mode: enum.LTF = enum.LTF.random


class Url(BasisModel):
    url: HttpUrl
    fqdn: str

    url_pagerank: float = None
    url_discovery_date: datetime = None
    url_last_visited: datetime = None
    url_blacklisted: bool = None
    url_bot_excluded: bool = None


class UrlFrontier(BasisModel):
    fqdn: str
    tld: str = None

    fqdn_last_ipv4: str = None
    fqdn_last_ipv6: str = None

    fqdn_avg_pagerank: float = None
    fqdn_crawl_delay: int = None
    fqdn_url_count: int = None

    url_list: List[Url] = []


class URLReference(BasisModel):
    url_out: str
    url_in: str
    date: datetime


class FrontierResponse(BasisModel):
    uuid: str
    short_term_mode: enum.STF = None
    long_term_mode: enum.LTF = None
    response_url: HttpUrl = None
    latest_return: datetime = None
    url_frontiers_count: int = 10
    url_count: int = 0
    url_frontiers: List[UrlFrontier] = []


# Developer Tools
class GenerateRequest(BasisModel):
    crawler_amount: int = 3
    fqdn_amount: int = 20
    min_url_amount: int = 10
    max_url_amount: int = 100
    visited_ratio: float = 1.0
    connection_amount: int = 0


class StatsResponse(BasisModel):
    crawler_amount: int
    frontier_amount: int
    url_amount: int
    url_ref_amount: int
    reserved_fqdn_amount: int


class DeleteDatabase(BasisModel):
    delete_url_refs: bool = False
    delete_crawlers: bool = False
    delete_urls: bool = False
    delete_fqdns: bool = False
    delete_reserved_fqdns: bool = False


class GetRandomUrls(BasisModel):
    amount: int = 1
    fqdn: str = None


class RandomUrls(BasisModel):
    url_list: List[Url] = []


class SimulatedParsedList(BasisModel):
    uuid: str
    fqdn_count: int
    fqdns: List[UrlFrontier]
    url_count: int
    urls: List[Url]
