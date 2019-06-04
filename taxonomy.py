# -*- coding: utf-8 -*-
import scrapy


class TaxonomySpider(scrapy.Spider):
    name = 'taxonomy'
    allowed_domains = ['www.thehyundai.com/front/dpa/searchSectItem.thd?sectId=2002&MainpageGroup=Category&GroupbannerName=womenf']
    start_urls = ['https://www.thehyundai.com/front/dpa/searchSectItem.thd?sectId=2002&MainpageGroup=Category&GroupbannerName=womenf']

             
    def parse_clothing(self, response):
        prod_name = response.xpath('//*[@class="prd-title"]/h2/text()').extract_first()
        prod_name = clothing_name.rstrip()
        cleaning_method = response.xpath('//*[@class="table-wrap"]/table/tbody/tr[10]/td/text()').extract_first()
        cleaning_method = cleaning_method.strip()
        component = response.xpath('//*[@class="table-wrap"]/table/tbody/tr[6]/td/text()').extract_first()
        component = component.strip();
        # yield {'제품 이름': prod_name, '분류': clothing_type, '제품 소재': component, '색상': color, '제조사': company, '세탁법': method}

        yield {'제품 이름': prod_name, '분류': clothing_type, '제품 소재': component}
        # yield {'세탁 방법': cleaning_method, '이름': clothing_name, '소재': component}
    
    def parse_page(self, response):
    	clothing_arr = response.xpath("//*[@class='img']/a/@href").extract()
    	for clothing in clothing_arr:
            absolute_next_page_url_3 = response.urljoin(clothing)
            yield scrapy.Request(absolute_next_page_url_3, callback=self.parse_clothing, dont_filter=True)

    def parse_list(self, response):
        page_arr = response.xpath("//*/ul[@class='pagination itemEvalPaging']/li/a/@href").extract()
        for i in range(1,2):
            absolute_next_page_url_2 = response.urljoin(page_arr[i])
            yield scrapy.Request(absolute_next_page_url_2, callback=self.parse_page, dont_filter=True)

    def parse(self, response):
        url_array = response.xpath("//*[@class='cmenu']/li/ul/li/a/@href").extract()
        clothing_type_arr = response.xpath("//*[@class='cmenu']/li/ul/li/a/text()").extract()
        for i in range(0, 10):
            absolute_next_page_url = response.urljoin(url_array[i])
            # clothing_type = clothing_type_arr[i]
            yield scrapy.Request(absolute_next_page_url, callback=self.parse_list, dont_filter=True)


