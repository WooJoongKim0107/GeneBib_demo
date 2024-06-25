import gc
import pickle
from mypathlib import PathTemplate
from multiprocessing import Pool
from functools import partial
from Communities import MIN_WORKERS
from Papers import Article
from Papers.article_finder import PmidToIdx
from UsPatents import UsPatent
from CnPatents import CnPatent
from EpPatents import EpPatent


_R_FILES = {'paper': PathTemplate('$pdata/paper/paper_$index.pkl.gz'),
            'us_patent': PathTemplate('$pdata/us_patent/patent_$index.pkl.gz'),
            'cn_patent': PathTemplate('$pdata/cn_patent/patent_$index.pkl.gz'),
            'ep_patent': PathTemplate('$pdata/ep_patent/patent_$index.pkl.gz'),}
W_FILES = {'paper': PathTemplate('$lite/paper/pmid2year.pkl').substitute(),
           'us_patent': PathTemplate('$lite/us_patent/pubnum2year.pkl').substitute(),
           'cn_patent': PathTemplate('$lite/cn_patent/pubnum2year.pkl').substitute(),
           'ep_patent': PathTemplate('$lite/ep_patent/pubnum2year.pkl').substitute(),}


def do(mode, index):
    gc.collect()
    cls, attr = {'paper': (Article, 'pub_date'),
                 'us_patent': (UsPatent, 'filing_date'),
                 'cn_patent': (CnPatent, 'filing_date'),
                 'ep_patent': (EpPatent, 'filing_date'),}[mode]

    res = {}
    for pmid, art in cls.load(index).items():  # R['cls']
        if year := getattr(art, attr).get('Year'):
            res[pmid] = year
    return res


def _main(mode: str):
    max_index = {'paper': PmidToIdx.STOP,
                 'us_patent': 112,
                 'cn_patent': 112,
                 'ep_patent': 112,}[mode]

    pmid2year = {}
    func = partial(do, mode)
    with Pool(MIN_WORKERS) as p:
        for res in p.imap_unordered(func, range(max_index)):  # If you encounter error here, manually modify Line39
            pmid2year.update(res)

    with open(W_FILES[mode], 'wb') as file:
        pickle.dump(pmid2year, file)


def main():
    for mode in ['paper', 'us_patent', 'cn_patent', 'ep_patent']:
        _main(mode)


if __name__ == '__main__':
    main()
