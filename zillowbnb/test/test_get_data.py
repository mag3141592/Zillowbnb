"""
Tests the input and output of get_data functions
"""
# pylint: disable=no-member
import unittest

import submodule_path # pylint: disable=E0401, W0611
import constants # pylint: disable=E0401, C0413
import get_data # pylint: disable=E0401, C0413

class UnitTest(unittest.TestCase):
    """
    5 unit test
    """

    def test_input_dictionary(self):
        """
        Tests input dictionary has required keys
        """
        dataset_properties = {'d':'2019-04-15',
                              'c':'Seattle',
                              's':'WA'}
        file = 'listings.csv.gz'
        with self.assertRaises(ValueError):
            get_data.download_dataset(dataset_properties, file)

    def test_valid_url(self):
        """
        Tests for valid data URL
        """
        file = 'listing.csv.gz'
        with self.assertRaises(ValueError):
            get_data.download_dataset(constants.DATASET_PROPERTIES, file)

    def test_output_shape(self):
        """
        Tests output dataframe has both rows and columns
        """
        data = get_data.download_dataset(constants.DATASET_PROPERTIES,
                                         constants.REVIEWS_DATA)
        rows, cols = list(data.shape)
        self.assertTrue(rows > 0 and cols > 0)

    def test_files_exist(self):
        """
        Tests input files exist
        """
        with self.assertRaises(FileNotFoundError):
            get_data.merge_data('test1.csv', 'test2.csv', 'test3.csv', 'listing_id')

#     def test_files_share_col(self):
#         """
#         Tests input files all have provided column to merge on
#         """
#         with self.assertRaises(ValueError):
#             get_data.merge_data('clean_listings.csv', 'reviews_sa_summarized.csv',
#                                 'calendar_price_averages.csv', 'test')

if __name__ == '__main__':
    unittest.main()
