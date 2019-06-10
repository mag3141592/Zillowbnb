"""
This module runs unit test for converting dataframes
into matrices to be fed into the machine learning model.
"""
# pylint: disable=no-member
import unittest

import numpy as np

import submodule_path # pylint: diable=E0401l W0611
import constants as co # pylint: disable=E0401, C0413
import convert_to_matrix as cm # pylint: disable=E0401, C0413
import get_data as gd # pylint: disable=E0401, C0413
import get_cleaned_listings as gcl # pylint: disable=E0401, C0413

DATA = gd.download_dataset(co.DATASET_PROPERTIES,
                           co.LISTINGS_DATA)

DATAFRAME = gcl.get_listings_dataframe(DATA, co.LISTING_COLUMNS)

X_VAR, Y_VAR = cm.to_matrix(DATAFRAME, co.LISTING_COLUMNS)

class MatrixTest(unittest.TestCase):
    """
    This class runs unit tests for the convert_to_matrix module.
    """

    def test_to_matrix_check_dtype(self):
        """
        Tests that to_matrix will not run if datatype is not dataframe.
        :params self:
        :return boolean:
        """
        with self.assertRaises(ValueError):
            cm.to_matrix('check', co.LISTING_COLUMNS)
            cm.to_matrix(1, co.LISTING_COLUMNS)
            cm.to_matrix([1, 2, 3], co.LISTING_COLUMNS)

    def test_output_length(self):
        """
        Tests outputs for equal length
        :params self:
        :return boolean:
        """
        x_length = len(X_VAR)
        y_length = len(Y_VAR)
        self.assertTrue(x_length == y_length)

    def test_x_columns(self):
        """
        Tests columns for x
        :params self:
        :return boolean:
        """
        n_col_x = X_VAR.shape[1]
        n_col_df = len(co.LISTING_COLUMNS)
        self.assertTrue(n_col_x == (n_col_df - 2))

    def test_y_nan(self):
        """
        Tests if any nan in response variable array
        :params self:
        :return boolean:
        """
        self.assertFalse(np.isnan(Y_VAR).any())

if __name__ == '__main__':
    unittest.main()
