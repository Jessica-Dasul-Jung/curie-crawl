# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
import time

class LfCrawlSpider(scrapy.Spider):
    name = 'lf_crawl'
    allowed_domains = ['www.lfmall.co.kr/p2/products/category?id=80607&etag1=003_A002_E226&etag2=0&etag3=4&etag4=80468']
    start_urls = ['http://www.lfmall.co.kr/p2/products/category?id=80607&etag1=003_A002_E226&etag2=0&etag3=4&etag4=80468']
                    
    def parse_item(self, response):
        info = response.xpath("//*/table[contains(@class,'tbl-y mb10')]/tr/td/text()").extract()
        prod_name = response.xpath("//*[@class='prod-name']/text()").extract()  

        clothing_type = response.meta['분류']
        component = info[0].strip() # 소재
        # color = info[1].strip() # 색상
        # company = info[3].strip() # 제조사
        # method = info[5].strip() # 세탁법
        # yield {'제품 이름': prod_name, '분류': clothing_type, '제품 소재': component, '색상': color, '제조사': company, '세탁법': method}
        yield {'제품 이름': prod_name, '분류': clothing_type, '제품 소재': component}

    def parse(self, response):
        clothing_type = "아우터"
        page_driver = webdriver.Chrome('C:\\Users\\Jessi\\Documents\\chromedriver_win32\\chromedriver.exe')

        index = 1
        try:
            while (True):
                try:
                	# receive original page again
                    page_driver.get("http://www.lfmall.co.kr/p2/products/category?id=80607&etag1=003_A002_E226&etag2=0&etag3=4&etag4=80468")
                    page_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                    # configure item path
                    item_path = "//*[@id='productUl']/li["
                    item_path = item_path + str(index) + "]/a"
                    page_driver.find_element_by_xpath(item_path).click()
                    item_url = page_driver.current_url
                    yield scrapy.Request(item_url, callback=self.parse_item, meta={"분류": clothing_type }, dont_filter=True)
                    index = index + 1
                except UnexpectedAlertPresentException:
                    index = index + 1
                    alert = page_driver.switch_to.alert
                    alert.accept()
                    page_driver = webdriver.Chrome('C:\\Users\\Jessi\\Documents\\chromedriver_win32\\chromedriver.exe')           
        except NoSuchElementException:
            self.logger.info('No more items to load.')
            page_driver.quit()
        pass
