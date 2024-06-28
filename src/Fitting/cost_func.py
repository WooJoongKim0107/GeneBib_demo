"""
Functions to evaluate the model estimation.

ChiOne calculates the deviation of the annual number of debuted genes
ChiTwo calculates the deviation of the cumulative number of debuted genes
"""
from collections.abc import Iterable
from dataclasses import dataclass
import numpy as np
from Fitting.data_preparation import get_dbdt, get_bt, dbdt_estimation, bt_estimation


@dataclass
class ChiOne:
    tau: float
    beta: float

    def __post_init__(self):
        dbdt = get_dbdt()
        self.dbdt = np.array([dbdt[t] for t in range(1997, 2022)])
        self.sum = self.dbdt.sum()

    def __call__(self, si: Iterable) -> float:
        dbdt_est = dbdt_estimation(self.tau, self.beta, *si, start=1997, stop=2022)
        return self.calc_chi(self.dbdt, dbdt_est, self.sum)

    @staticmethod
    def calc_chi(x, y, den):
        return np.abs(x - y).sum()/den


@dataclass
class ChiTwo(ChiOne):
    tau: float
    beta: float
    si: Iterable

    def __post_init__(self):
        bt = get_bt()
        self.bt = np.array([bt[t] for t in range(1997, 2022)])
        self.sum = self.bt.sum()

    def __call__(self, c) -> float:
        bt_est = bt_estimation(self.tau, self.beta, *self.si, c, start=1997, stop=2022)
        return self.calc_chi(self.bt, bt_est, self.sum)


@dataclass
class ChiRel:
    tau: float
    beta: float

    def __post_init__(self):
        dbdt = get_dbdt()
        self.dbdt = np.array([dbdt[t] for t in range(1997, 2022)])
        self.sum = self.dbdt.sum()

    def __call__(self, si: Iterable) -> float:
        dbdt_est = dbdt_estimation(self.tau, self.beta, *si, start=1997, stop=2022)
        return self.calc_chi(self.dbdt, dbdt_est, self.sum)

    @staticmethod
    def calc_chi(x, y, den):
        return (np.abs(x - y)/x).sum()
