"""
This module runs unit tests for detecting outliers
"""
import unittest

from os.path import dirname, abspath, join
import sys
import numpy as np

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)

import constants as co # pylint: disable=E0401, C0413
import convert_to_matrix as cm # pylint: disable=E0401, C0413
import detect_outliers as do # pylint: disable=E0401, C0413
import get_data as gd # pylint: disable=E0401, C0413
import get_cleaned_listings as gcl # pylint: disable=E0401, C0413

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
