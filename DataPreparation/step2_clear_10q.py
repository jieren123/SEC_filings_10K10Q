import pandas as pd
import requests
import re
import os
import csv
from bs4 import BeautifulSoup
# from get_tenQ_content import get_content
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('wordnet')

# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
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

    date_string = ''
    date_value = ''
    # Attempt to find the date using the XBRL tag
    try:
        date_element = soup.find("ix:nonnumeric", {"name": "dei:DocumentPeriodEndDate"})
        # If found, extract the date
        if date_element:
            date_string = date_element.text
            # date_string = parse(date_str).date()
            # print(date_value)
    except:
        pass

    # If not found, attempt to find the date using regex
    try:
        match = re.search(r'10-Q for the Quarterly Period Ended\s+(\w+\s+\d+,\s+\d+)', html_content)
        if match:
            date_string = match.group(1)
        else:
            match_1 = re.search(r'10-Q for the Quarterly Period Ended\s+(.*?)\s+', html_content)
            if match_1:
                date_value = match_1.group(1)
            else:
                date_pattern = r'([A-Z][a-z]{2,8}\s\d{1,2},\s\d{4})'
                for tag in soup.find_all('font', string=lambda t: t and 'quarterly period ended' in t.lower()):
                    date_match = re.search(date_pattern, tag.find_next_sibling('font').text)
                    if date_match:
                        date_string = date_match.group(1)
                    else:
                        date_pattern2 = r'the quarterly period ended\s*<a.*?>(.*?)</a>'
                        date_match2 = re.search(date_pattern, html_content)
                        if date_match2:
                            date_string = match_1.group(1)
                        else:
                            date_value = ''
                            print('No date found.')
    except:
        pass

    # try:
    #     date_start_index = text_content.find("For the quarterly period ended ") + len("For the quarterly period ended ")
    #     date_end_index = text_content.find(".", date_start_index)
    #     date_string = text_content[date_start_index:date_end_index]
    # except:
    #     pass

    # try:
    #     date_start_index = text_content.find("FOR THE QUARTERLY PERIOD ENDED ") + len("FOR THE QUARTERLY PERIOD ENDED ")
    #     date_end_index = text_content.find(".", date_start_index)
    #     date_string = text_content[date_start_index:date_end_index]
    # except:
    #     pass

    try:
        match = re.search(r'QUARTERLY PERIOD ENDED\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', html_content)
        if match:
            date_string = match.group(1)
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass

    try:
        match = re.search(r'the quarterly period ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', html_content)
        if match:
            date_string = match.group(1)
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass


    try:
        match = re.search(r'QUARTERLY REPORTING PERIOD ENDED\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', html_content)
        if match:
            date_string = match.group(1)
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass

    try:
        match = re.search(r'quarterly reporting period ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', html_content)
        if match:
            date_string = match.group(1)
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass


    try:
        match = re.search(r'the period ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', html_content)
        if match:
            date_string = match.group(1)
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass


    try:
        date_pattern = r'\b(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\b\s+\d{1,2},\s+\d{4}'
        match = re.search(date_pattern, html_content)
        if match:
            date_string = match.group()
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass

    try:
        date_pattern = r'\b(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\b\s+\d{1,2},\s+\d{4}'
        match = re.search(date_pattern, html_content)
        if match:
            date_string = match.group()
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass

    try:
        date_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'
        match = re.search(date_pattern, html_content)
        if match:
            date_string = match.group()
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass

    try:
        date_pattern = r'\b(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\b\s+&nbsp;?\d{1,2},\s+\d{4}'
        match = re.search(date_pattern, html_content)
        if match:
            date_string = match.group()
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass

    try:
        date_pattern = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b\s+&nbsp;?\d{1,2},\s+\d{4}'
        match = re.search(date_pattern, html_content)
        if match:
            date_string = match.group()
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass

    try:
        # bold_text = soup.b.string
        # date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\.?\s+\d{1,2},\s+\d{4}\b'
        # date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\w*\.?\s+\d{1,2},\s+\d{4}\b'
        date_pattern = r"([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})"
        match = re.search(date_pattern, html_content)
        if match:
            date_string = match.group(0)
        else:
            date_value = ''
            print("No date found in the HTML code.")
    except:
        pass


    print("date_string", date_string)

    try:
        if len(date_string) == 0 and len(date_value) == 0:
            print("No date found for this path, No date found for this path", path)
        else:
            date = parse(date_string).date()
            date_value = date.strftime('%m/%d/%Y')
            print("date_value", date_value)
    except:
        pass

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


fileType = "10-Q"
fileTypePath = "10Q"
import os

path = '/Users/jie_ren/Documents/SEC10K10Q/10Q/sec-edgar-filings'
save_path = '/Users/jie_ren/Documents/SEC10K10Q/result/10Q_output_66_151.csv'
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

# path = '/Users/jie_ren/Documents/SEC10K10Q/10Q/sec-edgar-filings'
# abspath = os.path.abspath(path)
# os.chdir(abspath)
# tickerSymbol_List = os.listdir()
# for tickerSymbol in tickerSymbol_List:
#     print("tickerSymbol", tickerSymbol)
#     if not os.path.isdir(tickerSymbol):
#         continue  # skip non-directory entries

#     subpath = os.path.join(abspath, tickerSymbol, '10-Q')
#     subabspath = os.path.abspath(subpath)
#     os.chdir(subabspath)
#     subsubfileList = os.listdir()
#     for subsubfile in subsubfileList:
#         if not os.path.isdir(subsubfile):
#             continue  # skip non-directory entries
#         file_path = os.path.join(subabspath, subsubfile, 'filing-details.html')

#         print("file_path: ", file_path)

#         if get_content(file_path):
#             date_value, lemmatized_text = get_content(file_path)

#         with open('/Users/jie_ren/Documents/SEC10K10Q/10Q_output_0_23.csv', mode='a') as output_file:
#             output_writer = csv.writer(output_file)
#             output_writer.writerow([tickerSymbol, date_value, lemmatized_text])
