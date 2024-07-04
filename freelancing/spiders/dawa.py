import scrapy


class DawaSpider(scrapy.Spider):
    name = "dawa"
    allowed_domains = ["www.goodlife.co.ke"]
    start_urls = ["https://www.goodlife.co.ke/product-category/health-care/"]
    custom_settings = {
    'ROBOTSTXT_OBEY': False
    }

    

    def parse(self, response):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        products_list = response.css('li.store-selected.add-to-wishlist-before_add_to_cart')

        for product in products_list:
            yield {
                'name': product.css('h2.woocommerce-loop-product__title::text').get(),
                'old_price': product.css('del .woocommerce-Price-amount.amount bdi::text').get(),
                'new_price': product.css('ins .woocommerce-Price-amount.amount bdi::text').get(),
                'image_url': product.css('img::attr(src)').get(),
                'product_url': product.css('a::attr(href)').get(),
                'discount': product.css('span.onsale::text').get(),
                'sku': product.css('a.add_to_cart_button::attr(data-product_sku)').get(),
                'stock_level': product.css('span.gtm4wp_productdata::attr(data-gtm4wp_product_data)').re_first(r'"stocklevel":(\d+)'),
            }
        # next_page = response.css('div.lmp_load_more_button a.lmp_button::attr(href)').get()
        next_page = response.xpath('//div[@class="lmp_load_more_button"]//a[@class="lmp_button"]/@href').get()
        print(next_page)
        print("************\n\n\n\n\n\n\n\n\n")
        if next_page is not None:
            # Make a request to the next page
            yield scrapy.Request(next_page,  headers={'User-Agent': user_agent}, callback=self.parse)

    # start_urls = ['https://www.goodlife.co.ke/shop/page/1/']  # Start from the first page

    # custom_settings = {
    #     'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    #     'ROBOTSTXT_OBEY': False
    # }

    # def parse(self, response):
    #     for product in response.css('li.store-selected.add-to-wishlist-before_add_to_cart'):
    #         yield {
    #             'name': product.css('h2.woocommerce-loop-product__title::text').get(),
    #             'old_price': product.css('del .woocommerce-Price-amount.amount bdi::text').get(),
    #             'new_price': product.css('ins .woocommerce-Price-amount.amount bdi::text').get(),
    #             'image_url': product.css('img::attr(src)').get(),
    #             'product_url': product.css('a::attr(href)').get(),
    #             'discount': product.css('span.onsale::text').get(),
    #             'sku': product.css('a.add_to_cart_button::attr(data-product_sku)').get(),
    #             'stock_level': product.css('span.gtm4wp_productdata::attr(data-gtm4wp_product_data)').re_first(r'"stocklevel":(\d+)'),
    #         }


import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DawaSpider(scrapy.Spider):
    name = "dawa"
    allowed_domains = ["www.goodlife.co.ke"]
    start_urls = ["https://www.goodlife.co.ke/shop/page/1/"]
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, *args, **kwargs):
        super(DawaSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # Wait for JavaScript to load

        selenium_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        products_list = selenium_response.css('li.store-selected.add-to-wishlist-before_add_to_cart')

        for product in products_list:
            yield {
                'name': product.css('h2.woocommerce-loop-product__title::text').get(),
                'old_price': product.css('del .woocommerce-Price-amount.amount bdi::text').get(),
                'new_price': product.css('ins .woocommerce-Price-amount.amount bdi::text').get(),
                'image_url': product.css('img::attr(src)').get(),
                'product_url': product.css('a::attr(href)').get(),
                'discount': product.css('span.onsale::text').get(),
                'sku': product.css('a.add_to_cart_button::attr(data-product_sku)').get(),
                'stock_level': product.css('span.gtm4wp_productdata::attr(data-gtm4wp_product_data)').re_first(r'"stocklevel":(\d+)'),
            }

        # Get the next page URL using Selenium 4
        # try:
        #     next_page_element = self.driver.find_element(By.CSS_SELECTOR, 'div.lmp_load_more_button a.lmp_button')
        #     next_page = next_page_element.get_attribute('href')
        # except Exception as e:
        #     next_page = None
        #     self.logger.error(f"Failed to get next page: {e}")
        try:
    # Wait up to 10 seconds until the element is found
            next_page = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.lmp_load_more_button a.lmp_button"))
            )
        finally:
            self.driver.quit()

        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def closed(self, reason):
        self.driver.quit()





import scrapy
from scrapy.http import HtmlResponse
from multiprocessing import Process, Pipe
from playwright.sync_api import sync_playwright

class DawaSpider(scrapy.Spider):
    name = "dawa"
    allowed_domains = ["www.goodlife.co.ke"]
    start_urls = ["https://www.goodlife.co.ke/shop/page/1/"]
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, *args, **kwargs):
        super(DawaSpider, self).__init__(*args, **kwargs)

    def fetch_page(self, url, conn):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector('div.lmp_load_more_button a.lmp_button')
            content = page.content()
            conn.send(content)
            conn.close()
            browser.close()

    def parse(self, response):
        parent_conn, child_conn = Pipe()
        process = Process(target=self.fetch_page, args=(response.url, child_conn))
        process.start()
        process.join()
        content = parent_conn.recv()

        selenium_response = HtmlResponse(url=response.url, body=content, encoding='utf-8')

        products_list = selenium_response.css('li.store-selected.add-to-wishlist-before_add_to_cart')

        for product in products_list:
            yield {
                'name': product.css('h2.woocommerce-loop-product__title::text').get(),
                'old_price': product.css('del .woocommerce-Price-amount.amount bdi::text').get(),
                'new_price': product.css('ins .woocommerce-Price-amount.amount bdi::text').get(),
                'image_url': product.css('img::attr(src)').get(),
                'product_url': product.css('a::attr(href)').get(),
                'discount': product.css('span.onsale::text').get(),
                'sku': product.css('a.add_to_cart_button::attr(data-product_sku)').get(),
                'stock_level': product.css('span.gtm4wp_productdata::attr(data-gtm4wp_product_data)').re_first(r'"stocklevel":(\d+)'),
            }

        # Get the next page URL using Playwright
        try:
            next_page_element = selenium_response.css('div.lmp_load_more_button a.lmp_button::attr(href)').get()
            if next_page_element is not None:
                yield scrapy.Request(url=next_page_element, callback=self.parse)
        except Exception as e:
            self.logger.error(f"Failed to get next page: {e}")
