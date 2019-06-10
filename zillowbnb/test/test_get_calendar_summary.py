"""
This module runs unit tests for get_calendar_summary
"""
# pylint: disable=no-member
import unittest

from os.path import dirname, abspath, join
import sys
import datetime

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'submodule'))
sys.path.append(CODE_DIR)

import get_data # pylint: disable=E0401, C0413
import get_calendar_summary # pylint: disable=E0401, C0413
import constants # pylint: disable=E0401, C0413

DATA = get_data.download_dataset(constants.DATASET_PROPERTIES,
                                 constants.CALENDAR_DATA)

TEST = get_calendar_summary.create_calendar_price_averages(DATA)

# used to test error throwing (can not be a string or datetime.datetime)
INCORRCT_DATA_TYPE = 9
TEST_DATE = datetime.date(2019, 4, 23)
TEST_CURRENCY_STRING = "$1,000.00"


class CalendarTest(unittest.TestCase):
    """
    This class runs unit tests for ZillowBnb
    """

    def test_calendar_no_na(self):
        """
        Tests imported calendar data has no empty values
        :param self:
        :return boolean:
        """
        self.assertTrue(DATA.isnull().values.any())


    def test_calendar_more_than_one_row(self):
        """
        Tests imported calendar data for more than one row
        :param self:
        :return boolean:
        """
        self.assertTrue(DATA.shape[0] >= 1)


    def test_calendar_col(self):
        """
        Test imported calendar data has the proper columns
        :param self:
        :return boolean:
        """
        column_titles = constants.CALENDAR_COLUMNS
        data_col_titles = list(DATA)
        self.assertTrue(all(x in column_titles for x in data_col_titles))


    def test_calendar_col_types(self):
        """
        Tests imported calendar data has the proper column data types
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


    def test_calendar_sumary_no_na(self):
        """
        Test that get_calendar_summary produces no empty values
        :param self:
        :return boolean:
        """
        self.assertTrue(TEST.isnull().values.any())

    def test_calendar_summary_more_than_one_row(self):
        """
        Tests that get_calendar_summary produces more than one row
        :param self:
        :return boolean:
        """
        self.assertTrue(TEST.shape[0] >= 1)


    def test_calendar_summary_col(self):
        """
        Tests that get_calendar_summary produces the proper column names
        :param self:
        :return boolean:
        """
        column_titles = constants.CALENDAR_SUMMARY_COLUMNS
        test_col_titles = list(TEST)
        self.assertTrue(all(x in column_titles for x in test_col_titles))


    def test_calendar_summary_col_types(self):
        """
        Tests that get_calendar_summary produces the proper column data types
        :param self:
        :return boolean:
        """
        self.assertTrue(TEST.dtypes.listing_id == int and
                        TEST.dtypes.fall_price == float and
                        TEST.dtypes.spring_price == float and
                        TEST.dtypes.summer_price == float and
                        TEST.dtypes.winter_price == float and
                        TEST.dtypes.weekday_price == float and
                        TEST.dtypes.weekend_price == float)

    def test_get_day_type_thorws_exception(self):
        """
        Tests that get_day_type throws an exception when passed something that
        isnt a datetime.date.
        :param self:
        :return boolean:
        """
        self.assertRaises(TypeError, get_calendar_summary.get_day_type,
                          INCORRCT_DATA_TYPE)

    def test_get_season_throws_exception(self):
        """
        Tests that get_season throws an exeption when passed something that
        is not a datetime.datetime
        :param self:
        :return boolean:
        """
        self.assertRaises(TypeError, get_calendar_summary.get_season,
                          INCORRCT_DATA_TYPE)

    def test_convert_currency_to_float(self):
        """
        Tests that convert_currency_to_float throws an exeption when passed
        something that is not a string
        :param self:
        :return boolean:
        """
        self.assertRaises(TypeError, get_calendar_summary.convert_currency_to_float,
                          INCORRCT_DATA_TYPE)

    def test_get_day_type_returns_string(self):
        """
        tests that get_day_type returns a string
        :param self:
        :return boolean:
        """
        test = get_calendar_summary.get_day_type(TEST_DATE)
        self.assertTrue(isinstance(test, str))

    def test_get_season_returns_string(self):
        """
        tests that get_season returns a string
        :param self:
        :return boolean:
        """
        test = get_calendar_summary.get_season(TEST_DATE)
        self.assertTrue(isinstance(test, str))

    def test_convert_currency_to_float_returns_float(self):
        """
        tests that convert_currency_to_float returns a float
        :param self:
        :return boolean:
        """
        test = get_calendar_summary.convert_currency_to_float(TEST_CURRENCY_STRING)
        self.assertTrue(isinstance(test, float))


if __name__ == '__main__':
    unittest.main()
