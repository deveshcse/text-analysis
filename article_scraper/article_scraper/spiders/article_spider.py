# import scrapy
# import pandas as pd
# import os
#
# def get_url_id(url):
#     data = pd.read_excel(r"C:\Users\dmish\Desktop\Test Assignment\Input.xlsx")
#     # Find the corresponding URL_ID for the target URL
#     url_id = data.loc[data['URL'] == url, 'URL_ID'].iloc[0] if not data.empty else None
#
#     return url_id
#
#
# class ArticleSpider(scrapy.Spider):
#     name = "article_spider"
#
#     # Load the URLs from an Excel file using Pandas
#     input_data = pd.read_excel(r"C:\Users\dmish\Desktop\Test Assignment\Input.xlsx")
#
#     # Extract URLs from the DataFrame
#     start_urls = input_data['URL'].tolist()
#
#     def parse(self, response):
#
#         article_title = response.css('.tdb-title-text::text, .entry-title::text').get()
#         article_text = " ".join([p.get() for p in response.css('p:not(.tdm-descr)::text')])
#
#         # Get the URL_ID from the start URL
#         url = response.url
#         url_id = get_url_id(url)
#
#         # Check if the CSV file exists
#         csv_file = r"C:\Users\dmish\Desktop\Test Assignment\output.csv"
#
#         if os.path.exists(csv_file):
#             # Load existing data from the CSV file into a DataFrame
#             existing_data = pd.read_csv(csv_file)
#
#             # Create a DataFrame with the scraped data
#             scraped_data = pd.DataFrame({'URL_ID': [url_id], 'Title': [article_title], 'Text': [article_text]})
#
#             # Concatenate the existing data with the scraped data
#             combined_data = pd.concat([existing_data, scraped_data], ignore_index=True)
#
#             # Save the combined DataFrame to the CSV file
#             combined_data.to_csv(csv_file, index=False, mode='w')
#         else:
#             # If the CSV file doesn't exist, create it with the scraped data
#             scraped_data = pd.DataFrame({'URL_ID': [url_id], 'Title': [article_title], 'Text': [article_text]})
#             scraped_data.to_csv(csv_file, index=False, mode='w')
#
#         self.log(f'Appended data to {csv_file}')
#


import scrapy
import pandas as pd
import os


def get_url_id(url):
    data = pd.read_excel(r"C:\Users\dmish\Desktop\Test Assignment\Input.xlsx")
    # Find the corresponding URL_ID for the target URL
    url_id = data.loc[data['URL'] == url, 'URL_ID'].iloc[0] if not data.empty else None
    return url_id


class ArticleSpider(scrapy.Spider):
    name = "article_spider"

    # Load the URLs from an Excel file using Pandas
    input_data = pd.read_excel(r"C:\Users\dmish\Desktop\Test Assignment\Input.xlsx")

    # Extract URLs from the DataFrame
    start_urls = input_data['URL'].tolist()

    def parse(self, response):
        # Check the response status code
        if response.status == 404:
            # Append a row with "None" for a 404 response
            self.append_none_row(response.url)
            return

        article_title = response.css('.tdb-title-text::text, .entry-title::text').get()
        article_text = response.css('p::text').extract()
        # Get the URL_ID from the start URL
        url = response.url
        url_id = get_url_id(url)

        # Check if the CSV file exists
        csv_file = r"C:\Users\dmish\Desktop\Test Assignment\dataset.csv"

        if os.path.exists(csv_file):
            # Load existing data from the CSV file into a DataFrame
            existing_data = pd.read_csv(csv_file)

            # Create a DataFrame with the scraped data
            scraped_data = pd.DataFrame({'URL_ID': [url_id], 'Title': [article_title], 'Text': [article_text]})

            # Concatenate the existing data with the scraped data
            combined_data = pd.concat([existing_data, scraped_data], ignore_index=True)

            # Save the combined DataFrame to the CSV file
            combined_data.to_csv(csv_file, index=False, mode='w')
        else:
            # If the CSV file doesn't exist, create it with the scraped data
            scraped_data = pd.DataFrame({'URL_ID': [url_id], 'Title': [article_title], 'Text': [article_text]})
            scraped_data.to_csv(csv_file, index=False, mode='w')

        self.log(f'Appended data to {csv_file}')

    def append_none_row(self, url):
        # Append a row with "None" for the title and text for a 404 response
        url_id = get_url_id(url)
        csv_file = r"C:\Users\dmish\Desktop\Test Assignment\output.csv"

        none_data = pd.DataFrame({'URL_ID': [url_id], 'Title': [None], 'Text': [None]})

        if os.path.exists(csv_file):
            # Load existing data from the CSV file into a DataFrame
            existing_data = pd.read_csv(csv_file)
            combined_data = pd.concat([existing_data, none_data], ignore_index=True)

            # Save the combined DataFrame to the CSV file
            combined_data.to_csv(csv_file, index=False, mode='w')
        else:
            # If the CSV file doesn't exist, create it with the "None" data
            none_data.to_csv(csv_file, index=False, mode='w')

        self.log(f'Appended "None" data to {csv_file}')
