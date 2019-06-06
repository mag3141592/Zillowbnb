"""Predicts price based on our xgb regressor model"""
import numpy as np
from scipy.special import boxcox1p # pylint: disable=E0611
from sklearn.externals import joblib
from xgboost import XGBRegressor # pylint: disable=W0611

def prediction(data, city):
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
    regressor = joblib.load("../../data/" + city + ".joblib.dat")

    #boxcox transforms features
    boxcox_data = boxcox1p(data, 0.15) + 1
    xgb_pred = np.expm1(regressor.predict(boxcox_data))
    return xgb_pred
