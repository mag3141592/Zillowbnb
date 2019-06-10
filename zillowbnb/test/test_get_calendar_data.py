"""
This module runs unit tests for getting the calendar data
"""
import unittest

from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)

import get_data # pylint: disable=E0401
import get_calendar_summary 
import constants

DATA = get_data.download_dataset(constants.DATASET_PROPERTIES,
                                 constants.CALENDAR_DATA)

class CalendarDataTest(unittest.TestCase):
    """
    This class runs unit tests for ZillowBnb
    """

    def test_calendar_no_na(self):
        """
        Tests calendar.csv.gz data has no empty values
        :param self:
        :return boolean:
        """
        self.assertTrue(DATA.isnull().values.any())


    def test_calendar_more_than_one_row(self):
        """
        Tests calendar.csv.gz data for more than one row
        :param self:
        :return boolean:
        """
        self.assertTrue(DATA.shape[0] >= 1)


    def test_calendar_col(self):
        """
        Test calendar.csv.gz data has the proper columns
        :param self:
        :return boolean:
        """
        column_titles = constants.CALENDAR_COLUMNS
        data_col_titles = list(DATA)
        self.assertTrue(all(x in column_titles for x in data_col_titles))


    def test_calendar_col_types(self):
        """
        Tests calendar.csv.gz data has the proper column data types
        :param self:
        :return boolean:
        """
        self.assertTrue(DATA.dtypes.listing_id == int and
                        DATA.dtypes.date == object and
                        DATA.dtypes.available == object and
                        DATA.dtypes.price == object and
                        DATA.dtypes.adjusted_price == object and
                        DATA.dtypes.minimum_nights == float and
                        DATA.dtypes.maximum_nights == float)


if __name__ == '__main__':
    unittest.main()
