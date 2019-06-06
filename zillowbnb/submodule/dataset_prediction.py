"""Reads dataset and predicts prices with the different models"""
import numpy as np
from scipy.special import boxcox1p # pylint: disable=E0611
from sklearn.externals import joblib
from xgboost import XGBRegressor # pylint: disable=W0611

import convert_to_matrix as cm

def detect_outlier(data_1):
    """
    Detects outliers
    :params data_1 array:
    :returns list of outliers:
    """
    outliers = []
    threshold = 3
    mean_1 = np.mean(data_1)
    std_1 = np.std(data_1)

    for y_var in data_1:
        z_score = (y_var - mean_1)/std_1
        if np.abs(z_score) > threshold:
            outliers.append(y_var)
    return outliers


def prediction(data_frame, columns):
    """
    Predicts prices of listings from a dataset
    :params data_frame dataframe:
    :params columns list:
    :returns predictions array:
    """
    x_var, y_var = cm.to_matrix(data_frame, columns)
    x_var = boxcox1p(x_var, 0.15) + 1
    price_length = len(y_var)

    #imports models
    regressor_a = joblib.load("../../data/Seattle.joblib.dat")
    regressor_b = joblib.load("../../data/Seattle_low.joblib.dat")

    outlier_boundary = min(detect_outlier(y_var))
    inbound = (y_var < outlier_boundary)
    outbound = (y_var >= outlier_boundary)
    #populates predictions depending on current price
    predictions = np.zeros(price_length)

    predictions[inbound] = np.expm1(regressor_b.predict(x_var[inbound]))
    predictions[outbound] = np.expm1(regressor_a.predict(x_var[outbound]))

    return predictions
