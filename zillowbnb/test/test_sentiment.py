"""
This module runs unit tests for ZillowBnb
"""
import unittest

from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)

import constants # pylint: disable=E0401
import get_data # pylint: disable=E0401
import sentiment # pylint: disable-all

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
            sentiment.polarity(1, 'check')

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
            sentiment.summarize_sentiment(1, ['check'], 'check')
            sentiment.summarize_sentiment(DATA, 1, 'check')


if __name__ == '__main__':
    unittest.main()