"""
Downloads datasets from Inside Airbnb.
"""

import pandas as pd

def download_dataset(city, state_abbv, country, yyyy_mm_dd, filename):
    """
    Takes in strings of the dataset's city, state_abbv, country, filename, and date complied
    (formated as yyyy-mm-dd) and the filename. It returns the dataset as a dataframe.
    """
    country = country.replace(' ', '-')
    data_url = ('http://data.insideairbnb.com/' + country + '/' + state_abbv + '/' + city + '/'
                + yyyy_mm_dd + '/data/' + filename)
    dataframe = pd.read_csv(data_url)
    return dataframe
