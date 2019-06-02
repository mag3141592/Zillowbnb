"""

Imports the raw data from http://insideairbnb.com/get-the-data.html

for Seattle, WA, United States, runs the cleaning scripts and combines the data

"""

import get_data

import get_calendar_summary

import convert_to_matrix

import cleanup_data

import sentiment

# need something for running model and saves coefficents



# import the datafiles

CALENDAR = get_data.download_dataset("seattle", "wa", "united-states",

                                     "2019-04-15", "calendar.csv.gz")

LISTINGS = get_data.download_dataset("seattle", "wa", "united-states",

                                     "2019-04-15", "listings.csv.gz")

REVIEWS = get_data.download_dataset("seattle", "wa", "united-states",

                                     "2019-04-15", "reviews.csv.gz")



# Clean LISTINGS

## returns a df

## or writes a .csv



# convert Listings to convert_to_matrix

## returns a dataframe

## or writes a .csv



# run sentiment analysis

## reutrns a dataframe

## or writes a .csv



# run calendar_summary

## returns a dataframe

## or writes a .csv



# Merge data

# different if each returns a dataframe than if they write .csvs



# call model coefficents??
