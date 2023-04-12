# SEC_filings_10K10Q

## Introduction
This dataset provides SEC filings for S&P 500 companies, which can be used for various financial analysis tasks, such as sentiment analysis, topic modeling, and more.

Please note that the dataset may reflect changes in the composition of the S&P 500 over time. For example, as of March 17th, 2023, there were 14 S&P 500 stocks that switched sectors, which may affect the weighting of sectors in the index. Here's the current weighting of sectors in the S&P 500:
| Sector                    | Weighting |
| ------------------------ | ---------|
| Technology               | 27%      |
| Health Care              | 14%      |
| Financials               | 12%      |
| Consumer Discretionary   | 11%      |
| Industrials              | 9%       |
| Communication Services   | 8%       |
| Consumer Staples         | 7%       |
| Energy                   | 5%       |
| Utilities                | 3%       |
| REITs                    | 3%       |
| Materials                | 2%       |


(Source: FactSet)

### Data Preparation
For text pre-processing, 
1. stopwords
2. lowcase 
3. remove the puncatuation
4. get root form 

#### Data Label 
- 10Q_Label Result 
![alt text](https://github.com/jieren123/SEC_filings_10K10Q/blob/main/sec10kq_Label/10q-filingsSentimentDistribution.png "10Q-Filings Sentiment Distribution")

- 10K_Label Result 
![alt text](https://github.com/jieren123/SEC_filings_10K10Q/blob/main/sec10kq_Label/10k-filingsSentimentDistribution.png "10K-Filings Sentiment Distribution")
