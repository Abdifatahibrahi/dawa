import scrapy


class TouristSpider(scrapy.Spider):
    name = "tourist"
    allowed_domains = ["bit.ly"]
    start_urls = ["http://bit.ly/3XnyEIm"]

    def parse(self, response):
        pass
