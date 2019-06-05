[![Build Status](https://travis-ci.org/mag3141592/Final515Project.svg?branch=master)](https://travis-ci.org/mag3141592/Final515Project)
[![Coverage Status](https://coveralls.io/repos/github/mag3141592/Final515Project/badge.svg?branch=master)](https://coveralls.io/github/mag3141592/Final515Project?branch=master)

# Zillowbnb

## Background
Homeowners and potential home buyers often rely on Zillow’s Zestimate to estimate the market price of houses. The Zestimate predicts a home’s value using publicly available housing data and a proprietary machine learning formula. It serves as a starting point for homeowners who are looking to sell their property and enables home buyers to gain a better understanding of the market.

Such a feature would be similarly useful to predict the market rental price of a short-term rental unit on Airbnb.  A guest could compare the price of an Airbnb listing to its predicted price to know if they are getting a good deal. A host could easily determine a good price to list their unit.

## Installation
1. Clone the repo
2. Create a new python environmet using conda env create zillowbnb
3. Activate zillowbnb by using conda activate zillowbnb
4. install the required python packages using pip install –r requirements.txt


## Directory Structure
```
zillowbnb/
  |- data/
     |- Seattle.joblib.dat
     |- calendar_price_averages.csv
     |- clean_listings.csv
     |- final_merged.csv
     |- reviews_sa_summarized.csv
  |- docs/
     |- Component_Specification.pdf
     |- Functional_Specification.pdf
     |- Technology Review.pdf
  |- zillowbnb/
     |- submodule/
        |- __init__.py
        |- bokeh_plot.py
        |- convert_to_matrix.py
        |- get_calendar_summary.py
        |- get_cleaned_listings.py
        |- get_data.py
        |- price_predictions.py
        |- sentiment.py
        |- transform_input.py
     |- test/
        |- __init__.py
        |- test_get_calendar_summary.py
        |- test_get_cleaned_listings.py
     |- __init__.py
     |- zillowbnb.py
  |- .coveragerc
  |- .travis.yml
  |- LICENSE
  |- README.md
  |- requirements.txt
  |- examples/
     |-
```
## How to Use/Examples
In work...
