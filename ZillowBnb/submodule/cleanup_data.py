"""
DOC HOLDER
"""

import os
import sys
import traceback
from pandas import read_csv, to_numeric, to_datetime
from pandas.io.json import json_normalize

#read the file
if len(sys.argv) < 2:
    print("Please specify your input file")
    sys.exit(1)

INPUT_FILE = sys.argv[1]

if not os.path.isfile(INPUT_FILE):
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)

LISTING_FILE = read_csv(INPUT_FILE)

#split up the amenities and host verifications
def clean_and_split(input_val, split_by_char=',', enclosure_char='{|}|[|]', strip_chars='"',
                    also_remove_single_inv_comma=False):
    """
    DOC HOLDER
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

AMENITIES_DF = json_normalize(LISTING_FILE.amenities.apply(clean_and_split))
AMENITIES_DF.add_prefix('amenities_')
AMENITIES_DF.drop('amenities_', axis=1, inplace=True)
AMENITIES_DF.fillna(value=0, inplace=True)

HOST_VER = LISTING_FILE.host_verifications
HOSTVERIFICATIONSDF = json_normalize(HOST_VER.apply(clean_and_split,
                                                    also_remove_single_inv_comma=True))
HOSTVERIFICATIONSDF.add_prefix('host_verifications_')
HOSTVERIFICATIONSDF.drop(['host_verifications_'], axis=1, inplace=True)
HOSTVERIFICATIONSDF.fillna(value=0, inplace=True)

LISTING_FILE = LISTING_FILE.join([AMENITIES_DF, HOSTVERIFICATIONSDF])

#remove the unneeded columns. Also host verifications and amenities because they got split
REMOVE_COLS = ['summary', 'space', 'interaction', 'access', 'description', 'neighborhood_overview',
               'notes', 'transit', 'house_rules', 'host_about', 'host_verifications', 'amenities']

LISTING_FILE.drop(REMOVE_COLS, axis=1, inplace=True)

#Get rid of dollar sign and commas in price columns. Convert to numeric
PRICE_COLS = [x for x in LISTING_FILE.columns if 'price' in x]
PRICE_COLS.append('cleaning_fee')
PRICE_COLS.append('security_deposit')
PRICE_COLS.append('extra_people')

for PriceCol in PRICE_COLS:
    LISTING_FILE.loc[:, PriceCol].fillna(value=0, inplace=True)
    LISTING_FILE.loc[:, PriceCol] = LISTING_FILE.loc[:, PriceCol].astype(str).str.replace('$', '')
    LISTING_FILE.loc[:, PriceCol] = LISTING_FILE.loc[:, PriceCol].str.replace(',', '')
    LISTING_FILE.loc[:, PriceCol] = to_numeric(LISTING_FILE.loc[:, PriceCol])

#Convert date columns to datetime format
DATECONVERSIONCOLS = ['last_scraped', 'host_since', 'calendar_last_scraped',
                      'first_review', 'last_review']
for DateCol in DATECONVERSIONCOLS:
    LISTING_FILE.loc[:, DateCol] = to_datetime(LISTING_FILE.loc[:, DateCol], format='%Y-%m-%d')

LISTING_FILE.to_csv('./CleanListings.csv', index=False)
