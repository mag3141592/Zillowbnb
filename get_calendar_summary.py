"""
Creates average price data using the calader data from
http://insideairbnb.com/get-the-data.html by season, weekday and weekend

Creates "calendar_price_averages.csv"

"""
import pandas as pd
import numpy as np


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
    dollars = string.translate({ord(i): None for i in "$,"})
    return float(dollars)


def create_calendar_price_averages(cal_df):
    """
    Creates calendar_price_averages.csv
    """
    # change date column from a string to a datetime
    cal_df["date"] = pd.to_datetime(cal_df["date"], format="%Y-%m-%d")

    # create season and day_type columns
    cal_df["season"] = cal_df["date"].apply(get_season)
    cal_df["day_type"] = cal_df["date"].apply(get_day_type)

    # convert currency columns to floats
    cal_df["price"] = cal_df["price"].apply(convert_currency_to_float)

    ## recreating the dataframe to have various average price metrics
    dataframe = cal_df.groupby(["listing_id", "season", "day_type"],
                               as_index=False)[["price"]].mean()

    # create temp tables for season and day_type by differnt price metrics
    seasons = dataframe.pivot_table(index="listing_id", columns="season",
                                    values="price", aggfunc=np.mean)
    day_types = dataframe.pivot_table(index="listing_id", columns="day_type",
                                      values="price", aggfunc=np.mean)

    # rename column titles and reshape tables
    seasons.columns = ["".join(i) for i in seasons.columns]
    seasons = seasons.reset_index()
    seasons = seasons.rename(columns={"fall": "fall_price",
                                      "spring": "spring_price",
                                      "summer": "summer_price",
                                      "winter": "winter_price"})

    day_types.columns = ["".join(i) for i in day_types.columns]
    day_types = day_types.reset_index()
    day_types = day_types.rename(columns={"weekend": "weekend_price",
                                          "weekday": "weekday_price"})

    # merge seasons and data_types tables
    calendar_summary = seasons.merge(day_types, on="listing_id")

    # save dataframe to a csv file
    calendar_summary.to_csv("calendar_price_averages.csv", index=False)
    return calendar_summary

# read in data
#import get_data
#CALENDAR = get_data.download_dataset('seattle', 'wa', 'united-states',
#                                     '2019-04-15', 'calendar.csv.gz')
#create_calendar_price_averages(CALENDAR)
