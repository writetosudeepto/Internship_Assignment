import os
import re
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from scrapy.utils.log import logger


class SaveToFilePipeline:

    def __init__(self):
        # Step 1: Load the Stop Words Lists
        self.stop_words = self.load_stop_words()

        # Step 2: Load the Master Dictionary of Positive and Negative words
        base_path = os.path.abspath(os.path.dirname(__file__))
        master_dict_folder = os.path.join(
            base_path, 'data', 'data_dictionary', 'master_dictionary')

        self.positive_words, self.negative_words = self.load_master_dictionary(
            os.path.join(master_dict_folder, 'positive-words.txt'),
            os.path.join(master_dict_folder, 'negative-words.txt')
        )

    def load_stop_words(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        # Construct the absolute path of the input CSV file
        stop_words_folder = os.path.join(
            base_path, 'data', 'data_dictionary', 'stop_words')
        stop_words = set()

        # Load each stop words file in the folder and combine them into a single set
        for filename in os.listdir(stop_words_folder):
            with open(os.path.join(stop_words_folder, filename), 'r') as f:
                stop_words.update(f.read().splitlines())

        return stop_words

    def clean_text(self, content):
        text = ' '.join(content).lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuations
        words = word_tokenize(text)
        # Use self.stop_words
        words = [word for word in words if word not in self.stop_words]
        return words

    def load_master_dictionary(self, positive_file_path, negative_file_path):
        with open(positive_file_path, 'r') as f:
            positive_word_list = f.read().splitlines()
        with open(negative_file_path, 'r') as f:
            negative_word_list = f.read().splitlines()

        positive_words = set(positive_word_list)
        negative_words = set(negative_word_list)

        return positive_words, negative_words

    def is_complex_word(self, word):
        syllables = self.calculate_syllables_per_word(word)
        return syllables > 2

    def calculate_syllables_per_word(self, word):
        # Here's a simple example using a basic rule-based approach:
        vowels = "aeiouAEIOU"
        syllable_count = 0
        prev_char_vowel = False

        for char in word:
            if char in vowels:
                if not prev_char_vowel:
                    syllable_count += 1
                prev_char_vowel = True
            else:
                prev_char_vowel = False

        # Adjust the count for certain cases
        if word.endswith("e"):
            syllable_count -= 1
        if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
            syllable_count += 1

        return syllable_count

    def calculate_sentiment_scores(self, content):
        words = content
        positive_score = sum(
            1 for word in words if word in self.positive_words)
        negative_score = sum(
            1 for word in words if word in self.negative_words)

        # Log positive and negative words
        positive_words_list = [
            word for word in words if word in self.positive_words]
        negative_words_list = [
            word for word in words if word in self.negative_words]
        if positive_words_list:
            logger.debug(
                f"Here are the positive words: {', '.join(positive_words_list)}")
        if negative_words_list:
            logger.debug(
                f"Here are the negative words: {', '.join(negative_words_list)}")

        polarity_score = (positive_score - negative_score) / \
            ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (
            positive_score + negative_score) / (len(words) + 0.000001)
        return {
            'positive_score': positive_score,
            'negative_score': negative_score,
            'polarity_score': polarity_score,
            'subjectivity_score': subjectivity_score
        }

    def calculate_readability_scores(self, content):
        # Step 1: Split the content into sentences and words
        sentences = sent_tokenize(" ".join(content))
        words = word_tokenize(" ".join(content))

        # Step 2: Calculate the average sentence length
        average_sentence_length = len(words) / len(sentences)

        # Step 3: Calculate the number of complex words
        complex_words = [
            word for word in words if self.is_complex_word(word)]
        percentage_of_complex_words = len(complex_words) * 100 / len(words)

        # Step 4: Calculate the Fog Index
        fog_index = 0.4 * (average_sentence_length +
                           percentage_of_complex_words)

        # Step 5: Calculate the average number of words per sentence
        average_number_of_words_per_sentence = len(words) / len(sentences)

        # Step 6: Calculate the complex word count
        complex_word_count = len(complex_words)

        # Step 7: Calculate the word count
        word_count = len(words)

        # Step 8: Calculate the syllable count per word
        syllable_count = sum(self.calculate_syllables_per_word(word)
                             for word in words)
        syllable_per_word = syllable_count / len(words)

        # Step 9: Calculate the personal pronouns count
        personal_pronouns = sum(1 for word in words if word.lower() in [
                                "i", "we", "my", "ours", "us"])

        # Step 10: Calculate the average word length
        avg_word_length = sum(len(word) for word in words) / len(words)

        return {
            'avg_sentence_length': average_sentence_length,
            'percentage_of_complex_words': percentage_of_complex_words,
            'fog_index': fog_index,
            'avg_number_of_words_per_sentence': average_number_of_words_per_sentence,
            'complex_word_count': complex_word_count,
            'word_count': word_count,
            'syllable_per_word': syllable_per_word,
            'personal_pronouns': personal_pronouns,
            'avg_word_length': avg_word_length
        }

    def process_item(self, item, spider):
        # Calculate sentiment scores and readability scores
        sentiment_scores = self.calculate_sentiment_scores(item['content'])
        readability_scores = self.calculate_readability_scores(item['content'])

        # Construct the new row data as a dictionary
        data = {
            'URL_ID': [item['url_id']],
            'URL': [item['url']],
            'TITLE': [item['title']],
            'POSITIVE SCORE': [sentiment_scores['positive_score']],
            'NEGATIVE SCORE': [sentiment_scores['negative_score']],
            'POLARITY SCORE': [sentiment_scores['polarity_score']],
            'SUBJECTIVITY SCORE': [sentiment_scores['subjectivity_score']],
            'AVG SENTENCE LENGTH': [readability_scores['avg_sentence_length']],
            'PERCENTAGE OF COMPLEX WORDS': [readability_scores['percentage_of_complex_words']],
            'FOG INDEX': [readability_scores['fog_index']],
            'AVG NUMBER OF WORDS PER SENTENCE': [readability_scores['avg_number_of_words_per_sentence']],
            'COMPLEX WORD COUNT': [readability_scores['complex_word_count']],
            'WORD COUNT': [readability_scores['word_count']],
            'SYLLABLE PER WORD': [readability_scores['syllable_per_word']],
            'PERSONAL PRONOUNS': [readability_scores['personal_pronouns']],
            'AVG WORD LENGTH': [readability_scores['avg_word_length']],
        }

        # Create a new DataFrame with the data
        new_row_df = pd.DataFrame(data)

        # Save the DataFrame to the output CSV file
        base_path = os.path.abspath(os.path.dirname(__file__))
        output_folder = os.path.join(base_path, 'data', 'output')
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, 'output.csv')

        # Check if the output file exists
        if os.path.exists(output_file):
            # Read the existing DataFrame from 'output.csv'
            output_df = pd.read_csv(output_file)

            # Concatenate the new row with the existing DataFrame
            output_df = pd.concat([output_df, new_row_df], ignore_index=True)

            # Sort the DataFrame by 'URL_ID'
            output_df.sort_values(by='URL_ID', inplace=True)

            # Save the updated DataFrame to the output CSV file
            output_df.to_csv(output_file, index=False)
        else:
            # If 'output.csv' doesn't exist, create it with the new row DataFrame
            new_row_df.to_csv(output_file, index=False)

        # Save the content to a text file
        url_without_protocol = item['url'].split('://', 1)[-1]
        url_filename = url_without_protocol.replace('/', '_')
        filename = f'{url_filename}.txt'
        output_file_path = os.path.join(output_folder, 'text_files', filename)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(f'{item["title"]}\n')
            f.write('\n'.join(item["content"]))

        return item
