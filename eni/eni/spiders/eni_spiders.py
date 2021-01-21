import scrapy
from scrapy import Request, FormRequest
from scrapy.http import JsonRequest
from ..items import EniItem


def format_row(row):
    result = ""
    for i in row[0]:
        if i.isdigit() or i == '.':
            result += i
    return result


def remove_spaces(name):
    """
    :param name: str название команды
    :return: str название команды без пробелов в строке
    """
    return ' '.join(name.split())


class KvizPlease(scrapy.Spider):
    name = "eni"
    number_commands = 0
    check = True

    def get_data(self):
        data = {
            'params[rows]': f"{self.number_commands}",
            'params[type]': '0',
            'params[season]': 'all',
            'params[direction]': 'desc',
            'params[order]': 'points_sum',
        }
        return data

    def start_requests(self):
        yield FormRequest(url='https://albertparty.ru/api/get_new_rows', method='POST', formdata=self.get_data())

    def parse(self, response, **kwargs):
        item = EniItem()
        for i in response.json()['data']['table']:
            if i.get('team'):
                item['name'] = remove_spaces(i.get('team'))
                item['number_game'] = int(i.get('count'))
                item['points'] = float(format_row(i.get('sum')))

                yield item
            else:
                self.check = False

        if self.check:
            self.number_commands += 10
            yield FormRequest(url='https://albertparty.ru/api/get_new_rows', method='POST', formdata=self.get_data(),
                              callback=self.parse)
