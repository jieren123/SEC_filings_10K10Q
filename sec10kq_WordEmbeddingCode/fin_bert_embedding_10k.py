import pandas as pd
from transformers import AutoModel, AutoTokenizer
import torch
import time
start = time.time()


finbert_model = AutoModel.from_pretrained('ProsusAI/finbert')
finbert_tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')

def get_finbert_embedding(text):
    tokenized_text = finbert_tokenizer.encode_plus(text, max_length=512, truncation=True, padding='max_length',
                                           add_special_tokens=True, return_tensors='pt')
    with torch.no_grad():
        outputs = finbert_model(tokenized_text['input_ids'], tokenized_text['attention_mask'])
        embedding = outputs[0][:, 0, :]
    return embedding.tolist()[0]

def get_top_n_words(text, n=512):
    # Tokenize the text into individual words
    tokens = text.lower().split()
    # Count the frequency of each word
    word_counts = {}
    for token in tokens:
        if token in word_counts:
            word_counts[token] += 1
        else:
            word_counts[token] = 1
    # Sort the words by frequency
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    # Get the top n words and return them as a string
    top_words = [word[0] for word in sorted_words[:n]]
    return ''.join(top_words)

# Load the input CSV file
df = pd.read_csv("combined_10k_output.csv")

# Get finBERT embeddings for the content column
embeddings = []
for text in df['content']:
    top_words = get_top_n_words(text)
    embedding = get_finbert_embedding(top_words)
    embeddings.append(embedding)


embeddings_df = pd.DataFrame(embeddings)
embeddings_df.to_csv("fin_bert_embedded_10k_output.csv", index=False)
end = time.time()
print("Execution time:", end - start, "seconds")