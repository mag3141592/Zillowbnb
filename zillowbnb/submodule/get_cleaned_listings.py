"""
Includes method that returns a cleaned listings dataframe.
"""

import pandas as pd
from pandas.io.json import json_normalize

def clean_and_split(input_val, split_by_char=',', enclosure_char='{|}|[|]', strip_chars='"',
                    also_remove_single_inv_comma=False):
    """
    Splits a column into multiple boolean columns.
    Used for amenities and host verifications within get_cleaned_listings().
    """
    input_val = input_val.strip()
    input_val = input_val.strip(enclosure_char)
    input_val = input_val.split(split_by_char)
    if also_remove_single_inv_comma is True:
        input_val = [item.strip().strip(strip_chars).strip("'").strip() for item in input_val]
    else:
        input_val = [item.strip().strip(strip_chars).strip() for item in input_val]

    output_dict = {}
    for item in input_val:
        output_dict[item] = 1

    return output_dict


def get_listings_dataframe(input_df, columns, write_csv=False):
    """
    Takes in listings dataframe and returns a cleaned listings dataframe.
    If write_csv = True, creates a csv file of the data in the directory.
    """

    #read the file
    listing_file = input_df

    #split up the amenities
    amenities_df = json_normalize(listing_file.amenities.apply(clean_and_split))
    amenities_df = amenities_df.add_prefix('amenities_')
    amenities_df.drop('amenities_', axis=1, inplace=True)
    amenities_df.fillna(value=0, inplace=True)

    #split up the host verifications
    host_verifications_df = json_normalize(listing_file.host_verifications.apply(
        clean_and_split, also_remove_single_inv_comma=True))
    host_verifications_df = host_verifications_df.add_prefix('host_verifications_')
    host_verifications_df.fillna(value=0, inplace=True)

    listing_file = listing_file.join([amenities_df, host_verifications_df])

    #remove some unneeded columns. Also host verifications and amenities because they got split
    remove_cols = ['summary', 'space', 'interaction', 'access', 'description',
                   'neighborhood_overview', 'notes', 'transit', 'house_rules',
                   'host_about', 'host_verifications', 'amenities']

    listing_file.drop(remove_cols, axis=1, inplace=True)

    #get rid of dollar sign and commas in price columns. Convert to numeric
    price_cols = [x for x in listing_file.columns if 'price' in x]
    price_cols.append('cleaning_fee')
    price_cols.append('security_deposit')
    price_cols.append('extra_people')

    for price_col in price_cols:
        listing_file.loc[:, price_col].fillna(value=0, inplace=True)
        listing_file.loc[:, price_col] = listing_file.loc[:, price_col] \
            .astype(str).str.replace('$', '')
        listing_file.loc[:, price_col] = listing_file.loc[:, price_col].str.replace(',', '')
        listing_file.loc[:, price_col] = pd.to_numeric(listing_file.loc[:, price_col])

    #Convert date columns to datetime format
    dateconversioncols = ['last_scraped', 'host_since', 'calendar_last_scraped',
                          'first_review', 'last_review']
    for date_col in dateconversioncols:
        listing_file.loc[:, date_col] = pd.to_datetime(listing_file.loc[:, date_col],
                                                       format='%Y-%m-%d')

    #Column selection
    listing_file = listing_file[columns]
    listing_file = listing_file.rename(columns={'id': 'listing_id'})

    if write_csv:
        listing_file.to_csv('./clean_listings.csv', index=False)

    return listing_file
