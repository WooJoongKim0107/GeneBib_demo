"""
Functions to minimize the cost function using the random initial parameters.
See <fitting.py> for its use.
"""
import numpy as np
from scipy.optimize import minimize
from Fitting.cost_func import ChiOne, ChiTwo
from Fitting.data_preparation import get_bt


B1997, B2018 = [v for k, v in get_bt().items() if k in (1997, 2018)]
BOUNDARIES = [[1e-6, 1.-1e-6], [0, B2018], [0, B1997]]


def random_initial_paras(num, bdries):
    return np.random.uniform(*zip(*bdries), size=(num, len(bdries)))


def minimize_chi_1(tau, beta, initial_para: np.ndarray, **kwargs):
    cost = ChiOne(tau, beta)
    return minimize(cost, initial_para, **kwargs)


def minimize_chi_2(tau, beta, si, initial_para: np.ndarray, **kwargs):
    cost = ChiTwo(tau, beta, si)
    return minimize(cost, initial_para, **kwargs)
