"""
Contains contants used throughout package
"""
import os

DATA_FOLDER = os.path.abspath('../../data')  + '/'

ADJUSTED_PRICE = 'adjusted_price'
AVAILABLE = 'available'
CITY = 'city'
COUNTRY = 'country'
DATE = 'date'
DAY_TYPE = 'day_type'
FALL = 'fall'
FALL_PRICE = 'fall_price'
LISTING_ID = 'listing_id'
MAXIMUM_NIGHTS = 'maximum_nights'
MINIMUM_NIGHTS = 'minimum_nights'
PRICE = 'price'
SEASON = 'season'
SPRING = 'spring'
SPRING_PRICE = 'spring_price'
STATE = 'state'
SUMMER = 'summer'
SUMMER_PRICE = 'summer_price'
WEEKDAY = 'weekday'
WEEKDAY_PRICE = 'weekday_price'
WEEKEND = 'weekend'
WEEKEND_PRICE = 'weekend_price'
WINTER = 'winter'
WINTER_PRICE = 'winter_price'


DATASET_PROPERTIES = {DATE:'2019-04-15',
                      CITY:'Seattle',
                      STATE:'WA',
                      COUNTRY:'United-States'}

ADDRESS = DATASET_PROPERTIES[CITY] + ', ' + DATASET_PROPERTIES[STATE]
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

CALENDAR_COLUMNS = [LISTING_ID, DATE, AVAILABLE, PRICE,
                    ADJUSTED_PRICE, MINIMUM_NIGHTS, MAXIMUM_NIGHTS]

CALENDAR_SUMMARY_COLUMNS = [LISTING_ID, FALL_PRICE, SPRING_PRICE,
                            SUMMER_PRICE, WINTER_PRICE, WEEKDAY_PRICE,
                            WEEKEND_PRICE]
