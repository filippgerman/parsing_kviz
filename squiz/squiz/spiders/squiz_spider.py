import scrapy
from ..items import SquizItem
from fomat import remove_spaces


def format_number(number):
    if ',' in number:
        number = number.replace(',', '.')
    return float(number)



class Squiz(scrapy.Spider):
    name = 'squiz'
    start_urls = ['https://squiz.ru/results/overall']

    def parse(self, response):
        data = []

        for i in response.css('div.t431__data-part2::text').extract():
            data.append(i.split('\n'))

        for i in data[0]:
            # print(f"{i.split(';')[3]} {int(i.split(';')[4])} {format_number(i.split(';')[5])}")
            Item = SquizItem()
            Item['name'] = remove_spaces(i.split(';')[3])
            Item['number_game'] = int(i.split(';')[4])
            Item['points'] = format_number(i.split(';')[5])

            yield Item
