"""
This module runs unit tests for ZillowBnb
"""
import unittest
from zillowbnb.submodule import get_data
from zillowbnb.submodule import get_cleaned_listings

DATASET_PROPERTIES = {'date':'2019-04-15',
                      'city':'Seattle',
                      'state':'WA',
                      'country':'United-States'}

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

class ListingsTest(unittest.TestCase):
    """
    This class runs unit tests for the get_cleaned_listings submodule
    """


    def test_listings_more_than_one_row(self):
        """
        Tests listings.csv.gz data for more than one row
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'listings.csv.gz')
        self.assertTrue(data.shape[0] >= 1)

    def test_clean_listings_row(self):
        """
        Tests cleaned_listings data for more than one row
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'listings.csv.gz')
        listings = get_cleaned_listings.get_listings_dataframe(data, LISTING_COLUMNS)
        self.assertTrue(listings.shape[0] >= 1)

    def test_listings_col(self):
        """
        Test cleaned_listings data has all 40 columns
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'listings.csv.gz')
        listings = get_cleaned_listings.get_listings_dataframe(data, LISTING_COLUMNS)
        self.assertTrue(listings.shape[1] == 40)

    def test_listings_col_types(self):
        """
        Test cleaned_listings data has the correct data column types
        """
        valid_types = ['int','O','O','float','float','O','O','int',
                       'int','int','float','float','float','float','float',
                       'float','float','float','float','float','float',
                       'float','float','float','float','float','float',
                       'float','float','float','float','float','float',
                       'float','float','float','float','float','float','float']
        data = get_data.download_dataset(DATASET_PROPERTIES, 'listings.csv.gz')
        listings = get_cleaned_listings.get_listings_dataframe(data, LISTING_COLUMNS)
        types = listings.dtypes
        self.assertTrue((types == valid_types).all())


if __name__ == '__main__':
    unittest.main()
