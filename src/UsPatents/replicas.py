from mypathlib import PathTemplate
from UsPatents import START, STOP, MIN_WORKERS
from replicas import Replica


_R_FILE = PathTemplate('$pdata/us_patent/epoglobal_2023autumn_$number.pkl.gz')
_W_FILES = {'replica': PathTemplate('$pdata/us_patent/patent_replicas.pkl'),
            'prints': PathTemplate('$pdata/us_patent/patent_replicas.txt')}


class UsPatentReplica(Replica):
    R_FILE = PathTemplate('$pdata/us_patent/epoglobal_2023autumn_$number.pkl.gz')
    LOAD_PATH = PathTemplate('$pdata/us_patent/patent_replicas.pkl').substitute()
    W_FILE = PathTemplate('$pdata/us_patent/patent_replicas.txt').substitute()
    START = START
    STOP = STOP
    KEY_ATTR = 'pub_number'
    NUM_WORKERS = MIN_WORKERS


main = UsPatentReplica.main


if __name__ == '__main__':
    main()
