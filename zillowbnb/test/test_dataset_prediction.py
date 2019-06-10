"""
This module runs unit tests for predicting price
for an entire dataset.
"""

import unittest

# import submodule_path # pylint: disable=W0611, E0401
from os.path import dirname, abspath, join
import sys
import numpy as np

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)

import constants as co # pylint: disable=E0401
import convert_to_matrix as cm # pylint: disable=E0401
import dataset_prediction as dp # pylint: disable=E0401
import get_data as gd # pylint: disable=E0401
import get_cleaned_listings as gcl # pylint: disable-all

DATA = gd.download_dataset(co.DATASET_PROPERTIES,
                           co.LISTINGS_DATA)

DATAFRAME = gcl.get_listings_dataframe(DATA, co.LISTING_COLUMNS)

X_VAR, Y_VAR = cm.to_matrix(DATAFRAME, co.LISTING_COLUMNS)

PREDICTIONS = dp.predict_dataset(DATAFRAME,
                            co.DATASET_PROPERTIES[co.CITY],
                            co.LISTING_COLUMNS)

class DatasetPredictionTest(unittest.TestCase):
    """
    This class runs unit tests for the test_dataset_prediction module.
    """

    def test_output_length(self):
        """
        Tests output length equal to dataset length
        :params self:
        :return boolean:
        """
        y_length = len(Y_VAR)
        predictions_length = len(PREDICTIONS)
        self.assertTrue(y_length == predictions_length)

    def test_output_no_nan(self):
        """
        Tests output has no nans
        :params self:
        :returns boolean:
        """
        self.assertFalse(np.isnan(PREDICTIONS).any())

if __name__ == '__main__':
    unittest.main()
