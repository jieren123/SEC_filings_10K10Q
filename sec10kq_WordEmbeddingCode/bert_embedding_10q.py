import time
start = time.time()

import pandas as pd
import torch
from transformers import BertModel, BertTokenizer

# Set the device to use for computing
device = torch.device('cpu')

# Load the input CSV file
df = pd.read_csv("combined_10q_output.csv")

# Load the pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name).to(device)

# Get BERT embeddings for the content column
embeddings = []
for text in df['content']:
    input_ids = tokenizer.encode(text, add_special_tokens=True, truncation=True, padding='max_length', max_length=512, return_tensors='pt').to(device)
    with torch.no_grad():
        output = model(input_ids)[0]
    embeddings.append(output[0][0].tolist())

# Convert the embeddings to a pandas DataFrame and save to a new CSV file
embeddings_df = pd.DataFrame(embeddings)
embeddings_df.to_csv("bert_embedded_10q_output.csv", index=False)


end = time.time()
print("Execution time:", end - start, "seconds")