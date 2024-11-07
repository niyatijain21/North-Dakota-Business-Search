# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscraperItem(scrapy.Item):
    rows = scrapy.Field()
    business_id = scrapy.Field()
    business_name = scrapy.Field()
    relationship_type = scrapy.Field()
    entity = scrapy.Field()
    