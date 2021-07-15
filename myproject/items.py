# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id= scrapy.Field()
    follower= scrapy.Field()
    following= scrapy.Field()
    mid= scrapy.Field()
    play_view= scrapy.Field()
    read_view= scrapy.Field()
    likes= scrapy.Field()
    name = scrapy.Field()
    face = scrapy.Field()
    sign = scrapy.Field()
