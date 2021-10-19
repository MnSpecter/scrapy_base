# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import re

from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a[rel="next"]::attr(href)').extract_first()

        response.follow(next_page, callback=self.parse)
        vacansy = response.css(
            'div.f-test-vacancy-item a[class*=f-test-link][href^="/vakansii"]::attr(href)'
        ).extract()

        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1 ::text').extract()
        salary = ''.join(response.css('span[class="_2Wp8I _2rfUm _2hCDz"]::text').extract())
        url = response.url

        yield JobparserItem(name=name[0], salary=salary, url=url, site=self.name)
