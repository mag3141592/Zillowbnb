"""
This module runs unit tests for ZillowBnb
"""

import unittest

import zillowbnb.test.submodule_path
import constants
import get_data
import sentiment

DATA = get_data.download_dataset(constants.DATASET_PROPERTIES,
                                 constants.REVIEWS_DATA)

class SentimentTest(unittest.TestCase):
    """
    This class runs unit tests for the sentiment submodule
    """

    def test_polarity_check_dtype(self):
        """
        Tests that polarity will not run if datatypes are incorrect
        :param self:
        :return boolean:
        """
        with self.assertRaises(ValueError):
            sentiment.polarity(DATA, 1)

    def test_polarity_check_column(self):
        """
        Tests that polarity will not run if column isnt in dataframe
        :param self:
        :return boolean:
        """
        with self.assertRaises(ValueError):
            sentiment.polarity(DATA, 'commentsfalse')

    def test_summarize_check(self):
        """
        Test that summarize_sentiment will not run if datatypes are incorrect
        :param self:
        :return boolean:
        """
        with self.assertRaises(ValueError):
            sentiment.summarize_sentiment(DATA, ['check'], 1)


if __name__ == '__main__':
    unittest.main()
