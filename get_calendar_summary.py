"""
Creates average price data using the calader data from
http://insideairbnb.com/get-the-data.html by season, weekday and weekend

Creates "calendar_price_averages.csv"

"""
#import datetime
#import re
import pandas as pd
import numpy as np


# read in data
CALENDAR = pd.read_csv("calendar.csv")

# create a new module for these functions.
def get_day_type(date):
    """
    Takes a date and returns if that day was a weekend or weekday
    """
    day_type = ""
    if date.weekday() in (0, 1, 2, 3, 4):
        day_type = "weekday"
    else:
        day_type = "weekend"
    return day_type


def get_season(date):
    """
    Takes a date and returns the season that day was in
    """
    month = ""
    if(date.month == 12 or date.month == 1 or date.month == 2):
        month = "winter"
    elif(date.month == 3 or date.month == 4 or date.month == 5):
        month = "spring"
    elif(date.month == 6 or date.month == 7 or date.month == 8):
        month = "summer"
    else:
        month = "fall"
    return month


def convert_currency_to_float(string):
    """
    Takes in a string representing currency and removes the $ and , and returns
    a float
    """
    dollars = string.translate({ord(i): None for i in '$,'})
    return float(dollars)


# change date column from a string to a datetime
CALENDAR['date'] = pd.to_datetime(CALENDAR['date'], format='%Y-%m-%d')

# create season and day_type columns
CALENDAR['season'] = CALENDAR['date'].apply(get_season)
CALENDAR['day_type'] = CALENDAR['date'].apply(get_day_type)

# convert currency columns to floats
CALENDAR["price"] = CALENDAR["price"].apply(convert_currency_to_float)

## recreating the dataframe to have various average price metrics
DATAFRAME = CALENDAR.groupby(['listing_id', 'season', 'day_type'],
                             as_index=False)[['price', "adjusted_price"]].mean()

# create temp tables for season and day_type by differnt price metrics
SEASONS_TABLE = DATAFRAME.pivot_table(index="listing_id", columns="season",
                                      values="price", aggfunc=np.mean)
DAY_TYPE_TABLE = DATAFRAME.pivot_table(index="listing_id", columns="day_type",
                                       values="price", aggfunc=np.mean)

# rename column titles and reshape tables
SEASONS_TABLE.columns = ["".join(i) for i in SEASONS_TABLE.columns]
SEASONS_TABLE = SEASONS_TABLE.reset_index()
SEASONS_TABLE = SEASONS_TABLE.rename(columns={"fall": "fall_price",
                                              "spring": "spring_price",
                                              "summer": "summer_price",
                                              "winter": "winter_price"})

DAY_TYPE_TABLE.columns = ["".join(i) for i in DAY_TYPE_TABLE.columns]
DAY_TYPE_TABLE = DAY_TYPE_TABLE.reset_index()
DAY_TYPE_TABLE = DAY_TYPE_TABLE.rename(columns={"weekend": "weekend_price",
                                                "weekday": "weekday_price"})

# merge seasons and data_types tables
CALENDAR_SUMMARY = SEASONS_TABLE.merge(DAY_TYPE_TABLE, on="listing_id")

# save dataframe to a csv file
CALENDAR_SUMMARY.to_csv("calendar_price_averages.csv")
