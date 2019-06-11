"""
Tests the input and output of get_data functions
"""
import unittest
import os

import zillowbnb.test.submodule_path
import constants as c
import get_data as gd

DATA_FOLDER = os.path.abspath('data')  + '/'
FILE1 = 'clean_predicted.csv'
FILE2 = 'reviews_sa_summarized.csv'
FILE3 = 'calendar_price_averages.csv'

class UnitTest(unittest.TestCase):
    """
    6 unit test for gd.download_dataset and gd.merge_data
    """

    def test_input_dictionary(self):
        """
        Tests input dictionary has required keys
        """
        dataset_properties = {'d':'2019-04-15',
                              'c':'Seattle',
                              's':'WA'}
        file = c.LISTINGS_DATA
        with self.assertRaises(ValueError):
            gd.download_dataset(dataset_properties, file)

    def test_valid_url(self):
        """
        Tests for valid data URL
        """
        file = 'listing.csv.gz'
        with self.assertRaises(ValueError):
            gd.download_dataset(c.DATASET_PROPERTIES, file)

    def test_gd_output_shape(self):
        """
        Tests output dataframe has both rows and columns
        """
        data = gd.download_dataset(c.DATASET_PROPERTIES,
                                   c.REVIEWS_DATA)
        rows, cols = list(data.shape)
        self.assertTrue(rows > 0 and cols > 0)

    def test_files_exist(self):
        """
        Tests input files exist
        """
        with self.assertRaises(FileNotFoundError):
            gd.merge_data('test1.csv', 'test2.csv', 'test3.csv', 'listing_id')

    def test_files_share_col(self):
        """
        Tests input files all have provided column to merge on
        """
        with self.assertRaises(ValueError):
            gd.merge_data(FILE1, FILE2, FILE3, 'test', DATA_FOLDER)

    def test_merge_data_output_shape(self):
        """
        Tests output dataframe has both rows and columns
        """
        data = gd.merge_data(FILE1, FILE2, FILE3, c.LISTING_ID, DATA_FOLDER)
        rows, cols = list(data.shape)
        self.assertTrue(rows > 0 and cols > 0)

if __name__ == '__main__':
    unittest.main()
