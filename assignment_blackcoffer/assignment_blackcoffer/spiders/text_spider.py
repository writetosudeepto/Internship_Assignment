import scrapy
import pandas as pd
import os
from assignment_blackcoffer.items import ArticleItem
import re


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
        url_ids = df['URL_ID']
        for link, url_id in zip(links, url_ids):
            yield scrapy.Request(url=link, callback=self.parse, meta={'url_id': url_id})

    def parse(self, response):
        # Your parsing logic here to extract the title and content
        title_tdb = response.css('h1.tdb-title-text::text').get()
        title_entry = response.css('h1.entry-title::text').get()
        title = title_tdb if title_tdb else title_entry

        # Select all elements with text content inside HTML tags (excluding CSS-related content)
        content_elements = response.css(
            'div.td-post-content *:not(style)::text').extract()

        # Process each text element and remove extra spaces and escape characters
        content = []
        for text in content_elements:
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            content.append(cleaned_text)

        # Filter out empty strings
        content = [text for text in content if text]

        # Create an instance of the ArticleItem and populate its fields
        article_item = ArticleItem()
        article_item['title'] = title
        article_item['content'] = content
        article_item['url'] = response.url

        # Extract URL ID from meta and add it to the item
        url_id = response.meta.get('url_id')
        article_item['url_id'] = url_id

        # Yield the ArticleItem
        yield article_item
