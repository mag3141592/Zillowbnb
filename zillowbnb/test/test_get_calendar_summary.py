"""
This module runs unit tests for get_calendar_summary
"""
import unittest

from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)

import get_data # pylint: disable=E0401
import get_calendar_summary # pylint: disable-all
import constants


DATA = get_data.download_dataset(constants.DATASET_PROPERTIES,
                                 constants.CALENDAR_DATA)

class CalendarTest(unittest.TestCase):
    """
    This class runs all the unit tests for ZillowBnb
    """

    def test_calendar_summary_col(self):
        """
        Tests that get_calendar_summary produces the proper column names
        """)
        test = get_calendar_summary.create_calendar_price_averages(DATA)
        column_titles = constants.CALENDAR_SUMAMRY_COLUMNS
        test_col_titles = list(test)
        self.assertTrue(all(x in column_titles for x in test_col_titles))


    def test_calendar_summary_col_types(self):
        """
        Tests that get_calendar_summary produces the proper column data types
        """
        test = get_calendar_summary.create_calendar_price_averages(DATA)
        self.assertTrue(test.dtypes.listing_id == int and
                        test.dtypes.fall_price == float and
                        test.dtypes.spring_price == float and
                        test.dtypes.summer_price == float and
                        test.dtypes.winter_price == float and
                        test.dtypes.weekday_price == float and
                        test.dtypes.weekend_price == float)


if __name__ == '__main__':
    unittest.main()
