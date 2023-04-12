import pandas as pd
import requests
import re
import os
import csv
import datetime
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('wordnet')

from dateutil.parser import parse
from bs4 import BeautifulSoup
# import nltk
import os
import re


def get_content(path):
    if '.DS_Store' in path or '-17-' in path:
        return None  # skip irrelevant files
    # Load the HTML file
    with open(path) as f:
        html_content = f.read()
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    # Extract the text content
    text_content = soup.get_text()
    
    print(path)
    year_string = "20" + path.split("/")[9].split("-")[1]

    print(year_string)

    def convert_year_to_date(year_string):
        year = int(year_string)
        date = datetime.datetime(year, 12, 31)
        return date.strftime('%m/%d/%Y')

    # example usage
    date_value = convert_year_to_date(year_string)
    print(date_value) # Output: December 31, 2018


    ##############################################################
    # lowercase, remove English Stopwords and remove punctuation #
    ##############################################################

    # Load the English stopwords
    # nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    # Convert the text to lowercase
    text_content = text_content.lower()

    # Tokenize the text content
    words = text_content.split()

    # Remove the stopwords
    filtered_words = [word for word in words if word not in stop_words and len(word) <= 50]

    # word contains only alphabetic characters
    filtered_words_clean = [word for word in filtered_words if word.isalpha()]

    ####################################
    #       Stemming get root form     #
    ####################################
    # Download the WordNet corpus (only need to do this once)
    # nltk.download('wordnet')

    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize each word and store in a list
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words_clean if len(word) > 2]

    # Join the lemmatized words back into a string
    lemmatized_text = ' '.join(lemmatized_words)

    return date_value, lemmatized_text


fileType = "10-K"
fileTypePath = "10K"
import os

path = '/Users/jie_ren/Documents/SEC10K10Q/10K/sec-edgar-filings'
save_path = '/Users/jie_ren/Documents/SEC10K10Q/result/10K_output_400_503.csv'
import os

# The root directory to search for HTML files
# root_dir = '/path/to/your/directory'
root_dir = path
# A list to store the absolute paths of HTML files
html_files = []

# Walk through the directory tree and find all HTML files
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            html_files.append(os.path.abspath(os.path.join(dirpath, filename)))

# with open(save_path, mode='w') as output_file:
#     output_writer = csv.writer(output_file)
#     # output_writer.writerow(['Symbol',  'content'])
#     output_writer.writerow(['Symbol', 'date', 'content'])

# with open('terminal_no_date2.txt', 'r') as f:
#     no_date_lines = [line.strip() for line in f if 'No date found for this path' in line]
#     for line in no_date_lines:
#         link = line.split("path")[2].strip()
#         html_files.append(os.path.abspath(link))

# Print the absolute paths of HTML files
for html_file in html_files:
    print(html_file)
    # The path to the HTML file
    path = html_file
    # Split the path into individual directories and files
    path_parts = os.path.normpath(path).split(os.path.sep)

    # Find the index of 'sec-edgar-filings' in the path
    sec_edgar_index = path_parts.index('sec-edgar-filings')

    # Get the ticker symbol by looking at the directory before '10-Q'
    tickerSymbol = path_parts[sec_edgar_index + 1]

    # date_value =1 
    # lemmatized_text = 2 

    if get_content(html_file):
        date_value, lemmatized_text = get_content(html_file)

    with open(save_path, mode='a') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow([tickerSymbol, date_value, lemmatized_text])
