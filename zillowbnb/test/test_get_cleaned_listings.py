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

DATA = get_data.download_dataset(constants.DATASET_PROPERTIES,
                                 constants.LISTINGS_DATA)

class ListingsTest(unittest.TestCase):
    """
    This class runs unit tests for the get_cleaned_listings submodule
    """


    def test_clean_listings_row(self):
        """
        Tests cleaned_listings data for more than one row
        :param self:
        :return boolean:
        """
        listings = get_cleaned_listings.get_listings_dataframe(DATA, constants.LISTING_COLUMNS)
        self.assertTrue(listings.shape[0] >= 1)

    def test_listings_col(self):
        """
        Test cleaned_listings data has all 40 columns
        :param self:
        :return boolean:
        """
        listings = get_cleaned_listings.get_listings_dataframe(DATA, constants.LISTING_COLUMNS)
        self.assertTrue(listings.shape[1] == 40)

    def test_listings_col_types(self):
        """
        Test cleaned_listings data has the correct data column types
        :param self:
        :return boolean:
        """
        valid_types = ['int', 'O', 'O', 'float', 'float', 'O', 'O', 'int',
                       'int', 'int', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float',
                       'float', 'float', 'float', 'float', 'float', 'float', 'float']
        listings = get_cleaned_listings.get_listings_dataframe(DATA, constants.LISTING_COLUMNS)
        types = listings.dtypes
        self.assertTrue((types == valid_types).all())


if __name__ == '__main__':
    unittest.main()
