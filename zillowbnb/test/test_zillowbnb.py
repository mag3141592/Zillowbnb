"""
This module runs unit tests for ZillowBnb
"""
import unittest
from zillowbnb.submodule import get_data
from zillowbnb.submodule import get_calendar_summary

DATASET_PROPERTIES = {'date':'2019-04-15',
                      'city':'Seattle',
                      'state':'WA',
                      'country':'United-States'}

class UnitTest(unittest.TestCase):
    """
    This class runs all the unit tests for ZillowBnb
    """

    def test_calendar_no_na(self):
        """
        Tests calendar.csv.gz data has no empty values
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'calendar.csv.gz')
        self.assertTrue(data.isnull.values.any())


    def test_calendar_more_than_one_row(self):
        """
        Tests calendar.csv.gz data for more than one row
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'calendar.csv.gz')
        self.assertTrue(data.shape[1] >= 1)


    def test_calendar_col(self):
        """
        Test calendar.csv.gz data has the proper columns for
        Seattle, WA, Unintes States
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'calendar.csv.gz')
        column_titles = ['listing_id', 'date', 'available', 'price',
                         'adjusted_price', 'minimum_nights', 'maximum_nights']
        data_col_titles = list(data)
        self.assertTrue(all(x in column_titles for x in data_col_titles))


    def test_calendar_col_types(self):
        """
        Tests calendar.csv.gz data has the proper column data types for
        Seattle, WA, United States
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'calendar.csv.gz')
        self.assertTrue(data.dtypes.listing_id == int and
                        data.dtypes.date == str and
                        data.dtypes.available == str and
                        data.dtypes.price == str and
                        data.dtypes.adjusted_price == str and
                        data.dtypes.minimum_nights == float and
                        data.dtypes.maximum_nights == float)


    def test_calendar_summary_col(self):
        """
        Tests that get_calendar_summary produces the proper column names
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'calendar.csv.gz')
        test = get_calendar_summary.create_calendar_price_averages(data)
        column_titles = ['listing_id', 'fall_price', 'spring_price',
                         'summer_price', 'winter_price', 'weekday_price',
                         'weekend_price']
        test_col_titles = list(test)
        self.assertTrue(all(x in column_titles for x in test_col_titles))


    def test_calendar_summary_col_types(self):
        """
        Tests that get_calendar_summary produces the proper column data types
        """
        data = get_data.download_dataset(DATASET_PROPERTIES, 'calendar.csv.gz')
        test = get_calendar_summary.create_calendar_price_averages(data)
        self.assertTrue(test.dtypes.listing_id == int and
                        test.dtypes.fall_price == float and
                        test.dtypes.spring_price == float and
                        test.dtypes.summer_price == float and
                        test.winter_price == float and
                        test.dtypes.weekday_price == float and
                        test.dtypes.weekdend_price == float)

if __name__ == '__main__':
    unittest.main()
