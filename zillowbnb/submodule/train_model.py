"""
Trains a boosted trees regressor and saves it as .dat in the data folder for future use.
"""
# pylint: disable=no-member

import numpy as np
from scipy.special import boxcox1p # pylint: disable=E0611
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor # pylint: disable=W0611

import zillowbnb.submodule.detect_outliers as do

def train_model(x_var, y_var, city):
    """
    Trains boosted trees model and saves it for future use
    :params x feature array:
    :params y price array:
    :params city string:
    """
    #creates data with no outliers
    outlier_boundary = min(do.detect_outlier(y_var))
    inbound = (y_var < outlier_boundary)
    x_var_low = x_var.copy()
    x_var_low = x_var[inbound]
    y_var_low = y_var.copy()
    y_var_low = y_var[inbound]

    #full data
    x_var = boxcox1p(x_var, 0.15) + 1
    y_var = np.log1p(y_var)
    x_train = train_test_split(x_var, y_var, test_size=0.2, random_state=0)[0]
    y_train = train_test_split(x_var, y_var, test_size=0.2, random_state=0)[2]

    #trains full model
    regressor = XGBRegressor(colsample_bytree=0.2, gamma=0.0,
                             learning_rate=0.05, max_depth=7,
                             min_child_weight=1.5, n_estimators=7200,
                             reg_alpha=0.9, reg_lambda=0.6,
                             subsample=0.2, seed=0, silent=1,
                             random_state=7).fit(x_train, y_train)
    joblib.dump(regressor, "../../data/" + city + ".joblib.dat")

    x_var_low = boxcox1p(x_var_low, 0.15) + 1
    y_var_low = np.log1p(y_var_low)

    x_train_low = train_test_split(x_var_low, y_var_low, test_size=0.2, random_state=0)[0]
    y_train_low = train_test_split(x_var_low, y_var_low, test_size=0.2, random_state=0)[2]

    #trains model without outliers
    regressor_low = XGBRegressor(colsample_bytree=0.2, gamma=0.0,
                                 learning_rate=0.05, max_depth=7,
                                 min_child_weight=1.5, n_estimators=7200,
                                 reg_alpha=0.9, reg_lambda=0.6,
                                 subsample=0.2, seed=0, silent=1,
                                 random_state=7).fit(x_train_low, y_train_low)
    joblib.dump(regressor_low, "../../data/" + city + "_low.joblib.dat")
