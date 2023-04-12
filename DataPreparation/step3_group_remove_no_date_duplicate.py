import pandas as pd

# Read in the CSV file
# df = pd.read_csv('10Q_output_10_21_clean.csv', header=None)
# df = pd.read_csv('10Q_output_0_10.csv', header=None)
# df = pd.read_csv('10Q_output_21_150.csv', header = None)
# df = pd.read_csv('10Q_output_0_150_date_missing.csv', header = None)
df = pd.read_csv('10K_output_400_503.csv', header = None)

# Add the header
df.columns = ['Symbol', 'date', 'content']

# Drop rows where the 'date' column is empty
df = df[df['date'].notna()]

# Remove duplicate rows
df = df.drop_duplicates()


# read the SP500 file
sp500 = pd.read_csv('SP500_20230317.csv')

# merge with our dataframe
merged_df = pd.merge(df, sp500[['Symbol', 'GICS Sector']], on='Symbol', how='left')


# rename the 'GICS Sector' column to 'sector'
merged_df = merged_df.rename(columns={'GICS Sector': 'sector'})


# reorder the columns
merged_df = merged_df.loc[:, ['Symbol', 'date', 'sector', 'content']]

# show the resulting dataframe
print(merged_df.head())


# create the new filename with folder path
# filename = '/Users/jie_ren/Documents/SEC10K10Q/10Q_clean/10Q_output_10_21_clean_processed.csv'
# filename = '/Users/jie_ren/Documents/SEC10K10Q/10Q_clean/10Q_output_0_10_processed.csv'
# filename = '/Users/jie_ren/Documents/SEC10K10Q/10Q_clean/10Q_output_21_150_processed.csv'
# filename = '/Users/jie_ren/Documents/SEC10K10Q/10Q_clean/10Q_output_0_150_date_missing_processed.csv'
filename = '/Users/jie_ren/Documents/SEC10K10Q/10K_clean/10K_output_400_503_processed.csv'

# save the resulting dataframe
merged_df.to_csv(filename, index=False)

