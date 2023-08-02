import os


class SaveToFilePipeline:
    def process_item(self, item, spider):
        # Get the parent folder of the current directory (where the spiders folder is located)
        parent_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        # Construct the output folder path inside the parent folder
        output_folder = os.path.join(parent_folder, 'data', 'output')
        os.makedirs(output_folder, exist_ok=True)

        # Get the URL without the "https://" or "http://" part
        url_without_protocol = item['url'].split('://', 1)[-1]

        # Replace forward slashes with underscores in the URL
        url_filename = url_without_protocol.replace('/', '_')

        # Construct the output file path based on the modified URL
        filename = f'{url_filename}.txt'
        output_file = os.path.join(output_folder, filename)

        # Save the content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'{item["title"]}\n')
            f.write('\n'.join(item["content"]))

        return item
