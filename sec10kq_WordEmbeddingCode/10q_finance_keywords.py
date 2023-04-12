

import pandas as pd
import nltk
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk.corpus import stopwords
import time
start = time.time()
import pandas as pd
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load the CSV file
df = pd.read_csv("combined_10q_output.csv")

# Define a list of POS tags that are relevant to finance
finance_words = ['NN', 'NNS', 'NNP', 'NNPS', 'VBG', 'VBN', 'VBZ', 'VBD', 'VBP', 'JJ']
finance_key_word_list = []
# Loop over each row in the DataFrame
for index, row in df.iterrows():
    content = row['content']

    # Tokenize the content into words
    tokens = nltk.word_tokenize(content)

    # Remove stopwords from the tokenized words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

    # Tag the filtered tokens with their POS
    tagged_tokens = nltk.pos_tag(filtered_tokens)

    # Create a list of finance-related words
    finance_words_list = [word for word, tag in tagged_tokens if tag in finance_words]

    # Count the occurrences of each word
    word_counts = Counter(finance_words_list)

    # Get the top 1000 most common words
    top_words = [word for word, count in word_counts.most_common(1000)]

    # Join the finance-related words into a single string
    finance_words_string = " ".join(finance_words_list)

    # Append the finance-related words string to the finance_key_word_list
    finance_key_word_list.append(finance_words_string)

# # Add the finance_key_word_list to the DataFrame as a new column
# df['finance_key_words'] = finance_key_word_list
finance_key_word_df = pd.DataFrame(finance_key_word_list)
# Save the DataFrame to a new CSV file
finance_key_word_df.to_csv("10q_finance_key_words.csv",  header=['content'], index = False)
end = time.time()
print("Execution time:", end - start, "seconds")