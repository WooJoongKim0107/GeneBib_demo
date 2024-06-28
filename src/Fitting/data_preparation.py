"""
Functions to calculate the model estimation for given parameters - t2y(), bt_estimation(), and dbdt_estimation()
and to generate the target data - the rest
"""
from itertools import accumulate
from functools import lru_cache
from collections.abc import Collection
import numpy as np
import pandas as pd
from mypathlib import PathTemplate

R_FILES = {
    'N': PathTemplate('$data/yearly_new_entries.csv').substitute(),
    'dbdt': PathTemplate('$data/yearly_new_genes.csv').substitute(),
}


def keys_sorted(dct: dict):
    return dict(sorted(dct.items()))


def fill_keys(dct: dict, sort=True):
    dictionary = {k: dct.get(k, 0) for k in range(min(dct), max(dct)+1)}
    return keys_sorted(dictionary) if sort else dictionary


def values_accumulated(dct: dict):
    return dict(zip(dct, accumulate(dct.values())))


N = pd.read_csv(R_FILES['N'], index_col=0).squeeze().to_dict()


@lru_cache(maxsize=128)
def get_dbdt():
    return pd.read_csv(R_FILES['dbdt'], index_col=0).squeeze().to_dict()


@lru_cache(maxsize=128)
def get_bt():
    return values_accumulated(get_dbdt())


def calc_dydt(t, tau):
    return sum(np.exp(-tt/tau) * N[t - tt] for tt in range(t-1939+1))*(1. - np.exp(-1./tau))


@lru_cache(maxsize=512)
def get_dydt(tau: float):
    if tau <= 0:
        return N.copy()
    return {t: calc_dydt(t, tau) for t in N}


@lru_cache(maxsize=512)
def get_yt(tau):
    return values_accumulated(get_dydt(tau))


def t2y(ts: Collection, tau: float, beta: float):
    """
    Change a sequence of times into sequence of y's.
    """
    yt = get_yt(tau)
    return np.fromiter((beta*yt[time] for time in ts), dtype=float, count=len(ts))


def dbdt_estimation(tau, beta, s, i, start=1997, stop=2022) -> np.ndarray:
    b_est = bt_estimation(tau, beta, s, i, 0, start=start-1, stop=stop)
    return np.diff(b_est)


def bt_estimation(tau, beta, s, i, c, start=1997, stop=2022) -> np.ndarray:
    ys = t2y(range(start, stop), tau, beta)
    return s*ys + i*(1.-np.exp(-ys*(1.-s)/i)) + c
