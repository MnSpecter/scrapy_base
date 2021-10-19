# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import re

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = 'https://hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']

        response.follow(next_page, callback=self.parse)
        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').getall()
        salary = ''.join(response.css('span[data-qa="vacancy-salary-compensation-type-net"]'
                                      '[class="bloko-header-2 bloko-header-2_lite"]::text').getall())
        url = response.url

        yield JobparserItem(name=name[0], salary=salary, url=url, site=self.name)

