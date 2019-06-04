# -*- coding: utf-8 -*-
import scrapy
import time

class SsgCrawlSpider(scrapy.Spider):
    name = 'ssg_crawl'
    allowed_domains = ['shinsegaemall.ssg.com/disp/category.ssg?ctgId=3500002111']
    start_urls = ['http://shinsegaemall.ssg.com/disp/category.ssg?ctgId=3500002111']
 
    def parse_clothing(self, response):
        clothing_type = "스커트"
        prod_name = response.xpath("//*[@class='cdtl_info_tit']/text()").extract()
        info = response.xpath("//*/div[contains(@class,'cdtl_tbl ty2')]/table/tbody/tr/td/div[@class='in']/text()").extract()
        component = info[0].strip() # 소재
        # color = info[1].strip() # 색상
        # company = info[6].strip() # 제조사
        # method = info[4].strip() # 세탁법
        # yield {'제품 이름': prod_name, '분류': clothing_type, '제품 소재': component, '색상': color, '제조사': company, '세탁법': method}
        yield {'제품 이름': prod_name, '분류': clothing_type, '제품 소재': component}

    def parse_page(self, response):
        clothing_arr = response.xpath("//*[@class='thmb']/a/@href").extract()
        for clothing in clothing_arr:
            absolute_next_page_url = response.urljoin(clothing)
            yield scrapy.Request(absolute_next_page_url, callback=self.parse_clothing, dont_filter=True)

    def parse(self, response):
        index = 1
        while (True):
            try:
                url = "http://shinsegaemall.ssg.com/disp/category.ssg?ctgId=3500002111&page=" + str(index)
                yield scrapy.Request(url, callback=self.parse_page, dont_filter=True)
                index = index + 1
                pass
            except Exception as e:
                raise e
        pass

