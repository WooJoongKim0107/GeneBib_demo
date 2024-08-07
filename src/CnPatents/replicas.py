from mypathlib import PathTemplate
from CnPatents import START, STOP, MIN_WORKERS
from replicas import Replica


_R_FILE = PathTemplate('$pdata/cn_patent/epoglobal_2023autumn_$number.pkl.gz')
_W_FILES = {'replica': PathTemplate('$pdata/cn_patent/patent_replicas.pkl'),
            'prints': PathTemplate('$pdata/cn_patent/patent_replicas.txt')}


class CnPatentReplica(Replica):
    R_FILE = PathTemplate('$pdata/cn_patent/epoglobal_2023autumn_$number.pkl.gz')
    LOAD_PATH = PathTemplate('$pdata/cn_patent/patent_replicas.pkl').substitute()
    W_FILE = PathTemplate('$pdata/cn_patent/patent_replicas.txt').substitute()
    START = START
    STOP = STOP
    KEY_ATTR = 'pub_number'
    NUM_WORKERS = MIN_WORKERS


main = CnPatentReplica.main


if __name__ == '__main__':
    main()
