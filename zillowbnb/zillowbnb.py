"""

Imports the raw data from http://insideairbnb.com/get-the-data.html

for Seattle, WA, United States, runs the cleaning scripts and combines the data

"""

import get_data

import get_calendar_summary

import convert_to_matrix

import get_cleaned_listings

import sentiment

# need something for running model and saves coefficents

#column selection
columns = ['id', 'neighbourhood_cleansed', 'neighbourhood_group_cleansed',
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



# Clean LISTINGS
clean_listings = get_cleaned_listings.get_listings_dataframe(LISTINGS, columns, write_csv=True)

# convert Listings to convert_to_matrix
listings_matrix = convert_to_matrix.to_matrix(clean_listings)

# run sentiment analysis
REVIEWS_DATESET = REVIEWS.dropna()
SENTIMENT_SCORES = sentiment.polarity(REVIEWS_DATESET, 'comments')
SENTIMENT_SUMMARIZED = sentiment.summarize_sentiment(SENTIMENT_SCORES, ['listing_id'], 'compound')

# run calendar_summary
get_calendar_summary.create_calendar_price_averages(CALENDAR)



# Merge data

# different if each returns a dataframe than if they write .csvs
clean_listings = pd.read_csv('clean_listings.csv')
reviews = pd.read_csv('calendar_price_averages.csv')
calendar = pd.read_csv('reviews_sa_summarized.csv')

merged1 = clean_listings.merge(reviews, on='listing_id')
final_merged = merged1.merge(calendar, on='listing_id')
final_merged.to_csv('final_merged.csv', index=False)


# call model coefficents??
