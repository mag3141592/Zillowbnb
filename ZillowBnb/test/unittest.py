import os
import unittest
from ZillowBnb import ZillowBnb

class UnitTest(unittest.TestCase):
    """
    This class runs all the unit tests for ZillowBnb
    """

    def test_calendar_no_na():
    """
    Tests calendar.csv.gz data has no empty values
    """
    data = get_data.download_dataset('seattle', 'wa', 'united-states', '2019-04-15',
                    'calendar.csv.gz')
    assert data.isnull.values.any()


    def test_calendar_more_than_one_row():
        """
        Tests calendar.csv.gz data for more than one row
        """
        data = get_data.download_dataset('seattle', 'wa', 'united-states', '2019-04-15',
                        'calendar.csv.gz')
    assert data.shape[1] >= 1


    def test_calendar_col():
        """
        Test calendar.csv.gz data has the proper columns for
        Seattle, WA, Unintes States
        """
        data = get_data.download_dataset('seattle', 'wa', 'united-states', '2019-04-15',
                        'calendar.csv.gz')
        column_titles = ['listing_id', 'date', 'available', 'price',
                         'adjusted_price', 'minimum_nights', 'maximum_nights']
        data_col_titles = list(data)
        assert all(x in column_titles for x in data_col_titles)


    def test_calendar_col_types():
        """
        Tests calendar.csv.gz data has the proper column data types for
        Seattle, WA, United States
        """
        data = get_data.download_dataset('seattle', 'wa', 'united-states', '2019-04-15',
                        'calendar.csv.gz')
        assert (data.dtypes.listing_id == int and data.dtypes.date == str and
                data.dtypes.available == str and data.dtypes.price == str and
                data.dtypes.adjusted_price == str and
                data.dtypes.minimum_nights == float and
                data.dtypes.maximum_nights == float)




if __name__ == '__main__':
unittest.main()
