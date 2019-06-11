"""
This module runs unit tests for detecting outliers
"""
import unittest

import numpy as np

import zillowbnb.test.submodule_path

import constants as co
import convert_to_matrix as cm
import detect_outliers as do
import get_data as gd
import get_cleaned_listings as gcl

DATA = gd.download_dataset(co.DATASET_PROPERTIES, co.LISTINGS_DATA)

DATAFRAME = gcl.get_listings_dataframe(DATA, co.LISTING_COLUMNS)

X_VAR, Y_VAR = cm.to_matrix(DATAFRAME, co.LISTING_COLUMNS)

class OutlierTest(unittest.TestCase):
    """
    This class runs unit tests for the detect_outliers module.
    """

    def test_outlier__exists(self):
        """
        Tests if outliers exist
        :params self:
        :return boolean:
        """
        outliers = do.detect_outlier(Y_VAR)
        n_outliers = len(outliers)
        self.assertTrue(n_outliers > 0)


    def test_outlier_greater(self):
        """
        Tests smallest outlier greater than mean.
        :params self:
        :return boolean:
        """
        outliers = do.detect_outlier(Y_VAR)
        outlier_boundary = min(outliers)
        mean_value = np.mean(Y_VAR)
        self.assertTrue(outlier_boundary > mean_value)


if __name__ == '__main__':
    unittest.main()
