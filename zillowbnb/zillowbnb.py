"""
Imports the raw data from http://insideairbnb.com/get-the-data.html
for Seattle, WA, United States. Runs the data cleaning scripts and
combines the dataset. Trains or runs the pretrained model to predict
listing prices. Displays interactive Bokeh visualization.
"""

import os
import pandas as pd

import submodule.constants as c
import submodule.get_data as gd, submodule.price_prediction as pp

# Uncomment below if regenerating all datasets
# from submodule import convert_to_matrix as ctm, get_calendar_summary as gcs
# from submodule import get_cleaned_listings as gcl, sentiment as s, train_model as tml

# Set data folder path
DATA_FOLDER = os.path.abspath('../data')  + '/'

# Import the datafiles
CALENDAR = gd.download_dataset(c.DATASET_PROPERTIES, c.CALENDAR_DATA)
LISTINGS = gd.download_dataset(c.DATASET_PROPERTIES, c.LISTINGS_DATA)
REVIEWS = gd.download_dataset(c.DATASET_PROPERTIES, c.REVIEWS_DATA)

# Clean the calendar dataset
# Run:
# 1. CALENDAR_DF = gcs.create_calendar_price_averages(CALENDAR)
CALENDAR_DF = 'calendar_price_averages.csv'

# Run sentiment analysis on review datasets
# Run: (Can take a few hours)
# 1. SENTIMENT_SCORES = s.polarity(REVIEWS, 'comments')
# 2. SENTIMENT_DF = s.summarize_sentiment(SENTIMENT_SCORES, ['listing_id'], 'compound')
SENTIMENT_DF = 'reviews_sa_summarized.csv'

# Clean the listings datasets
# Run:
# 1. CLEAN_LSITINGS_DF = gcl.get_listings_dataframe(LISTINGS, c.LISTING_COLUMNS)
CLEAN_LISTINGS_DF = pd.read_csv(DATA_FOLDER + 'clean_listings.csv')

# We will use the pretrained model below, to retrain the model:
# 1. x, y = ctm.to_matrix(CLEAN_LISTINGS_DF, c.LISTING_COLUMNS)
# 2. tm.train_model(x, y, c.DATASET_PROPERTIES[c.CITY])
# Get predicted price for listing datasets
PREDICTED_PRICES = pp.predict_dataset(CLEAN_LISTINGS_DF,
                                      c.DATASET_PROPERTIES[c.CITY],
                                      c.LISTING_COLUMNS)
CLEAN_LISTINGS_DF['predicted_price'] = PREDICTED_PRICES
CLEAN_LISTINGS_DF.to_csv(DATA_FOLDER + 'clean_predicted.csv', index=False)

# Merge datasets
MERGED_DATASET = gd.merge_data('clean_predicted.csv',
                               CALENDAR_DF,
                               SENTIMENT_DF,
                               c.LISTING_ID,
                               DATA_FOLDER)

# Create and initializat visualization filters
