# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException

class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['www.coupang.com/np/search?q=%EA%B0%80%EC%A3%BD+%ED%81%B4%EB%A6%AC%EB%84%88&brand=&offerCondition=NEW&filter=&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=auto&component=115573&rating=0&sorter=scoreDesc&listSize=36']
    start_urls = ['https://www.coupang.com/np/search?q=%EA%B0%80%EC%A3%BD+%ED%81%B4%EB%A6%AC%EB%84%88&brand=&offerCondition=NEW&filter=&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=auto&component=115573&rating=0&sorter=scoreDesc&listSize=36']

    def parse_page(self, response):
        item_arr = response.xpath("//*[@class='name']/text()").extract()
        img_arr1 = response.xpath("//*[@class='image']/img/@src").extract()
        img_arr2 = response.xpath("//*/img[@class='search-product-wrap-img']/@data-img-src").extract()
        img_arr1 = img_arr1[0:8]
        img_arr = img_arr1 + img_arr2        
        size = len(item_arr)
        for i in range (0, size):
            item_name = item_arr[i]
            img_src = response.urljoin(img_arr[i])
            yield {'대분류': "가죽클리너", '중분류': "-", '이름': item_name, '이미지': img_src}

    def parse(self, response):
        page_driver = webdriver.Chrome('C:\\Users\\Jessi\\Documents\\chromedriver_win32\\chromedriver.exe')
        page_driver.get("https://www.coupang.com/np/search?q=%EA%B0%80%EC%A3%BD+%ED%81%B4%EB%A6%AC%EB%84%88&brand=&offerCondition=NEW&filter=&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=auto&component=115573&rating=0&sorter=scoreDesc&listSize=36")
        cont = True
        while (cont):
            try:
                page_url = page_driver.current_url
                yield scrapy.Request(page_url, callback=self.parse_page, dont_filter=True)
                page_driver.find_element_by_xpath("//*[@class='btn-next']").click()
                page_driver.implicitly_wait(3)
                pass                
            except WebDriverException:
                self.logger.info('No more items to load.')
                page_driver.quit()
                cont = False
        pass
