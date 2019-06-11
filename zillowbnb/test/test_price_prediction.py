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
import price_prediction as pp

DATA = gd.download_dataset(co.DATASET_PROPERTIES,
                           co.LISTINGS_DATA)

DATAFRAME = gcl.get_listings_dataframe(DATA, co.LISTING_COLUMNS)

X_VAR, Y_VAR = cm.to_matrix(DATAFRAME, co.LISTING_COLUMNS)


PREDICTIONS = pp.predict_dataset(DATAFRAME,
                                 co.DATASET_PROPERTIES[co.CITY],
                                 co.LISTING_COLUMNS)

class PricePredictionTest(unittest.TestCase):
    """
    This class runs unit tests for the price_prediction module.
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
