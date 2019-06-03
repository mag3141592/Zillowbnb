"""

Imports the raw data from http://insideairbnb.com/get-the-data.html

for Seattle, WA, United States, runs the cleaning scripts and combines the data

"""

import get_data


# need something for running model and saves coefficents

#The columns used for the listings dataset
LISTING_COLUMNS = ['id', 'neighbourhood_cleansed', 'neighbourhood_group_cleansed',
           'latitude', 'longitude', 'property_type', 'room_type',
           'minimum_nights', 'maximum_nights',
           'accommodates', 'bathrooms', 'bedrooms', 'beds', 'amenities_TV',
           'amenities_Heating', 'amenities_Air conditioning', 'amenities_Breakfast',
           'amenities_Laptop friendly workspace', 'amenities_Indoor fireplace',
           'amenities_Iron', 'amenities_Hair dryer', 'amenities_Private entrance',
           'amenities_Smoke detector', 'amenities_Carbon monoxide detector',
           'amenities_First aid kit', 'amenities_Fire extinguisher',
           'amenities_Lock on bedroom door', 'amenities_Pool',
           'amenities_Kitchen', 'amenities_Washer', 'amenities_Dryer',
           'amenities_Free parking on premises', 'amenities_Elevator',
           'amenities_Hot tub', 'amenities_Gym', 'amenities_Pets allowed',
           'amenities_Smoking allowed', 'amenities_Suitable for events',
           'amenities_Pets live on this property', 'price']

# import the datafiles
CALENDAR = get_data.download_dataset("seattle", "wa", "united-states",

                                     "2019-04-15", "calendar.csv.gz")

LISTINGS = get_data.download_dataset("seattle", "wa", "united-states",

                                     "2019-04-15", "listings.csv.gz")

REVIEWS = get_data.download_dataset("seattle", "wa", "united-states",

                                     "2019-04-15", "reviews.csv.gz")


# Create generated data csv files. Comment out if already exists in folder
# Takes a long time to run to get the sentiment scores
'''
get_data.generate_cleaned_data(LISTINGS, LISTING_COLUMNS, REVIEWS, CALENDAR)
'''

# Merge data. Generated data csvs must already exist.
final_merge_df = get_data.merge_data()


# call model coefficents??
