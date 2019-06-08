"""
Creates average price data using the calader data from
http://insideairbnb.com/get-the-data.html by season, weekday and weekend

Creates "calendar_price_averages.csv"

"""
import pandas as pd
import numpy as np
import datetime


# create a new module for these functions.
def get_day_type(date):
    """
    Returns if a date is a weeday or weekend
    :param date datetime:
    :return string:
    """
    # check if date is a datetime.date
    if isinstance(date, datetime.date) == False:
        raise TypeError('date is not a datetime.date')

    day_type = ""
    if date.weekday() in (0, 1, 2, 3, 4):
        day_type = "weekday"
    else:
        day_type = "weekend"
    return day_type


def get_season(date):
    """
    Returns what season a date is in
    :param date datetime:
    :return string:
    """
    # check if date is a datetime.date
    if isinstance(date, datetime.date) == False:
        raise TypeError('date is not a datetime.date')

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


def convert_currency_to_float(dollar_amt):
    """
    Converts a US dollar string to a float
    :param dollar_amt string:
    :return float:
    """
    # check if dollar_amt is a string
    if isInstance(dollar_amt, str) == False:
        raise TypeError('dollar_amt is not a string')

    # removes $ at the beginning of the string, and the , in the dollars
    dollars = dollar_amt.translate({ord(i): None for i in "$,"})
    return float(dollars)


def create_calendar_price_averages(cal_df):
    """
    Cleans calendar data
    Creates average price by season and day type
    Creates calendar_price_averages.csv
    :param cal_df dataframe:
    :return dataframe:
    """
    # check if cal_df is a pd.DataFrame
    if isinstance(cal_df, pd.DataFrame) == False:
        raise TypeError('cal_df is not a pd.DataFrame')

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
