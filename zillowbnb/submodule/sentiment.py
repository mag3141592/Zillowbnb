"""
Uses Vadar Sentiment Analysis to calculate the polarity of text.
"""
import constants

import nltk
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def polarity(dataframe, review_column):
    """
    Takes a dataframe and the column name containing text to calculate the
    sentiment polarity of. Calculates polarity then appends to existing
    dataframe to return.

    :params dataframe dataframe:
    :params review_column string:
    :returns dataframe:
    """
    # Datatype checks
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("dataframe is not a pandas dataframe")
    if not isinstance(review_column, str):
        raise ValueError("review_column is not a string")
    if not review_column in dataframe:
        raise ValueError("review_column is not in the dataframe")

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

    :params dataframe dataframe:
    :params group_on_list list:
    :params avg_over_column string:
    :returns dataframe:
    """
    # Datatype checks
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("dataframe is not a pandas dataframe")
    if not isinstance(group_on_list, list):
        raise ValueError("group_on_list is not a list")
    if not isinstance(avg_over_column, str):
        raise ValueError("avg_over_column is not a string")

    all_columns = group_on_list + [avg_over_column]
    results = dataframe[all_columns].groupby(group_on_list).agg(
                {avg_over_column : ['mean', 'var', 'count']})
    results = results[avg_over_column].reset_index()
    results.to_csv(constants.DATA_FOLDER + 'reviews_sa_summarized.csv', index=False)
    return results
