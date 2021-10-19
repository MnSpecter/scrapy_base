from pymongo import MongoClient
import re

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_280

    def process_item(self, item, spider):
        salary = self.fix_salary(item['salary'])

        print('\n--- Вносим запись в БД ----')
        print('Название вакансии: ', item['name'])
        print('Минимальная зарплата: ', salary[0])
        print('Максимальная зарплата: ', salary[1])
        print('Ссылка: ', item['url'])
        print('Сайт: ', item['site'])

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def fix_salary(self, salary):

        drop = "./рубKZTEURUSD" # лень разбираться с конвертацией валют, поэтому просто оставляем цифры

        before = ''
        after = ''
        min_salary = ''
        max_salary = ''

        for char in drop:
            salary = salary.replace(char, "")

        if 'от' in salary:
            after = 1
        if 'до' in salary:
            before = 1

        if '–' in salary:
            min_salary, max_salary = salary.split('–')

        if after and before:
            s = salary.split('до')
            min_salary = s[0]
            max_salary = s[1]

        elif before:
            min_salary = salary

        elif after:
            max_salary = salary

        else:
            min_salary = salary
            max_salary = salary

        min_salary = re.sub(r'[^\x00-\x7F]+', '', min_salary)
        max_salary = re.sub(r'[^\x00-\x7F]+', '', max_salary)
        min_salary = min_salary.replace(' ', '')
        max_salary = max_salary.replace(' ', '')

        salary = [min_salary, max_salary]

        return salary
