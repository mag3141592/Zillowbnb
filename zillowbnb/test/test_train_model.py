"""
This module runs unit test for training the machine learning model.
"""

import unittest

import zillowbnb.test.submodule_path

import constants as co
import convert_to_matrix as cm
import get_data as gd
import get_cleaned_listings as gcl
import train_model as tm

DATA = gd.download_dataset(co.DATASET_PROPERTIES,
                           co.LISTINGS_DATA)

DATAFRAME = gcl.get_listings_dataframe(DATA, co.LISTING_COLUMNS)

X_VAR, Y_VAR = cm.to_matrix(DATAFRAME, co.LISTING_COLUMNS)

class TrainModelTest(unittest.TestCase):
    """
    This class runs unit tests for the train_model module.
    """

    def test_input_size(self):
        """
        Tests that train_model will not run if sizes of x_var and y_var
        do not match.
        :params self:
        :returns boolean:
        """
        with self.assertRaises(IndexError):
            tm.train_model(X_VAR[:500], Y_VAR, 'Hawaii')
            tm.train_model(X_VAR, Y_VAR[:500], 'Hawaii')

    def test_x_input_dtype(self):
        """
        Test that train_model will not run with wrong data types for x_var
        :params self:
        :returns boolean
        """
        with self.assertRaises(AttributeError):
            tm.train_model(1, Y_VAR, 'Hawaii')
            tm.train_model('check', Y_VAR, 'Hawaii')

    def test_y_input_dtype(self):
        """
        Tests that train_model will not run with wrong data types for y_var.
        :params self:
        :returns boolean:
        """
        with self.assertRaises(TypeError):
            tm.train_model(X_VAR, 1, 'Hawaii')
            tm.train_model(X_VAR, 'check', 'Hawaii')

if __name__ == '__main__':
    unittest.main()
