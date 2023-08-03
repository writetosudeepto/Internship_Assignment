# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AssignmentBlackcofferItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()

    avg_sentence_length = scrapy.Field()
    percentage_of_complex_words = scrapy.Field()
    fog_index = scrapy.Field()
    avg_number_of_words_per_sentence = scrapy.Field()
    complex_word_count = scrapy.Field()
    word_count = scrapy.Field()
    syllable_per_word = scrapy.Field()
    personal_pronouns = scrapy.Field()
    avg_word_length = scrapy.Field()

    positive_score = scrapy.Field()
    negative_score = scrapy.Field()
    polarity_score = scrapy.Field()
    subjectivity_score = scrapy.Field()
