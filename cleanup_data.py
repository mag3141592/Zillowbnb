from pandas import read_csv, to_numeric, io, to_datetime
from pandas.io.json import json_normalize
import sys
import os
import traceback

if len(sys.argv) < 2:
  print("Please specify your input file")
  sys.exit(1)

input_file = sys.argv[1]

if not os.path.isfile(input_file):
  traceback.print_exc(file=sys.stdout)
  sys.exit(1)

ListingFile = read_csv(input_file)


def CleanAndSplit(inputVal,
                  SplitByChar=',',
                  enclosureChar='{|}|[|]',
                  stripChars='"',
                  alsoRemoveSingleInvComma=False):
  inputVal = inputVal.strip()
  inputVal = inputVal.strip(enclosureChar)
  inputVal = inputVal.split(SplitByChar)
  if alsoRemoveSingleInvComma == True:
    inputVal = [item.strip().strip(stripChars).strip("'").strip() for item in inputVal]
  else:
    inputVal = [item.strip().strip(stripChars).strip() for item in inputVal]

  OutputDict = {}
  for item in inputVal:
    OutputDict[item] = 1

  return(OutputDict)


AmenitiesDF = json_normalize(ListingFile.amenities.apply(CleanAndSplit)).add_prefix('amenities_')
AmenitiesDF.drop('amenities_', axis=1, inplace=True)
AmenitiesDF.fillna(value=0, inplace=True)

HostVerificationsDF = json_normalize(ListingFile.host_verifications.apply(CleanAndSplit, alsoRemoveSingleInvComma=True)).add_prefix('host_verifications_')
HostVerificationsDF.drop(['host_verifications_'], axis=1, inplace=True)
HostVerificationsDF.fillna(value=0, inplace=True)

ListingFile = ListingFile.join([AmenitiesDF, HostVerificationsDF])

removeCols = ['summary',
              'space',
              'interaction',
              'access',
              'description',
              'neighborhood_overview',
              'notes',
              'transit',
              'house_rules',
              'host_about',
              'host_verifications',
              'amenities']

ListingFile.drop(removeCols, axis=1, inplace=True)

PriceCols = [x for x in ListingFile.columns if 'price' in x]
PriceCols.append('cleaning_fee')
PriceCols.append('security_deposit')
PriceCols.append('extra_people')

for PriceCol in PriceCols:
  ListingFile.loc[:, PriceCol].fillna(value=0, inplace=True)
  ListingFile.loc[:, PriceCol] = ListingFile.loc[:, PriceCol].astype(str).str.replace('$', '')
  ListingFile.loc[:, PriceCol] = ListingFile.loc[:, PriceCol].str.replace(',', '')
  ListingFile.loc[:, PriceCol] = to_numeric(ListingFile.loc[:, PriceCol])

DateConversionCols = ['last_scraped', 'host_since', 'calendar_last_scraped', 'first_review', 'last_review']
for DateCol in DateConversionCols:
  ListingFile.loc[:, DateCol] = to_datetime(ListingFile.loc[:, DateCol], format='%Y-%m-%d')

ListingFile.to_csv('~/Documents/CleanListings.csv', index=False)
