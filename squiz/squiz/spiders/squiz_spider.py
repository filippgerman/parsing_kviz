import scrapy
from ..items import SquizItem


def remove_spaces(name):
    """
    :param name: str название команды
    :return: str название команды без пробелов в строке
    """
    return ' '.join(name.split())


def format_number(number):
    if ',' in number:
        number = number.replace(',', '.')
    return float(number)


class Squiz(scrapy.Spider):
    name = 'squiz'
    start_urls = ['https://squiz.ru/results/overall']

    def parse(self, response, **kwargs):
        data = []

        for i in response.css('div.t431__data-part2::text').extract():
            data.append(i.split('\n'))

        for i in data[0]:
            item = SquizItem()
            item['name'] = remove_spaces(i.split(';')[3])
            item['number_game'] = int(i.split(';')[4])
            item['points'] = format_number(i.split(';')[5])

            yield item
