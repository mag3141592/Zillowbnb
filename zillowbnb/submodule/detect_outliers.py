"""Detects outliers for list or array of values"""

import numpy as np

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
