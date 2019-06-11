![zillowbnb_logo](https://github.com/mag3141592/Zillowbnb/blob/master/docs/zillowbnb.jpg)

[![Build Status](https://travis-ci.org/mag3141592/Zillowbnb.svg?branch=master)](https://travis-ci.org/mag3141592/Zillowbnb)
[![Coverage Status](https://coveralls.io/repos/github/mag3141592/Zillowbnb/badge.svg?branch=master)](https://coveralls.io/github/mag3141592/Zillowbnb?branch=master)

# Zillowbnb

## Background
Homeowners and potential home buyers often rely on Zillow’s Zestimate to estimate the market price of houses. The Zestimate predicts a home’s value using publicly available housing data and a proprietary machine learning formula. It serves as a starting point for homeowners who are looking to sell their property and enables home buyers to gain a better understanding of the market.

Such a feature would be similarly useful to predict the market rental price of a short-term rental unit on Airbnb.  A guest could compare the price of an Airbnb listing to its predicted price to know if they are getting a good deal. A host could easily determine a good price to list their unit.

## Installation
1. Clone the repo  
2. Create a new python environmet using the command:  
```conda env create zillowbnb```  
3. Activate zillowbnb by using the command:  
```conda activate zillowbnb```  
4. Install the required python packages using:  
```pip install –r requirements.txt```  

## Directory Structure
```
zillowbnb/
  |- data/
     |- Seattle.joblib.dat
     |- Seattle_low.joblib.dat
     |- calendar_price_averages.csv
     |- clean_listings.csv
     |- final_sa_summarized.csv
     |- seattle_merged.csv
  |- docs/
     |- Component_Specification.pdf
     |- Functional_Specification.pdf
     |- Technology Review.pdf
  |- zillowbnb/
     |- submodule/
        |- __init__.py
        |- bokeh_plot.py
        |- constants.py
        |- convert_to_matrix.py
        |- detect_outliers.py
        |- get_calendar_summary.py
        |- get_cleaned_listings.py
        |- get_data.py
        |- price_prediction.py
        |- sentiment.py
        |- train_model.py
     |- test/
        |- __init__.py
        |- submodule_path.py
        |- test_convert_to_matrix.py
        |- test_detect_outliers.py
        |- test_get_calendar_summary.py
        |- test_get_cleaned_listings.py
        |- test_get_data.py
        |- test_price_prediction.py
        |- test_sentiment.py
        |- test_train_model.py
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
