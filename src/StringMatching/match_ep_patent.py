import gzip
import pickle
from mypathlib import PathTemplate
from EpPatents import EpPatent
from UniProt.containers import Nested


_R_FILE0 = PathTemplate('$pdata/uniprot/nested.pkl')
_R_FILE1 = PathTemplate('$pdata/ep_patent/patent_$index.pkl.gz')
W_FILE = PathTemplate('$pdata/ep_patent/matched/patent_$index.pkl.gz')

NESTED = Nested.load()  # Read0


def match_entire_file(index):
    res = {}
    for pub, ep_pat in EpPatent.load(index).items():  # Read1
        title = NESTED.match_and_filter(ep_pat.title)
        abstract = NESTED.match_and_filter(ep_pat.abstract)
        if title or abstract:
            res[pub] = title, abstract

    with gzip.open(W_FILE.substitute(index=index), 'wb') as file:
        pickle.dump(res, file)
    return index


def main():
    for index in range(112):
        match_entire_file(index)
        print(f'{index}\n', end='')


if __name__ == '__main__':
    main()
