"""
Find the best set of parameters (s, i, c) for each (tau, beta) and repackage them
  among the raw results generated from <fitting.py>

fit_raw files:
    <tau0_beta01.pkl> contains  {'chi1': [chi1 of the first random initial fitting, chi1 of the second, ...],
                                 'chi2': [chi2 of the first random initial fitting, chi1 of the second, ...],
                                 'sic': [sic of the first random initial fitting, chi1 of the second, ...],}
    <tau0_beta02.pkl> contains  {'chi1': [...], 'chi2': [...], 'sic': [...]}
    ...
    <tau19_beta10.pkl> contains {'chi1': [...], 'chi2': [...], 'sic': [...]}


fit_res files:
    <fit_res.pkl> contains  {'chi1': {tau -> {beta -> minimum of chi1 for given (tau, beta)}},
                             'chi2' {tau -> {beta -> chi2 from the set of parameters
                                        that gives the minimum chi1 for given (tau, beta)}},
                             'sic': {tau -> {beta -> the set of parameters
                                        that gives the minimum chi1 for given (tau, beta)}}}
"""
import pickle
from operator import itemgetter
from myclass.nested import KLV
from mypathlib import PathTemplate
from fitting import taubeta_rep, taubeta_grid


R_FILE = PathTemplate('$pdata/fit_raw/${taubeta_rep}.pkl')
W_FILE = PathTemplate('$pdata/fit_res/fit_res.pkl')


class FitRes(dict):
    R_FILE = R_FILE
    W_FILE = W_FILE

    def __init__(self, load=True, thr=True):
        if load and thr:
            data = {k: KLV(v) for k, v in self.load_thr().items()}
        elif load and not thr:
            data = {k: KLV(v) for k, v in self.load().items()}
        else:
            data = get_fit_res(dtype=KLV, thr=thr)
        super().__init__(data)

    @property
    def chi1(self):
        return self['chi1']

    @property
    def chi2(self):
        return self['chi2']

    @property
    def sic(self):
        return self['sic']

    def fget(self, tau, beta):
        return self['chi1'][tau][beta], self['chi2'][tau][beta], self['sic'][tau][beta]

    @classmethod
    def dump(cls):
        w_path = cls.W_FILE.substitute()
        with open(w_path, 'wb') as file:
            pickle.dump(get_fit_res(dtype=dict, thr=False), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILE.substitute()
        with open(w_path, 'rb') as file:
            return pickle.load(file)

    @classmethod
    def load_thr(cls):
        chi1s, chi2s, sics = cls.load().values()
        it = ([(tau, beta), (chi1, chi2, sic)]
              for (tau, beta), (chi1, chi2, sic) in KLV.zip_fitems(chi1s, chi2s, sics)
              if chi1 <= 0.07)
        return repackage(it, dtype=dict)


def get_fit_res(dtype, thr=True):
    base_it = iload_thr() if thr else iload()
    unpacked_it = ([taubeta, unpack_min(res)] for taubeta, res in base_it)
    return repackage(unpacked_it, dtype)


def repackage(it, dtype):
    new = {'chi1': dtype(), 'chi2': dtype(), 'sic': dtype()}
    for (tau, beta), (chi1, chi2, sic) in it:
        new['chi1'].setdefault(tau, {})[beta] = chi1
        new['chi2'].setdefault(tau, {})[beta] = chi2
        new['sic'].setdefault(tau, {})[beta] = sic
    return new


def unpack_min(res):
    min_chi1, min_chi2, min_sic = min(zip(*res), key=itemgetter(1))
    return min_chi1, min_chi2, min_sic


def iload_thr():
    for (tau, beta), (chi1s, chi2s, paras) in iload():
        if any(chi1 <= 0.07 for chi1 in chi1s):
            yield (tau, beta), (chi1s, chi2s, paras)


def iload():
    """
    chi1s, chi2s, paras = res
    chi1s: list[float], len=100000
    chi2s: list[float], len=100000
    paras: list[(s, i, c)], len=100000
    """
    for tau, beta in taubeta_grid():
        r_path = R_FILE.substitute(taubeta_rep=taubeta_rep(tau, beta))
        with open(r_path, 'rb') as file:
            res = pickle.load(file)
        yield (tau, round(beta, 1)), res


def update():
    FitRes.dump()
