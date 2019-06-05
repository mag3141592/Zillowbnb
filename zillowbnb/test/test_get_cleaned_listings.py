"""
This module runs unit tests for ZillowBnb
"""
import unittest

from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)

import constants # pylint: disable=E0401
import get_data # pylint: disable=E0401
import get_cleaned_listings # pylint: disable-all

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

DATA = get_data.download_dataset(DATASET_PROPERTIES, 'listings.csv.gz')

class ListingsTest(unittest.TestCase):
    """
    This class runs unit tests for the get_cleaned_listings submodule
    """


    def test_clean_listings_row(self):
        """
        Tests cleaned_listings data for more than one row
        """
        listings = get_cleaned_listings.get_listings_dataframe(DATA, LISTING_COLUMNS)
        self.assertTrue(listings.shape[0] >= 1)

    def test_listings_col(self):
        """
        Test cleaned_listings data has all 40 columns
        """
        listings = get_cleaned_listings.get_listings_dataframe(DATA, LISTING_COLUMNS)
        self.assertTrue(listings.shape[1] == 40)

    def test_listings_col_types(self):
        """
        Test cleaned_listings data has the correct data column types
        """
        valid_types = ['int', 'O', 'O', 'float', 'float', 'O', 'O', 'int',
                       'int', 'int', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float', 'float']
        listings = get_cleaned_listings.get_listings_dataframe(DATA, LISTING_COLUMNS)
        types = listings.dtypes
        self.assertTrue((types == valid_types).all())


if __name__ == '__main__':
    unittest.main()
