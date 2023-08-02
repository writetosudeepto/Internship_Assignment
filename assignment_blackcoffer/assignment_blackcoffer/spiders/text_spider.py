import scrapy
import pandas as pd
import os
from assignment_blackcoffer.items import ArticleItem


class TextSpiderSpider(scrapy.Spider):
    name = "text_spider"
    allowed_domains = ["insights.blackcoffer.com"]

    def start_requests(self):
        # Get the absolute path of the directory containing the settings.py file
        base_path = os.path.abspath(os.path.dirname(__file__))
        # Construct the absolute path of the input CSV file
        csv_file_path = os.path.join(
            base_path, '..', 'data', 'input', 'input.csv')
        df = pd.read_csv(csv_file_path)
        # Replace 'link_column_name' with the actual column containing links
        links = df['URL']
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse)

    # def start_requests(self):
        # Replace 'your_csv_file.csv' with the path to your CSV file containing the links
        df = pd.read_csv(
            r"assignment_blackcoffer\data\input\input.csv")

        # Replace 'link_column_name' with the actual column containing links
        links = df['URL']
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse)

    # def parse(self, response):
        # Your parsing logic here to extract the title and paragraphs
        title_tdb = response.css('h1.tdb-title-text::text').get()
        title_entry = response.css('h1.entry-title::text').get()
        title = title_tdb if title_tdb else title_entry
        paragraphs = response.css('div.td-post-content p::text').getall()

        # Create an instance of the ArticleItem and populate its fields
        article_item = ArticleItem()
        article_item['title'] = title
        article_item['content'] = paragraphs
        article_item['url'] = response.url
        # article_item['url'] = response.meta['url']

        # Yield the ArticleItem
        yield article_item

    def parse(self, response):
        # Your parsing logic here to extract the title and content
        title_tdb = response.css('h1.tdb-title-text::text').get()
        title_entry = response.css('h1.entry-title::text').get()
        title = title_tdb if title_tdb else title_entry

        # Select all elements with text content (paragraphs, strong texts, list items, etc.)
        content = response.css(
            'div.td-post-content *:not(:empty)::text').getall()

        # Create an instance of the ArticleItem and populate its fields
        article_item = ArticleItem()
        article_item['title'] = title
        article_item['content'] = content
        article_item['url'] = response.url

        # Yield the ArticleItem
        yield article_item
