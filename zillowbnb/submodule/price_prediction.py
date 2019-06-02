"""Predicts price based on our xgb regressor model"""
import numpy as np
from scipy.special import boxcox1p
from sklearn.externals import joblib
from xgboost import XGBRegressor

def prediction(data, city):
    """
    predicts price using the saved models
    :params data array:
    :params city string:
    :returns price prediction:
    """
    if data.shape == (38,):
        data = data[np.newaxis, :]
    regressor = joblib.load("../../data/" + city + ".joblib.dat")
    boxcox_data = boxcox1p(data, 0.15) + 1
    xgb_pred = np.expm1(regressor.predict(boxcox_data))
    return xgb_pred
