"""
This module runs unit test for converting dataframes
into matrices to be fed into the machine learning model.
"""
import unittest
import numpy as np

import zillowbnb.test.submodule_path
import constants as co
import convert_to_matrix as cm
import get_data as gd
import get_cleaned_listings as gcl
import host_predict as hp

HOST_DATA = gd.download_dataset(co.DATASET_PROPERTIES,
                                co.LISTINGS_DATA)

HOST_DATAFRAME = gcl.get_listings_dataframe(HOST_DATA, co.LISTING_COLUMNS)

X_VAR, Y_VAR = cm.to_matrix(HOST_DATAFRAME, co.LISTING_COLUMNS)

class HostPredictTest(unittest.TestCase):
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
        output = hp.predict_input(X_VAR, co.DATASET_PROPERTIES[co.CITY])
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
        output = hp.predict_input(x_one, co.DATASET_PROPERTIES[co.CITY])
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
        output = hp.predict_input(x_subset, co.DATASET_PROPERTIES[co.CITY])
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
            hp.predict_input(X_VAR, 'Colorado')
            hp.predict_input(X_VAR, 'Boston')
            hp.predict_input(X_VAR, 'check')
            hp.predict_input(X_VAR, 1)

    def test_price_check_input(self):
        """
        Test that prediction will not run if input is not array.
        :params self:
        :returns boolean:
        """
        with self.assertRaises(AttributeError):
            hp.predict_input('check', co.DATASET_PROPERTIES[co.CITY])
            hp.predict_input(1, co.DATASET_PROPERTIES[co.CITY])
            hp.predict_input([1, 2, 3], co.DATASET_PROPERTIES[co.CITY])

if __name__ == '__main__':
    unittest.main()
