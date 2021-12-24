# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem


class EstateItem(DjangoItem):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    region = scrapy.Field()
    year = scrapy.Field()
    area = scrapy.Field()
    estate_type = scrapy.Field()
    use_type = scrapy.Field()
    ppm = scrapy.Field()
    rooms = scrapy.Field()
    elevator = scrapy.Field()
    convertable = scrapy.Field()
    parking = scrapy.Field()
    mortgage = scrapy.Field()
    rent = scrapy.Field()
    store = scrapy.Field()
    image_url = scrapy.Field()

