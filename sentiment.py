"""
Uses Vadar Sentiment Analysis to calculate the polarity of text.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
nltk.download('vader_lexicon')

def polarity(dataframe, review_column):
    """
    Takes a dataframe and the column name containing text to calculate the
    sentiment polarity of. Calculates polarity then appends to existing
    dataframe to return.
    """
    dataframe = dataframe.dropna()
    rows = dataframe.shape[0]
    scores_array = np.zeros([rows, 4])
    keys = []

    index_1 = 0
    for review in dataframe[review_column]:
        scores = SentimentIntensityAnalyzer().polarity_scores(review)
        scores_array[index_1] = list(scores.values())
        if index_1 == 0:
            keys = list(scores.keys())
        index_1 += 1

    index_2 = 0
    for k in keys:
        dataframe[k] = scores_array[:, index_2]
        index_2 += 1

    return dataframe

def summarize_sentiment(dataframe, group_on_list, avg_over_column):
    """
    Takes a dataframe, a list of columns you wish to group, and the column to be
    summarized.  Calculates the mean, variance, and count of the summarized
    column. Outputs the summarized dataframe to a .csv and returns the dataframe.
    """
    all_columns = group_on_list + [avg_over_column]
    results = dataframe[all_columns].groupby(group_on_list).agg(
                {avg_over_column : ['mean', 'var', 'count']})
    results = results[avg_over_column].reset_index()
    results.to_csv('reviews_sa_summarized.csv', index=False)
    return results

# REVIEWS_DATESET = get_data.download_dataset('seattle', 'wa',
#                                             'united states', '2019-04-15', 'reviews.csv.gz')
# REVIEWS_DATESET = REVIEWS_DATESET.dropna()
# SENTIMENT_SCORES = polarity(REVIEWS_DATESET, 'comments')
# SENTIMENT_SUMMARIZED = summarize_sentiment(SENTIMENT_SCORES, ['listing_id'], 'compound')