"""
Contains contants used throughout package
"""
import os

DATA_FOLDER = os.path.abspath('../../data')  + '/'

DATE = 'date'
CITY = 'city'
STATE = 'state'
COUNTRY = 'country'
DATASET_PROPERTIES = {DATE:'2019-04-15',
                      CITY:'Seattle',
                      STATE:'WA',
                      COUNTRY:'United-States'}

LISTINGS_DATA = 'listings.csv.gz'
REVIEWS_DATA = 'reviews.csv.gz'
CALENDAR_DATA = 'calendar.csv.gz'

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

CALENDAR_COLUMNS = ['listing_id', 'date', 'available', 'price',
                    'adjusted_price', 'minimum_nights', 'maximum_nights']

CALENDAR_SUMMARY_COLUMNS = ['listing_id', 'fall_price', 'spring_price',
                            'summer_price', 'winter_price', 'weekday_price',
                            'weekend_price']
