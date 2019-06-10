"""
This module runs unit test for converting dataframes
into matrices to be fed into the machine learning model.
"""
# pylint: disable=no-member
import unittest

import numpy as np


import submodule_path # pylint: disable=E0401, W0611

import constants as con # pylint: disable=E0401, C0413
import convert_to_matrix as ctm # pylint: disable=E0401, C0413
import get_data as gdt # pylint: disable=E0401, C0413
import get_cleaned_listings as gl # pylint: disable=E0401, C0413

DATA = gdt.download_dataset(con.DATASET_PROPERTIES,
                            con.LISTINGS_DATA)

DATAFRAME = gl.get_listings_dataframe(DATA, con.LISTING_COLUMNS)

X_VAR, Y_VAR = ctm.to_matrix(DATAFRAME, con.LISTING_COLUMNS)

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
            ctm.to_matrix('check', con.LISTING_COLUMNS)
            ctm.to_matrix(1, con.LISTING_COLUMNS)
            ctm.to_matrix([1, 2, 3], con.LISTING_COLUMNS)

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
        n_col_df = len(con.LISTING_COLUMNS)
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
