import scrapy
from ..items import KviziumItem


def remove_spaces(name):
    """
    :param name: str название команды
    :return: str название команды без пробелов в строке
    """
    return ' '.join(name.split())


class Kvizium(scrapy.Spider):
    name = "kvizium"
    start_urls = ['https://quizium.ru/ajaxrating?search_team=&season=all&city=7&json=1&offset=0']
    number = 10

    def parse(self, response, **kwargs):
        if response.json().get('rows'):
            for row in response.json().get('rows'):

                kviz_item = KviziumItem()
                try:
                    kviz_item['name'] = remove_spaces(row.get('team_name'))
                    kviz_item['number_game'] = int(row.get('all_games'))
                    kviz_item['points'] = float(row.get('points_alltime'))
                except (KeyError, ValueError):
                    kviz_item['number_game'] = 0
                finally:
                    yield kviz_item

            self.number += 10
            yield scrapy.Request(
                f'https://quizium.ru/ajaxrating?search_team=&season=all&city=7&json=1&offset={self.number}',
                callback=self.parse)
