import scrapy
from ..items import MozgvaItem
from fomat import remove_spaces


class Mozgva(scrapy.Spider):
    name = "mozgva"
    start_urls = [
        'https://mozgva.com/rating?pretendents_page=1&top_page=1'
    ]
    number_page = 1

    def parse(self, response):

        for i in response.css('table.tableOfRating tr'):
            # id div по названию команды
            if id := i.css('::attr(id)').get():
                name = i.css('td.tName a::text').get()
                quantity_game = int(response.xpath(f'//*[@id="{id}"]/td[4]/text()').get())
                points = float(i.css('td.tScores::text').get())

                Item = MozgvaItem()

                Item['name'] = remove_spaces(str(i.css('td.tName a::text').get()))  # название команды
                Item['number_game'] = int(response.xpath(f'//*[@id="{id}"]/td[4]/text()').get())  # количество игр
                Item['points'] = float(i.css('td.tScores::text').get())  # кол-во очков

                print(f"название команды: {name} количество игр {quantity_game} количество очков {points}")
                yield Item

        # пагинация
        if links := response.css('span.next a::attr(href)').getall():  # проверка есть ли ссылки на след. страницу
            self.number_page += 1  # номер страницы
            url = response.urljoin(
                f'https://mozgva.com/rating?pretendents_page={self.number_page}&top_page={self.number_page}')
            yield scrapy.Request(url, callback=self.parse)
