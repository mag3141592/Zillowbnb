"""
Note: creates "calendar_price_averages.csv"

"""
import pandas as pd
import numpy as np
import datetime
import re

# read in data
CALENDAR = pd.read_csv("calendar.csv")

# create a new module for these functions.
def get_day_type(date):
    day_type = ""
    if(date.weekday() in (0, 1, 2, 3, 4)):
        day_type = "weekday"
    else:
        day_type = "weekend"
    return day_type


def get_season(date):
    month = ""
    if(date.month == 12 or date.month == 1 or date.month == 2):
        month = "winter"
    elif(date.month == 3 or date.month == 4 or date.month == 5):
        month = "spring"
    elif(date.month ==6 or date.month ==7 or date.month ==8):
        month = "summer"
    else:
        month == "fall"
    return month


def convert_currency_to_float(string):
    dollars = string.translate({ord(i): None for i in '$,'})
    return float(dollars)


# change date column from a string to a datetime
CALENDAR['date'] = pd.to_datetime(CALENDAR['date'], format='%Y-%m-%d')

# create season and day_type columns
CALENDAR['season'] = CALENDAR['date'].apply(get_season)
CALENDAR['day_type'] = CALENDAR['date'].apply(get_day_type)

# convert currency columns to floats
CALENDAR["price"] = CALENDAR["price"].apply(convert_currency_to_float)
CALENDAR["adjusted_price"] = CALENDAR["adjusted_price"].apply(convert_currency_to_float)

## recreating the dataframe to have various average price metrics
df = CALENDAR.groupby(['listing_id','season', 'day_type'], as_index = False)[['price', "adjusted_price"]].mean()

# create temp tables for season and day_type by differnt price metrics
temp  = df.pivot_table(index = "listing_id", columns = "season", values = "price", aggfunc=np.mean)
temp1 = df.pivot_table(index = "listing_id", columns = "season", values = "adjusted_price", aggfunc=np.mean)
temp2 = df.pivot_table(index = "listing_id", columns = "day_type", values = "price", aggfunc=np.mean)
temp3 = df.pivot_table(index = "listing_id", columns = "day_type", values = "adjusted_price", aggfunc=np.mean)

# rename column titles and reshape tables
temp.columns = ["".join(i) for i in temp.columns]
temp = temp.reset_index()
temp = temp.rename(columns = {"fall": "fall_price",
                      "spring": "spring_price",
                      "summer": "summer_price",
                      "winter": "winter_price"})

temp1.columns = ["".join(i) for i in temp1.columns]
temp1 = temp1.reset_index()
temp1 = temp1.rename(columns = {"fall": "fall_adjusted_price",
                      "spring": "spring_adjusted_price",
                      "summer": "summer_adjusted_price",
                      "winter": "winter_adjusted_price"})

temp2.columns = ["".join(i) for i in temp2.columns]
temp2 = temp2.reset_index()
temp2 = temp2.rename(columns = {"weekend": "weekend_price",
                                "weekday": "weekday_price"})

temp3.columns = ["".join(i) for i in temp3.columns]
temp3 = temp3.reset_index()
temp3 = temp3.rename(columns = {"weekend": "weekend_adjusted_price",
                                "weekday": "weekday_adjusted_price"})

# merge season tables
seasons_table = temp.merge(temp1, on = "listing_id")

# merge day_type tables
day_types_table = temp2.merge(temp3, on = "listing_id")

# merge seasons and data_types tables
final = seasons_table.merge(day_types_table, on = "listing_id")

# save dataframe to a csv file
final.to_csv("calendar_price_averages.csv")
