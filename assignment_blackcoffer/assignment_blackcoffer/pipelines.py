import os
import re
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize


class SaveToFilePipeline:
    # def __init__(self):
    #     # Step 1: Load the Stop Words Lists
    #     self.stop_words = self.load_stop_words()

    #     # Step 2: Load the Master Dictionary of Positive and Negative words
    #     base_path = os.path.abspath(os.path.dirname(__file__))
    #     # Construct the absolute path of the input CSV file
    #     master_dict_folder = os.path.join(
    #         base_path, 'data', 'data_dictionary', 'master_dictionary')

    #     self.positive_words = self.load_master_dictionary(
    #         os.path.join(master_dict_folder, 'positive-words.txt'))
    #     self.negative_words = self.load_master_dictionary(
    #         os.path.join(master_dict_folder, 'negative-words.txt'))

    # def __init__(self):
    #     # Step 1: Load the Stop Words Lists
    #     self.stop_words = self.load_stop_words()

    #     # Step 2: Load the Master Dictionary of Positive and Negative words
    #     base_path = os.path.abspath(os.path.dirname(__file__))
    #     # Construct the absolute path of the input CSV file
    #     master_dict_folder = os.path.join(
    #         base_path, 'data', 'data_dictionary', 'master_dictionary')

    #     self.positive_words = self.load_master_dictionary(
    #         os.path.join(master_dict_folder, 'positive-words.txt'))
    #     self.negative_words = self.load_master_dictionary(
    #         os.path.join(master_dict_folder, 'negative-words.txt'))

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

    # def load_stop_words(self):
    #     # Replace 'path/to/your/StopWords' with the actual path to the folder containing Stop Words Lists
    #     base_path = os.path.abspath(os.path.dirname(__file__))
    #     # Construct the absolute path of the input CSV file
    #     stop_words_folder = os.path.join(
    #         base_path, 'data', 'data_dictionary', 'stop_words')
    #     stop_words = set()

    #     # Load each stop words file in the folder and combine them into a single set
    #     for filename in os.listdir(stop_words_folder):
    #         with open(os.path.join(stop_words_folder, filename), 'r') as f:
    #             stop_words.update(f.read().splitlines())

    #     return stop_words

    #     base_path = os.path.abspath(os.path.dirname(__file__))
    #     # Construct the absolute path of the input CSV file
    #     master_dict_path = os.path.join(
    #         base_path, 'data', 'data_dictionary', 'master_dictionary')
    #     with open(master_dict_path, 'r') as f:
    #         master_dictionary = f.read().splitlines()
    #     positive_words = [word.split('\t')[0]
    #                       for word in master_dictionary if word.startswith('positive') and word.split('\t')[0] not in self.stop_words]
    #     negative_words = [word.split('\t')[0]
    #                       for word in master_dictionary if word.startswith('negative') and word.split('\t')[0] not in self.stop_words]
    #     return positive_words, negative_words

    def load_stop_words(self):
        # Replace 'path/to/your/StopWords' with the actual path to the folder containing Stop Words Lists
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

    # def load_master_dictionary(self, file_path):
    #     # Replace 'path/to/your/MasterDictionary' with the actual path to the folder containing positive_words.txt and negative_words.txt
    #     with open(file_path, 'r') as f:
    #         word_list = f.read().splitlines()
    #     return {word for word in word_list if word not in self.stop_words}

    def load_master_dictionary(self, positive_file_path, negative_file_path):
        # Replace 'path/to/your/MasterDictionary' with the actual path to the folder containing positive-words.txt and negative-words.txt
        with open(positive_file_path, 'r') as f:
            positive_word_list = f.read().splitlines()
        with open(negative_file_path, 'r') as f:
            negative_word_list = f.read().splitlines()

        positive_words = {
            word for word in positive_word_list if word not in self.stop_words}
        negative_words = {
            word for word in negative_word_list if word not in self.stop_words}

        return positive_words, negative_words

    def clean_text(self, content):
        stop_words = set(stopwords.words('english'))
        text = ' '.join(content).lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuations
        words = word_tokenize(text)
        words = [word for word in words if word not in stop_words]
        return words

    def is_complex_word(self, word):
        # Implement your logic to check if a word is complex (contains more than two syllables)
        # Here's a simple example using the NLTK library:
        syllables = self.calculate_syllables_per_word(word)
        return syllables > 2

    def calculate_syllables_per_word(self, word):
        # Implement your logic to count the number of syllables in a word
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

    # def calculate_readability_scores(self, content):
    #     # Step 1: Split the content into sentences and words
    #     sentences = sent_tokenize(" ".join(content))
    #     words = word_tokenize(" ".join(content))

    #     # Step 2: Calculate the average sentence length
    #     average_sentence_length = len(words) / len(sentences)

    #     # Step 3: Calculate the number of complex words
    #     complex_words = [word for word in words if self.is_complex_word(word)]
    #     percentage_of_complex_words = len(complex_words) / len(words)

    #     # Step 4: Calculate the Fog Index
    #     fog_index = 0.4 * (average_sentence_length +
    #                        percentage_of_complex_words)

    #     # Step 5: Calculate the average number of words per sentence
    #     average_number_of_words_per_sentence = len(words) / len(sentences)

    #     # Step 6: Calculate the complex word count
    #     complex_word_count = len(complex_words)

    #     # Step 7: Calculate the word count
    #     word_count = len(words)

    #     # Step 8: Calculate the syllable count per word
    #     syllable_per_word = self.calculate_syllables_per_word(words)

    #     # Step 9: Calculate the personal pronouns count
    #     personal_pronouns = sum(1 for word in words if word.lower() in [
    #                             "i", "we", "my", "ours", "us"])

    #     # Step 10: Calculate the average word length
    #     avg_word_length = sum(len(word) for word in words) / len(words)

    #     return {
    #         'avg_sentence_length': average_sentence_length,
    #         'percentage_of_complex_words': percentage_of_complex_words,
    #         'fog_index': fog_index,
    #         'avg_number_of_words_per_sentence': average_number_of_words_per_sentence,
    #         'complex_word_count': complex_word_count,
    #         'word_count': word_count,
    #         'syllable_per_word': syllable_per_word,
    #         'personal_pronouns': personal_pronouns,
    #         'avg_word_length': avg_word_length
    #     }

    def calculate_readability_scores(self, content):
        # Step 1: Split the content into sentences and words
        sentences = sent_tokenize(" ".join(content))
        words = word_tokenize(" ".join(content))

        # Step 2: Calculate the average sentence length
        average_sentence_length = len(words) / len(sentences)

        # Step 3: Calculate the number of complex words
        complex_words = [
            word for word in words if self.is_complex_word(word)]
        percentage_of_complex_words = len(complex_words) / len(words)

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
    # def process_item(self, item, spider):
    #     # Get the parent folder of the current directory (where the spiders folder is located)
    #     parent_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    #     # Construct the output folder path inside the parent folder
    #     output_folder = os.path.join(
    #         parent_folder, 'data', 'output', 'text_files')
    #     os.makedirs(output_folder, exist_ok=True)

    #     # Get the URL without the "https://" or "http://" part
    #     url_without_protocol = item['url'].split('://', 1)[-1]

    #     # Replace forward slashes with underscores in the URL
    #     url_filename = url_without_protocol.replace('/', '_')

    #     # Construct the output file path based on the modified URL
    #     filename = f'{url_filename}.txt'
    #     output_file = os.path.join(output_folder, filename)

    #     # Save the content to the output file
    #     with open(output_file, 'w', encoding='utf-8') as f:
    #         f.write(f'{item["title"]}\n')
    #         f.write('\n'.join(item["content"]))

    #     return item

    # def process_item(self, item, spider):
    #     # Get the parent folder of the current directory (where the spiders folder is located)
    #     parent_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    #     # Construct the output folder path inside the parent folder
    #     output_folder = os.path.join(
    #         parent_folder, 'data', 'output')
    #     os.makedirs(output_folder, exist_ok=True)

    #     # Construct the output CSV file path
    #     output_file = os.path.join(output_folder, 'output.csv')

    #     # Check if the output CSV file already exists or not
    #     # If it exists, append the data to the existing file
    #     # If not, create a new file with headers
    #     if os.path.exists(output_file):
    #         item_df = pd.DataFrame([item])
    #         item_df.to_csv(output_file, mode='a', index=False, header=False)
    #     else:
    #         item_df = pd.DataFrame([item])
    #         item_df.to_csv(output_file, index=False)

    #     # Save the content to a text file
    #     # Get the URL without the "https://" or "http://" part
    #     url_without_protocol = item['url'].split('://', 1)[-1]

    #     # Replace forward slashes with underscores in the URL
    #     url_filename = url_without_protocol.replace('/', '_')

    #     # Construct the output file path based on the modified URL
    #     filename = f'{url_filename}.txt'
    #     output_file_path = os.path.join(output_folder, 'text_files', filename)

    #     # Save the content to the output file
    #     with open(output_file_path, 'w', encoding='utf-8') as f:
    #         f.write(f'{item["title"]}\n')
    #         f.write('\n'.join(item["content"]))

    #     return item

    def process_item(self, item, spider):
        # Get the parent folder of the current directory (where the spiders folder is located)
        parent_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        # Construct the output folder path inside the parent folder
        output_folder = os.path.join(
            parent_folder, 'data', 'output')
        os.makedirs(output_folder, exist_ok=True)

        # Construct the output CSV file path
        output_file = os.path.join(output_folder, 'output.csv')

        # Calculate sentiment scores and readability scores
        sentiment_scores = self.calculate_sentiment_scores(item['content'])
        readability_scores = self.calculate_readability_scores(item['content'])

        # Add the scores to the item dictionary
        item['positive_score'] = sentiment_scores['positive_score']
        item['negative_score'] = sentiment_scores['negative_score']
        item['polarity_score'] = sentiment_scores['polarity_score']
        item['subjectivity_score'] = sentiment_scores['subjectivity_score']
        item['avg_sentence_length'] = readability_scores['avg_sentence_length']
        item['percentage_of_complex_words'] = readability_scores['percentage_of_complex_words']
        item['fog_index'] = readability_scores['fog_index']
        item['avg_number_of_words_per_sentence'] = readability_scores['avg_number_of_words_per_sentence']
        item['complex_word_count'] = readability_scores['complex_word_count']
        item['word_count'] = readability_scores['word_count']
        item['syllable_per_word'] = readability_scores['syllable_per_word']
        item['personal_pronouns'] = readability_scores['personal_pronouns']
        item['avg_word_length'] = readability_scores['avg_word_length']

        # Check if the output CSV file already exists or not
        # If it exists, append the data to the existing file
        # If not, create a new file with headers
        if os.path.exists(output_file):
            item_df = pd.DataFrame([item])
            # Remove the content column
            item_df.drop(columns=['content'], inplace=True)
            item_df.to_csv(output_file, mode='a', index=False, header=False)
        else:
            item_df = pd.DataFrame([item])
            # Remove the content column
            item_df.drop(columns=['content'], inplace=True)
            item_df.to_csv(output_file, index=False)

        # Save the content to a text file
        # Get the URL without the "https://" or "http://" part
        url_without_protocol = item['url'].split('://', 1)[-1]

        # Replace forward slashes with underscores in the URL
        url_filename = url_without_protocol.replace('/', '_')

        # Construct the output file path based on the modified URL
        filename = f'{url_filename}.txt'
        output_file_path = os.path.join(output_folder, 'text_files', filename)

        # Save the content to the output file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(f'{item["title"]}\n')
            f.write('\n'.join(item["content"]))

        return item
