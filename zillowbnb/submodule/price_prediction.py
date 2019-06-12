"""Predicts price based on our xgb regressor model"""

from os.path import dirname, abspath, join

import numpy as np
from scipy.special import boxcox1p
from sklearn.externals import joblib
from xgboost import XGBRegressor

import constants as c
import convert_to_matrix as cm
import detect_outliers as do

# Find data directory relative to current directory
THIS_DIR = dirname(__file__)
DATA_DIR = abspath(join(THIS_DIR, '../..', 'data'))

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
    regressor_a = joblib.load(DATA_DIR + '/' + city + c.MODEL_1_SUFFIX)
    regressor_b = joblib.load(DATA_DIR + '/' + city + c.MODEL_2_SUFFIX)

    outlier_boundary = min(do.detect_outlier(y_var))
    inbound = (y_var < outlier_boundary)
    outbound = (y_var >= outlier_boundary)

    #populates predictions depending on current price
    predictions = np.zeros(price_length)

    predictions[inbound] = np.expm1(regressor_b.predict(x_var[inbound]))
    predictions[outbound] = np.expm1(regressor_a.predict(x_var[outbound]))

    return predictions
