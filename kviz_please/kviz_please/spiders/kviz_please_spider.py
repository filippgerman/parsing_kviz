import scrapy
from ..items import SquizItem


def format_row(row):
    result = ""
    for i in row[0]:
        if i.isdigit() or i == '.':
            result += i
    return result


class KvizPlease(scrapy.Spider):
    name = "kviz_please"
    start_urls = [
        'https://quizium.ru/ajaxrating?search_team=&season=all&city=7&json=1&offset=0'
    ]

    def parse(self, response):

        for div in response.css('.item'):
            # получение данных о команде
            name = div.css('.rating-table-row-td1::text').extract()
            number_game = div.css('.rating-table-kol-game::text').extract()
            points = div.css('.rating-table-points::text').extract()

            # форматирование строки очков
            points = format_row(points)

            # Добавление в объект
            Item = SquizItem()
            try:
                Item['name'] = name[1]
                Item['number_game'] = int(number_game[1])
                Item['points'] = float(points)
            except (KeyError, ValueError):
                Item['number_game'] = 0
            finally:
                yield Item

            #Пагинация
            for href in response.css('ul.pagination > li.next > a::attr("href")'):
                if url := response.urljoin(href.extract()):
                    yield scrapy.Request(url, callback=self.parse)
