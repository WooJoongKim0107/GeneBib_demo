__all__ = ['UsPatent', 'START', 'STOP']
from system_dep_paras import MIN_WORKERS, MAX_WORKERS
from UsPatents.containers import UsPatent
START = 0
STOP = 150

STARTS = [int(STOP/112*i) for i in range(112)]
STOPS = [int(STOP/112*(i+1)) for i in range(112)]
