import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from brainboy.brainboy.items import BrainboyItem


def format_name(name):
    """
    :param name: str имя команды, для парсинга
    :return: str форматированное имя команды (без цифр и пунктиров)
    """
    name = name.split(" ")
    return ' '.join(name[2::])


def remove_spaces(name):
    """
    :param name: str название команды
    :return: str название команды без пробелов в строке
    """
    return ' '.join(name.split())


class Mozgoboy(scrapy.Spider):
    name = "brainboy"
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    offset = 0
    check = True

    def get_url(self):
        return f"http://mozgoboy.ru/ajax?action=get/rating&city=5&offset={self.offset}&season=all&league=1&search_team_name=&_=1610204052611"

    def start_requests(self):
        yield Request(
            url=self.get_url(),
            headers=self.headers)

    def parse(self, response, **kwargs):
        if response.text:
            soup = BeautifulSoup(response.text, 'lxml')
            item = BrainboyItem()
            for tr in soup.find_all('tr', class_='command_row'):
                name = format_name(tr.find('td').get_text())

                item['number_game'] = int(tr.find('td', class_='games').get_text())
                item['points'] = float(tr.find('td', class_='points').get_text())
                item['name'] = remove_spaces(name)  # убирает лищние пробелы
                yield item
            else:
                self.offset += 20
                yield Request(url=self.get_url(), headers=self.headers, callback=self.parse)


process = CrawlerProcess()
process.crawl(Mozgoboy)
process.start()
