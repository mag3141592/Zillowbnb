"""
Creates average price data using the calader data from
http://insideairbnb.com/get-the-data.html by season, weekday and weekend

Creates "calendar_price_averages.csv"

"""

import datetime
import pandas as pd
import numpy as np
import constants as c

# create a new module for these functions.
def get_day_type(date):
    """
    Returns if a date is a weeday or weekend
    :param date datetime:
    :return string:
    """
    # check if date is a datetime.date
    if not isinstance(date, datetime.date):
        raise TypeError('date is not a datetime.date')

    day_type = ""
    if date.weekday() in (0, 1, 2, 3, 4):
        day_type = c.WEEKDAY
    else:
        day_type = c.WEEKEND
    return day_type


def get_season(date):
    """
    Returns what season a date is in
    :param date datetime:
    :return string:
    """
    # check if date is a datetime.date
    if not isinstance(date, datetime.date):
        raise TypeError('date is not a datetime.date')

    month = ""
    if(date.month == 12 or date.month == 1 or date.month == 2):
        month = c.WINTER
    elif(date.month == 3 or date.month == 4 or date.month == 5):
        month = c.SPRING
    elif(date.month == 6 or date.month == 7 or date.month == 8):
        month = c.SUMMER
    else:
        month = c.FALL
    return month


def convert_currency_to_float(dollar_amt):
    """
    Converts a US dollar string to a float
    :param dollar_amt string:
    :return float:
    """
    # check if dollar_amt is a string
    if not isinstance(dollar_amt, str):
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
    if not isinstance(cal_df, pd.DataFrame):
        raise TypeError('cal_df is not a pd.DataFrame')

    # change date column from a string to a datetime
    cal_df[c.DATE] = pd.to_datetime(cal_df[c.DATE],
                                    format="%Y-%m-%d")

    # create season and day_type columns
    cal_df[c.SEASON] = cal_df[c.DATE].apply(get_season)
    cal_df[c.DAY_TYPE] = cal_df[c.DATE].apply(get_day_type)

    # convert currency columns to floats
    cal_df[c.PRICE] = cal_df[c.PRICE].apply(convert_currency_to_float)

    ## recreating the dataframe to have various average price metrics
    dataframe = cal_df.groupby([c.LISTING_ID, c.SEASON,
                                c.DAY_TYPE],
                               as_index=False)[[c.PRICE]].mean()

    # create temp tables for season and day_type by differnt price metrics
    seasons = dataframe.pivot_table(index=c.LISTING_ID,
                                    columns=c.SEASON,
                                    values=c.PRICE, aggfunc=np.mean)
    day_types = dataframe.pivot_table(index=c.LISTING_ID,
                                      columns=c.DAY_TYPE,
                                      values=c.PRICE, aggfunc=np.mean)

    # rename column titles and reshape tables
    seasons.columns = ["".join(i) for i in seasons.columns]
    seasons = seasons.reset_index()
    seasons = seasons.rename(columns={c.FALL: c.FALL_PRICE,
                                      c.SPRING: c.SPRING_PRICE,
                                      c.SUMMER: c.SUMMER_PRICE,
                                      c.WINTER: c.WINTER_PRICE})

    day_types.columns = ["".join(i) for i in day_types.columns]
    day_types = day_types.reset_index()
    day_types = day_types.rename(columns={c.WEEKEND: c.WEEKEND_PRICE,
                                          c.WEEKDAY:c.WEEKDAY_PRICE})

    # merge seasons and data_types tables
    calendar_summary = seasons.merge(day_types, on=c.LISTING_ID)

    # save dataframe to a csv file
    # calendar_summary.to_csv('../data/' + 'calendar_price_averages.csv', index=False)
    return calendar_summary
