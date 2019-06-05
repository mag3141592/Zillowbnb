"""
Contains methods for downloading and merging datasets.
"""

import pandas as pd
import requests

import constants

def download_dataset(dataset_dict, filename, write_csv=False):
    """
    Downloads datasets from Inside Airbnb

    :params dataset_dict dict (required keys: date, city, state, country):
    :params filename string:
    :params write_csv boolean (optional):
    :returns data as dataframe and outputs csv when write_csv=True:
    """

    # Checks dataset_dict has rquired keys
    keys = list(dataset_dict.keys())
    required_keys = list(constants.DATASET_PROPERTIES.keys())
    if not set(required_keys).issubset(keys):
        raise ValueError('Dictionary does not have necessary keys: ' + str(required_keys))

    date = dataset_dict[required_keys[0]]
    city = dataset_dict[required_keys[1]].lower()
    state = dataset_dict[required_keys[2]].lower()
    country = dataset_dict[required_keys[3]].replace(' ', '-').lower()
    filename = filename.lower()

    data_url = ('http://data.insideairbnb.com/' + country + '/' + state + '/'
                + city + '/' + date + '/data/' + filename)
    response = requests.get(data_url)

    # Checks URL is valid
    if response.status_code == 404:
        raise ValueError('Invalid URL')

    dataframe = pd.read_csv(data_url)
    rows, cols = dataframe.shape

    # Checks dataframe has rows and columns
    if(rows == 0 or cols == 0):
        raise ValueError('Invalid URL')

    if write_csv:
        csv_name = filename.strip('.gz')
        dataframe.to_csv(constants.DATA_FOLDER + csv_name, index=False)

    return dataframe


def merge_data(file1, file2, file3, merge_on):
    """
    Merges the cleaned datasets into one csv file.

    :params file1 string:
    :params file2 string:
    :params file3 string:
    :params merge_on string:
    :returns merged data as dataframe and outputs csv:
    """

    # Load datasets
    try:
        file1 = pd.read_csv(constants.DATA_FOLDER + file1)
        file2 = pd.read_csv(constants.DATA_FOLDER + file2)
        file3 = pd.read_csv(constants.DATA_FOLDER + file3)
    except FileNotFoundError:
        raise FileNotFoundError()

    # Check merge_on is in all files
    if (merge_on not in file1.columns or
            merge_on not in file2.columns or
            merge_on not in file3.columns):

        raise ValueError(merge_on + ' is missing from at least 1 file.')

    merge_1 = file1.merge(file2, on=merge_on)
    merge_2 = merge_1.merge(file3, on=merge_on)
    merge_2.to_csv(constants.DATA_FOLDER +
                   constants.DATASET_PROPERTIES[constants.CITY] +
                   'merged.csv', index=False)

    return merge_2
