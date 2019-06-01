"""
Includes method for downloading datasets.
"""

import pandas as pd

def download_dataset(city, state_abbv, country, yyyy_mm_dd, filename, write_csv=False):
    """
    Takes in strings of the dataset's city, state_abbv, country, filename, and date complied
    (formated as yyyy-mm-dd) and the filename. It returns the dataset as a dataframe.
    If write_csv = True, creates a csv file of the data in the directory.
    """
    country = country.replace(' ', '-')
    data_url = ('http://data.insideairbnb.com/' + country + '/' + state_abbv + '/' + city + '/'
                + yyyy_mm_dd + '/data/' + filename)
    dataframe = pd.read_csv(data_url)

    if write_csv:
        csv_name = filename.strip('.gz')
        dataframe.to_csv('./' + csv_name, index=False)

    return dataframe
