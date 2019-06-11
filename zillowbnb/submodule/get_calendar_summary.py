"""
Creates average price data using the calader data from
http://insideairbnb.com/get-the-data.html by season, weekday and weekend

Creates "calendar_price_averages.csv"

"""

# pylint: disable=no-member
import datetime
import pandas as pd
import numpy as np
import submodule.constants


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
        day_type = constants.WEEKDAY
    else:
        day_type = constants.WEEKEND
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
        month = constants.WINTER
    elif(date.month == 3 or date.month == 4 or date.month == 5):
        month = constants.SPRING
    elif(date.month == 6 or date.month == 7 or date.month == 8):
        month = constants.SUMMER
    else:
        month = constants.FALL
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
    cal_df[constants.DATE] = pd.to_datetime(cal_df[constants.DATE],
                                            format="%Y-%m-%d")

    # create season and day_type columns
    cal_df[constants.SEASON] = cal_df[constants.DATE].apply(get_season)
    cal_df[constants.DAY_TYPE] = cal_df[constants.DATE].apply(get_day_type)

    # convert currency columns to floats
    cal_df[constants.PRICE] = cal_df[constants.PRICE].apply(convert_currency_to_float)

    ## recreating the dataframe to have various average price metrics
    dataframe = cal_df.groupby([constants.LISTING_ID, constants.SEASON,
                                constants.DAY_TYPE],
                               as_index=False)[[constants.PRICE]].mean()

    # create temp tables for season and day_type by differnt price metrics
    seasons = dataframe.pivot_table(index=constants.LISTING_ID,
                                    columns=constants.SEASON,
                                    values=constants.PRICE, aggfunc=np.mean)
    day_types = dataframe.pivot_table(index=constants.LISTING_ID,
                                      columns=constants.DAY_TYPE,
                                      values=constants.PRICE, aggfunc=np.mean)

    # rename column titles and reshape tables
    seasons.columns = ["".join(i) for i in seasons.columns]
    seasons = seasons.reset_index()
    seasons = seasons.rename(columns={constants.FALL: constants.FALL_PRICE,
                                      constants.SPRING: constants.SPRING_PRICE,
                                      constants.SUMMER: constants.SUMMER_PRICE,
                                      constants.WINTER: constants.WINTER_PRICE})

    day_types.columns = ["".join(i) for i in day_types.columns]
    day_types = day_types.reset_index()
    day_types = day_types.rename(columns={constants.WEEKEND: constants.WEEKEND_PRICE,
                                          constants.WEEKDAY:constants.WEEKDAY_PRICE})

    # merge seasons and data_types tables
    calendar_summary = seasons.merge(day_types, on=constants.LISTING_ID)

    # save dataframe to a csv file
    calendar_summary.to_csv('../data/' + 'calendar_price_averages.csv', index=False)
    return calendar_summary
