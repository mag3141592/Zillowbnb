"""Boxcox transform input array to feed into model for prediction"""

from scipy.special import boxcox1p

def transform_input(array):
    """
    Converts input array to be used in model
    :params array array:
    :return array:
    """
    return boxcox1p(array, 0.15) + 1
