import scrapy
from ..items import DawnscrapItem


class DawnLatestNewsSpider(scrapy.Spider):
    name = 'dln_spider'
    start_urls = [
        'https://www.dawn.com/latest-news'
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

