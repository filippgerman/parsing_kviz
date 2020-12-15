import scrapy
from ..items import SquizItem


class Squiz(scrapy.Spider):
    name = 'Squiz'
    start_urls = ['https://squiz.ru/results/overall']

    def parse(self, response):
        data = []

        for i in response.css('div.t431__data-part2::text').extract():
            data.append(i.split('\n'))


        for i in data[0]:

            Item = SquizItem()
            Item['name'] = i.split(';')[3]
            Item['number_game'] = int(i.split(';')[4])
            Item['points'] = float(i.split(';')[5])

            yield Item
