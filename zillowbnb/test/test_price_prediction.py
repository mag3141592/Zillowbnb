"""
This module runs unit test for converting dataframes
into matrices to be fed into the machine learning model.
"""
import unittest

from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)


import constants as co # pylint: disable=E0401
import convert_to_matrix as cm # pylint: disable=E0401
import get_data as gd # pylint: disable=E0401
import get_cleaned_listings as gcl # pylint: disable=E0401
import price_prediction as pp

DATA = gd.download_dataset(co.DATASET_PROPERTIES,
                           co.LISTINGS_DATA)

DATAFRAME = gcl.get_listings_dataframe(DATA, co.LISTING_COLUMNS)

X_VAR, Y_VAR = cm.to_matrix(DATAFRAME, co.LISTING_COLUMNS)

class PricePredictionTest(unittest.TestCase):
    """
    This class runs unit tests for the price_prediction module.
    """

    def test_output_length_1(self):
        """
        Tests that output has same length as input
        :params self:
        :returns boolean:
        """
        y_length = len(Y_VAR)
        output = pp.prediction(X_VAR, co.DATASET_PROPERTIES[co.CITY])
        output_length = len(output)
        self.assertTrue(y_length == output_length)

    def test_output_length_2(self):
        """
        Tests that output has same length as input
        when using only 1 row.
        :params self:
        :returns boolean:
        """
        x_one = X_VAR[0]
        y_one = [Y_VAR[0]]
        y_one_length = len(y_one)
        output = pp.prediction(x_one, co.DATASET_PROPERTIES[co.CITY])
        output_length = len(output)
        self.assertTrue(y_one_length == output_length)

    def test_output_length_3(self):
        """
        Test that output has same length as input
        when using a subset of the data.
        :params self:
        :returns boolean:
        """
        x_subset = X_VAR[0:20]
        y_subset = Y_VAR[0:20]
        y_subset_length = len(y_subset)
        output = pp.prediction(x_subset, co.DATASET_PROPERTIES[co.CITY])
        output_length = len(output)
        self.assertTrue(y_subset_length == output_length)


    def test_prediction_check_file(self):
        """
        Tests that prediction will not run if file containing model
        does not exists.
        :params self:
        :returns boolean:
        """
        with self.assertRaises(FileNotFoundError):
            pp.prediction(X_VAR, 'Colorado')
            pp.prediction(X_VAR, 'Boston')
            pp.prediction(X_VAR, 'check')
            pp.prediction(X_VAR, 1)

    def test_price_check_input(self):
        """
        Test that prediction will not run if input is not array.
        :params self:
        :returns boolean:
        """
        with self.assertRaises(AttributeError):
            pp.prediction('check', co.DATASET_PROPERTIES[co.CITY])
            pp.prediction(1, co.DATASET_PROPERTIES[co.CITY])
            pp.prediction([1, 2, 3], co.DATASET_PROPERTIES[co.CITY])

if __name__ == '__main__':
    unittest.main()
