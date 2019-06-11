"""
This module runs unit tests for ZillowBnb
"""
# pylint: disable=no-member
import unittest

import zillowbnb.test.submodule_path # pylint: disable=E0401, W0611
import constants # pylint: disable=E0401, C0413
import get_data # pylint: disable=E0401, C0413
import get_cleaned_listings # pylint: disable=E0401, C0413

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

    def test_wrong_check_dtype(self):
        """
        Tests that get_listings_dataframe will not run if datatypes are incorrect
        :param self:
        :return boolean:
        """
        with self.assertRaises(ValueError):
            get_cleaned_listings.get_listings_dataframe('Incorrect', constants.LISTING_COLUMNS)

if __name__ == '__main__':
    unittest.main()
