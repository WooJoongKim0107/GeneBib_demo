import pickle
import pandas as pd
from Papers import Journal  # Read
from mypathlib import PathTemplate


R_FILE = PathTemplate('$data/journal_curated_220523/wos-core_SCIE_2022-April-19_selected.csv').substitute()
_R_FILE = PathTemplate('$pdata/paper/journal_cache.pkl.gz').substitute()
_W_FILE = PathTemplate('$lite/paper/jnls_selected.pkl').substitute()


def find_from_Journal(wos_title, info):
    match info:
        case {'ISSN': str(issn)} if res := list(Journal.find_issn(issn)):
            return 'ISSN', res
        case {'eISSN': str(issn)} if res := list(Journal.find_issn(issn)):
            return 'eISSN', res
    if res := list(Journal.find_title(wos_title, strict=True)):
        return 'title', res
    else:
        return 'failed', []


def main():
    # journals: dict {journal title (WoS ver) -> journal_info}
    # journal_info: dict {ISSN: _, eISSN: _, ..., WoS category: _}
    journals = pd.read_csv(R_FILE, header=0, index_col=0).T.to_dict()

    q = {k: find_from_Journal(k, v) for k, v in journals.items()}
    for k, (method, result) in q.items():
        assert len(result) == 1 or method == 'failed'

    selected = {k: result[0].medline_ta for k, (method, result) in q.items() if method != 'failed'}
    with open(Journal.SELECTED_PATH, 'wb') as file:
        pickle.dump(selected, file)


if __name__ == '__main__':
    main()
