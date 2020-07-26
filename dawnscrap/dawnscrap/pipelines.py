# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class DawnscrapPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("dawn_latest.db")
        # self.conn = sqlite3.connect("dawn_archives.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS latest_news_tb""")
        self.curr.execute("""CREATE TABLE latest_news_tb(title text, excerpt text, date_time text)""")
        # self.curr.execute("""DROP TABLE IF EXISTS arch_news_tb""")
        # self.curr.execute("""CREATE TABLE arch_news_tb(title text, excerpt text, date_time text)""")

    def process_item(self, item, spider):
        if (item['title'] is not None) and (item['excerpt'] is not None) and (item['time'] is not None):
            item['title'] = item['title'].replace('\n', '').strip()
            item['excerpt'] = item['excerpt'].replace('\n', '').strip()
            self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""Insert into latest_news_tb values (?,?,?) """, (
            item['title'],
            item['excerpt'],
            item['time']
        ))
        # self.curr.execute("""Insert into arch_news_tb values (?,?,?) """, (
        #     item['title'],
        #     item['excerpt'],
        #     item['time']
        # ))
        self.conn.commit()
