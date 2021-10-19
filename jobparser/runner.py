from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
#from jobparser.pipelines import JobparserPipeline

from pymongo import MongoClient
import pandas as pd

from jobparser import settings

if __name__ == '__main__':
    search = 'Python'
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)
    process.start()

    print(process)