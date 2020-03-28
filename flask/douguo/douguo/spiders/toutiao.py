# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from douguo.items import DouguoItem


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    URL = "https://www.douguo.com"
    # allowed_domains = ['https://www.douguo.com/fenlei']
    start_urls = ['https://www.douguo.com/fenlei/']

    def parse(self, response):
        remeng = response.xpath('//div[@id="content"]/div[2]/div[1]')
        li_list = remeng.xpath('./ul[@class="sortlist clearfix"]/li')

        for li in li_list:
            name = li.xpath('./a/text()').extract_first()
            sub_url = li.xpath('./a/@href').extract_first()
            url = self.URL + sub_url
            yield Request(url=url, callback=self.parse_list, dont_filter=True, meta={"name": name})

    def parse_list(self, response):
        li_list = response.xpath('//div[@class="mt25"]/ul/li')
        classify = response.xpath('//div[@class="des-material"]/h3/text()').extract_first()
        for li in li_list:
            url = li.xpath('./div[@class="cook-info"]/a/@href').extract_first()
            yield Request(url=self.URL + url, callback=self.parse_detail, meta={"classify": classify})

        # 下一页
        next_url = response.xpath('//a[@class="anext"]/@href').extract_first()
        if next_url:
            yield Request(url=next_url, callback=self.parse_list)

    def parse_detail(self, response):
        print("解析 : ", response.url)
        classify = response.meta.get("classify")
        item = DouguoItem()
        img_url = response.xpath('//div[@id="banner"]/a/img/@src').extract_first()
        title = response.xpath('//div[@class="rinfo relative"]/h1/text()').extract_first()
        read_num = response.xpath('//div[@class="vcnum relative"]/span[1]/text()').extract_first()
        col_num = response.xpath('//div[@class="vcnum relative"]/span[@class="collectnum"]/text()').extract_first()
        aut_img = response.xpath('//a[@class="author-img left"]/img/@src').extract_first()
        aut_name = response.xpath('//div[@class="author-info left"]/a/text()').extract_first()
        aut_desc = response.xpath('//div[@class="rinfo relative"]/p[@class="intro"]/text()').extract_first().strip()
        tips = response.xpath('//div[@class="tips"]/p[1]/text()').extract_first()
        created_time = response.xpath('//p[@class="creattime"]/text()').extract_first()

        # 用料
        materials = {}
        td_list = response.xpath('//div[@class="metarial"]/table/tr/td')
        for td in td_list:
            name = td.xpath('./span[1]/a/text()').extract_first() if td.xpath('./span[1]/a/text()') else td.xpath('./span[1]/text()').extract_first()
            value = td.xpath('./span[2]/text()').extract_first()
            if name:
                materials[name] = value

        # 做法
        step = []
        div_list = response.xpath('//div[@class="step"]/div')
        for div in div_list:
            img_url = div.xpath('./a/img/@src').extract_first()
            info = div.xpath('./div[@class="stepinfo"]/text()').extract()
            for i in info:
                s = i.strip()
                if s:
                    step.append([img_url, s])

        item["classify"] = classify
        item["title"] = title
        item["img_url"] = img_url
        item["read_num"] = read_num
        item["col_num"] = col_num
        item["aut_img"] = aut_img
        item["aut_name"] = aut_name
        item["aut_desc"] = aut_desc
        item["materials"] = materials
        item["step"] = step
        item["tips"] = tips
        item["created_time"] = created_time

        yield item
