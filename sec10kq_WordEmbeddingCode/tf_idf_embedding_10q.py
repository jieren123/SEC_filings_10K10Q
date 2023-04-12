import pandas as pd

# df = pd.read_csv("combined_10k_output.csv", nrows=5)
# print(df)
import time
start = time.time()

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the input CSV file
df = pd.read_csv("combined_10q_output.csv")

# Create a TfidfVectorizer object and fit it to the content column
vectorizer = TfidfVectorizer()
vectorizer.fit(df['content'])

# Transform the content column into TF-IDF vectors
tfidf_vectors = vectorizer.transform(df['content'])

# Convert the sparse matrix to a pandas DataFrame
tfidf_df = pd.DataFrame.sparse.from_spmatrix(tfidf_vectors)

# Save the DataFrame to a new CSV file
tfidf_df.to_csv("tf_idf_embedded_10q_output.csv", index=False)


end = time.time()
print("Execution time:", end - start, "seconds")