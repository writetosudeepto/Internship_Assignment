import scrapy
import pandas as pd
import os


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

    def parse(self, response):
        url = response.url
        # Your parsing logic here
        # For example, if you want to extract the text content from <p> elements:
        paragraphs = response.css('div.td-post-content p::text').getall()
        # Save the extracted text to a file named after the URL
        filename = url.split("://", 1)[-1].replace("/", "_").strip("_")
        output_folder = 'data/output'
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f'output_{filename}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(paragraphs))
