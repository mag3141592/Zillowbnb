"""Predicts price based on our xgb regressor model"""
# pylint: disable=no-member

from os.path import dirname, abspath, join # pylint: disable=R0801

import numpy as np
from scipy.special import boxcox1p # pylint: disable=E0611
from sklearn.externals import joblib
from xgboost import XGBRegressor # pylint: disable=W0611

import convert_to_matrix as cm
import detect_outliers as do

THIS_DIR = dirname(__file__)
DATA_DIR = abspath(join(THIS_DIR, '../..', 'data'))

# Find data directory relative to current directory

def predict_input(data, city):
    """
    predicts price using the saved models
    :params data array:
    :params city string:
    :returns price prediction:
    """

    #in case it only predicts one row
    if data.shape == (38,):
        data = data[np.newaxis, :]

    #imports model
    regressor = joblib.load(DATA_DIR + "/" +  city + ".joblib.dat")

    #boxcox transforms features
    boxcox_data = boxcox1p(data, 0.15) + 1
    xgb_pred = np.expm1(regressor.predict(boxcox_data))
    return xgb_pred

def predict_dataset(data_frame, city, columns):
    """
    Predicts prices of listings from a dataset
    :params data_frame dataframe:
    :params city str:
    :params columns list:
    :returns predictions array:
    """
    x_var, y_var = cm.to_matrix(data_frame, columns)
    x_var = boxcox1p(x_var, 0.15) + 1
    price_length = len(y_var)

    #imports models
    regressor_a = joblib.load(DATA_DIR + "/" + city + ".joblib.dat")
    regressor_b = joblib.load(DATA_DIR + "/" + city + "_low.joblib.dat")

    outlier_boundary = min(do.detect_outlier(y_var))
    inbound = (y_var < outlier_boundary)
    outbound = (y_var >= outlier_boundary)

    #populates predictions depending on current price
    predictions = np.zeros(price_length)

    predictions[inbound] = np.expm1(regressor_b.predict(x_var[inbound]))
    predictions[outbound] = np.expm1(regressor_a.predict(x_var[outbound]))

    return predictions
