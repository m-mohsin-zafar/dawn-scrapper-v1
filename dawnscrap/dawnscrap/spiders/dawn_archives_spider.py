import scrapy
from ..items import DawnscrapItem
import datetime


class DawnArchivesSpider(scrapy.Spider):
    name = 'darch_spider'
    start_urls = [
        'https://www.dawn.com/archive/2019-08-22'
    ]

    def parse(self, response):

        item_list = DawnscrapItem()

        STORIES_SELECTOR = '.story'
        STORY_TITLE_SELECTOR = '.story__title'
        STORY_LINK_SELECTOR = '.story__link::text'
        STORY_EXCERPT_SELECTOR = '.story__excerpt::text'
        STORY_TIME_SELECTOR = 'span.timeago'

        for stories in response.css(STORIES_SELECTOR):

            title = stories.css(STORY_TITLE_SELECTOR).css(STORY_LINK_SELECTOR).extract_first()
            excerpt = stories.css(STORY_EXCERPT_SELECTOR).extract_first()
            time = stories.css(STORY_TIME_SELECTOR).xpath('@title').extract_first()

            item_list['title'] = title
            item_list['excerpt'] = excerpt
            item_list['time'] = time

            yield item_list

            # If we don't use the 'items' approach
            # yield {
            #     'story_title': stories.css(STORY_TITLE_SELECTOR).css(STORY_LINK_SELECTOR).extract_first(),
            #     'story_excerpt': stories.css(STORY_EXCERPT_SELECTOR).extract_first(),
            #     'publication_time': stories.css(STORY_TIME_SELECTOR).xpath('@title').extract_first()
            # }

        prev_page = response.css('ol.pagination li a::attr(href)').get()

        dto = datetime.datetime.strptime(prev_page.split('/')[2], '%Y-%m-%d')
        # print(prev_page)
        # print(dto)
        if dto.date().month == 8 and dto.date().day >= 18:
            yield response.follow(prev_page, callback=self.parse)
