import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('10q_label_frequency_per_row.csv')
df.fillna(0, inplace=True)
neutral, positive, negative = df.sum() / df.sum().sum()
# print(neutral, positive, negative)
label = []
for index, row in df.iterrows():
    neu = row['0']
    pos = row['1']
    neg = row['2']
    row_sum = row.sum()
    # label positive if num of postive more than negative and percentage greater than overall
    row_label = 0
    if pos >= neg and pos / row_sum >= positive:
        row_label = 1
    elif neg >= pos and neg / row_sum >= negative:
        row_label = 2
    label.append(row_label)

label_df = pd.DataFrame(label, columns=['label'])
label_df.to_csv('10q_label_frequency_final.csv', header=['label'], index=False)

# label_df.to_csv('10k_label_frequency_final.csv', header='label', index=False)
######################################################################################################################
############################
#     Plot bar_plot        #
############################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the label categories
label_categories = {0: 'neutral', 1: 'positive', 2: 'negative'}

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('10q_label_frequency_final.csv')

# Plot a histogram of the labels using seaborn
# plt.figure(figsize=(16, 12)) # set the figure size
sns.countplot(x='label', data=df)
plt.xlabel('Label')
plt.ylabel('Count')
plt.title('10q-filings Sentiment Distribution')

# Display the count of each label exactly over the each bar
for i, count in enumerate(df['label'].value_counts().sort_index()):
    plt.annotate(str(count), xy=(i, count), ha='center', va='bottom')


# Set the x-axis labels to the category labels
plt.xticks(list(label_categories.keys()), label_categories.values())

plt.show()

# plt.savefig('10q_sentiment_distribution.jpg', dpi=300)

plt.savefig('10q_sentiment_distribution.png')

