import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import time

start = time.time()
# Load the pre-trained model and tokenizer
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

# Load the data from the CSV file
df = pd.read_csv('combined_10k_output.csv')

# Create an empty dictionary to store the frequency of each label
label_freq = {0:0, 1:0, 2:0}

# Create an empty list to store the label frequencies for each row
row_label_freq = []

# Loop through each row in the dataframe and classify the content using the FinBERT model
for index, row in df.iterrows():
    # Split the content into 512 length segments
    content = row['content']
    segments = [content[i:i+512] for i in range(0, len(content), 512)]
    # Initialize an empty list to store the predicted labels of each segment
    segment_labels = []
    # Classify each segment using the FinBERT model
    for segment in segments:
        # Tokenize the input segment and prepare it for the model
        inputs = tokenizer.encode_plus(segment, add_special_tokens=True, truncation=True, max_length=512)

        # Use the FinBERT model to predict the sentiment of the input segment
        with torch.no_grad():
            outputs = finbert(torch.tensor(inputs['input_ids']).unsqueeze(0),
                              token_type_ids=torch.tensor(inputs['token_type_ids']).unsqueeze(0))
            predictions = torch.argmax(outputs[0], axis=1).item()

        # Add the predicted label to the list of segment labels
        segment_labels.append(predictions)

    # Compute the frequency of each label in the segment labels list
    segment_label_freq = {label: segment_labels.count(label) for label in set(segment_labels)}
    row_label_freq.append(segment_label_freq)
    # print(row_label_freq)
    # # Assign the label with the highest frequency to the row
    # row_label = max(segment_label_freq, key=segment_label_freq.get)
    # row['label'] = row_label
print(row_label_freq)
# Create a new dataframe with the label frequency for each row
label_df = pd.DataFrame(row_label_freq)

# Save the updated dataframe and label frequency dataframe to new CSV files
# df.to_csv('combined_10k_output_label.csv', index=False)
label_df.to_csv('10k_label_frequency_per_row.csv', index=False)

end = time.time()
print("Execution time:", end - start, "seconds")

