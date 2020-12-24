import scrapy


class Mozgva(scrapy.Spider):
    name = "mozgva"
    start_urls = [
        'https://mozgva.com/rating?pretendents_page=2&top_page=2'
    ]

    def parse(self, response):
        # Пагинация
        print(response.css('section.ratingSection td.tName a::text').extract())
