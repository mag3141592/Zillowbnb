"""
Imports the raw data from http://insideairbnb.com/get-the-data.html
for Seattle, WA, United States, runs the cleaning scripts and combines the data
"""
import os
import pandas as pd

from submodule import constants as c, dataset_prediction as dp, get_data as gd
#bokeh_plot as bp
# Uncomment below if regenerating all datasets
# from submodule import get_calendar_summary, get_cleaned_listings, sentiment, train_model

# Set data folder path
DATA_FOLDER = os.path.abspath('../data')  + '/'

# Import the datafiles
CALENDAR = gd.download_dataset(c.DATASET_PROPERTIES, c.CALENDAR_DATA)
LISTINGS = gd.download_dataset(c.DATASET_PROPERTIES, c.LISTINGS_DATA)
REVIEWS = gd.download_dataset(c.DATASET_PROPERTIES, c.REVIEWS_DATA)

# Clean the calendar dataset
# Run:
# 1. CALENDAR_DF = get_calendar_summary.create_calendar_price_averages(CALENDAR)
CALENDAR_DF = DATA_FOLDER + 'calendar_price_averages.csv'

# Run sentiment analysis on review datasets
# Run: (Can take a few hours)
# 1. SENTIMENT_SCORES = polarity(REVIEWS, 'comments')
# 2. SENTIMENT_DF = summarize_sentiment(SENTIMENT_SCORES, ['listing_id'], 'compound')
SENTIMENT_DF = DATA_FOLDER + 'reviews_sa_summarized.csv'

# Clean the listings datasets
# Run:
# 1. CLEAN_LSITINGS_DF = get_cleaned_listings.get_listings_dataframe(LISTINGS, c.LISTING_COLUMNS)
CLEAN_LISTINGS_DF = pd.read_csv(DATA_FOLDER + 'clean_listings.csv')

# We will use the pretrained model below, to retrain the model:
# 1. x, y = convert_to_matrix.to_matrix(CLEAN_LISTINGS_DF, c.LISTING_COLUMNS)
# 2. train_model.train_model(x, y, c.DATASET_PROPERTIES[c.CITY])
# Get predicted price for listing datasets
PREDICTED_PRICES = dp.prediction(CLEAN_LISTINGS_DF,
                                 c.DATASET_PROPERTIES[c.CITY],
                                 c.LISTING_COLUMNS)
CLEAN_LISTINGS_DF['predicted_price'] = PREDICTED_PRICES
CLEAN_LISTINGS_DF.to_csv(DATA_FOLDER + 'clean_predicted.csv', index=False)

# Merge datasets
MERGED_DATASET = gd.merge_data(DATA_FOLDER + 'clean_predicted.csv',
                               CALENDAR_DF,
                               SENTIMENT_DF,
                               c.LISTING_ID)
# Visualization
# BOKEH variables
