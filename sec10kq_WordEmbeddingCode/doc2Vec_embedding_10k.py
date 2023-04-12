import pandas as pd

# df = pd.read_csv("combined_10k_output.csv", nrows=5)
# print(df)
import time
start = time.time()
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess

# Load the input CSV file
df = pd.read_csv("combined_10k_output.csv")

# Preprocess the documents and create TaggedDocument objects
tagged_data = [TaggedDocument(words=simple_preprocess(doc), tags=[i]) for i, doc in enumerate(df['content'])]

# Train the Doc2Vec model
model = Doc2Vec(tagged_data, vector_size=100, window=5, min_count=1, epochs=20)

# Get the embeddings for each document and save to a new CSV file
embeddings = [model.infer_vector(simple_preprocess(doc)) for doc in df['content']]
embeddings_df = pd.DataFrame(embeddings)
embeddings_df.to_csv("doc2vec_embeddings_10k.csv", index=False)

end = time.time()
print("Execution time:", end - start, "seconds")