# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


class LprodSpider(scrapy.Spider):
    name = 'lprod'
    allowed_domains = ['http://www.lotte.com/display/viewDispShop.lotte?search_flag=&sub_search_flag=Y&disp_no=5414477&allCheckDispNo=&allCheckBrndNo=&lst_sort_cd=10&rowsPerPage=180&disp_type=image&reloadYn=Y&pageIdx=1&prevPageIdx=0&slct_dpml_no=2&SORT_FIELD=&allViewYn=Y&smartpickBranch=&cpcadCnt=0&first_goods_no=0&last_goods_no=0&tthn_cate_exists=N&item_nm_array=&brd_nm_array=']
    start_urls = ['http://www.lotte.com/display/viewDispShop.lotte?search_flag=&sub_search_flag=Y&disp_no=5414477&allCheckDispNo=&allCheckBrndNo=&lst_sort_cd=10&rowsPerPage=180&disp_type=image&reloadYn=Y&pageIdx=1&prevPageIdx=0&slct_dpml_no=2&SORT_FIELD=&allViewYn=Y&smartpickBranch=&cpcadCnt=0&first_goods_no=0&last_goods_no=0&tthn_cate_exists=N&item_nm_array=&brd_nm_array=']

    def parse_item (self, response):
        clothing_type = "스포츠/아웃도어"
        prod_name = response.xpath("//*/p[@class='pname']/strong/text()").extract()
        component = response.xpath("//*/table[@class='prd-point']/tbody/tr/td/text()").extract_first()
        component = component.strip()
        yield {'제품 이름': prod_name, '분류': clothing_type, '제품 소재': component}

    def parse_page (self, response):
        page_driver = webdriver.Chrome('C:\\Users\\Jessi\\Documents\\chromedriver_win32\\chromedriver.exe')
        item_path_raw = '//*[@id="result"]/div[2]/ul/li['
        url = response.request.url
        for i in range (1, 180):
            try:
                # page_driver.quit()
                page_driver.get(url)
                item_path = item_path_raw + str(i) + ']/div/div/div[3]/div[2]/p/a'
                page_driver.find_element_by_xpath(item_path).click()
                time.sleep(2)
                item_url = page_driver.current_url
                yield scrapy.Request(item_url, callback=self.parse_item, dont_filter=True)
                pass
            except NoSuchElementException:
                self.logger.info('No more items to load.')



    def parse(self, response):
        web_driver = webdriver.Chrome('C:\\Users\\Jessi\\Documents\\chromedriver_win32\\chromedriver.exe')
        web_driver.get("http://www.lotte.com/display/viewDispShop.lotte?search_flag=&sub_search_flag=Y&disp_no=5418403&allCheckDispNo=&allCheckBrndNo=&lst_sort_cd=11&rowsPerPage=180&disp_type=image&reloadYn=Y&pageIdx=1&prevPageIdx=0&slct_dpml_no=2&SORT_FIELD=&allViewYn=Y&smartpickBranch=&cpcadCnt=0&first_goods_no=0&last_goods_no=0&tthn_cate_exists=N&item_nm_array=&brd_nm_array=")
        page_path = "//*/span[@class='selOut'][8]/a"
        web_driver.find_element_by_xpath(page_path).click()
        yield scrapy.Request(web_driver.current_url, callback=self.parse_page, dont_filter=True)
        # for i in range (1, 10):
        #     web_driver.get("http://www.lotte.com/display/viewDispShop.lotte?search_flag=&sub_search_flag=Y&disp_no=5418403&allCheckDispNo=&allCheckBrndNo=&lst_sort_cd=11&rowsPerPage=180&disp_type=image&reloadYn=Y&pageIdx=1&prevPageIdx=0&slct_dpml_no=2&SORT_FIELD=&allViewYn=Y&smartpickBranch=&cpcadCnt=0&first_goods_no=0&last_goods_no=0&tthn_cate_exists=N&item_nm_array=&brd_nm_array=")
        #     page_path = "//*/span[@class='selOut'][" + str(i) + "]/a"
        #     web_driver.find_element_by_xpath(page_path).click()
        #     yield scrapy.Request(web_driver.current_url, callback=self.parse_page, dont_filter=True)
        #     time.sleep(10)
        pass
