import scrapy


class ParkspiderSpider(scrapy.Spider):
    name = "parkspider"
    allowed_domains = ["parks.ca.gov"]
    start_urls = ["https://parks.ca.gov/Find-a-Park"]

    def parse(self, response):
        pass
