from mypathlib import PathTemplate
from EpPatents import START, STOP, MIN_WORKERS
from replicas import Replica


_R_FILE = PathTemplate('$pdata/ep_patent/epoglobal_2023autumn_$number.pkl.gz')
_W_FILES = {'replica': PathTemplate('$pdata/ep_patent/patent_replicas.pkl'),
            'prints': PathTemplate('$pdata/ep_patent/patent_replicas.txt')}


class EpPatentReplica(Replica):
    R_FILE = PathTemplate('$pdata/ep_patent/epoglobal_2023autumn_$number.pkl.gz')
    LOAD_PATH = PathTemplate('$pdata/ep_patent/patent_replicas.pkl').substitute()
    W_FILE = PathTemplate('$pdata/ep_patent/patent_replicas.txt').substitute()
    START = START
    STOP = STOP
    KEY_ATTR = 'pub_number'
    NUM_WORKERS = MIN_WORKERS


main = EpPatentReplica.main


if __name__ == '__main__':
    main()
