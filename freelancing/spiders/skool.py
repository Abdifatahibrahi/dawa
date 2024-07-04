import scrapy


class SkoolSpider(scrapy.Spider):
    name = "skool"
    allowed_domains = ["www.skool.com"]
    start_urls = ["https://www.skool.com/discovery?c=90a9d60f0fe44dbd8603d24e27f30dcd"]

    def parse(self, response):
        companies = response.css("a.styled__ChildrenLink-sc-i4j3i6-1.kbNjnr.styled__DiscoveryCardLink-sc-13ysp3k-0.eyLtsl")
        for company in companies:
            title = company.css("div.styled__TypographyWrapper-sc-m28jfn-0.eoHmvk::text").get()
            # print(titles)
            url = company.css("::attr(href)").get()
            sub_title = company.css("div.styled__DiscoveryCardDescription-sc-13ysp3k-5.dCJqtG::text").get()
            courses_type = company.css("div.styled__DiscoveryCardMeta-sc-13ysp3k-7.jjNZwk::text").get()

            
            yield {
                'titles': title, 
                'url': url,
                'subtitle': sub_title,
                'courses_type': courses_type
            }






