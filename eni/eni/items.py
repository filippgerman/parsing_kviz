# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EniItem(scrapy.Item):
    name = scrapy.Field()
    number_game = scrapy.Field()
    points = scrapy.Field()

