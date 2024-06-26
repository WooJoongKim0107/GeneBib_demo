import gzip
import pickle
from collections import ChainMap
from mypathlib import PathTemplate


R_FILES = {'ngrams': PathTemplate('$data/wc_ngram_curation/1903182220KPO.${n}gramOnSort'),
           'nonME': PathTemplate('$data/wc_ngram_curation/1908272135ZKO.ngramSorted_nonME').substitute(),
           'answered': PathTemplate('$data/papat_hit_phrase_200517.pkl').substitute(),
           'ngram_counts': PathTemplate('$pdata/ngram/google_ngram_counts.pkl.gz').substitute(),
           'paths': PathTemplate('$lite/match/matched_paths.pkl').substitute(),
           'parents': PathTemplate('$lite/match/matched_parents.pkl').substitute(),
           'counts': PathTemplate('$lite/match/match_counts.pkl').substitute()}
W_FILE = PathTemplate('/home/data/01_data/google_ngrams/to_filter/${n}grams4filter.txt')


def get_answered():
    with open(R_FILES['answered'], 'rb') as file:
        answered = set(pickle.load(file))
    ci_preserved_keys = {}  # ci = case_insensitive
    ci_removed_keys = {}

    def update(f):
        for line in f.read().splitlines()[1:]:
            removed, key, num_paper, paper_hit, ngram_hit = line.split('; ')[:-1]
            answered.add(key)
            if int(removed):
                ci_removed_keys.setdefault(key.lower(), set()).add(key)
            else:
                ci_preserved_keys.setdefault(key.lower(), set()).add(key)

    r_paths = [R_FILES['ngrams'].substitute(n=i) for i in range(1, 7)]
    r_paths.append(R_FILES['nonME'])
    for r_path in r_paths:
        with open(r_path, 'rt') as file:
            update(file)

    return answered, ci_preserved_keys, ci_removed_keys


def get_todo():
    keys = {}
    with open(R_FILES['paths'], 'rb') as file:
        paths = pickle.load(file)
    for key, path in paths.items():
        keys.setdefault(len(path), set()).add(key)

    with open(R_FILES['counts'], 'rb') as file:
        counts = pickle.load(file)

    with open(R_FILES['parents'], 'rb') as file:
        parents = pickle.load(file)
    return keys, counts, parents


def list_up():
    todo, todo_counts, todo_parents = get_todo()
    answered, preserved, removed = get_answered()

    def okay_to_skip(k):
        return any(check_upper(k) <= check_upper(v) for v in removed.get(k.lower(), set())) or \
               any(check_upper(k) >= check_upper(v) for v in preserved.get(k.lower(), set()))

    already = answered.copy()
    keys_to_check = {}
    for n, keys in todo.items():
        for key in keys.difference(answered):
            if len(key) <= 1 or okay_to_skip(key):
                already.add(key)
            else:
                keys_to_check.setdefault(n, set()).add(key)

    with gzip.open(R_FILES['ngram_counts'], 'rb') as file:
        ngram_counts = pickle.load(file)

    def find_where(k):
        if k.lower() in removed:
            return 'removed'
        elif k.lower() in preserved:
            return 'preserved'
        elif k.lower() in answered:
            return 'answered'
        else:
            return 'undetermined'

    summary = {}
    ci_answered = ChainMap(preserved, removed)
    for n, keys in keys_to_check.items():
        temp = []
        for key in keys:
            entries, keywords = todo_parents[key]
            tc = todo_counts[key]
            nc = ngram_counts.get(key, 0)
            where = find_where(key)
            alias = ci_answered.get(key.lower(), '')
            temp.append((key, tc, nc, where, alias, entries, keywords))
        summary[n] = sorted(temp, key=lambda x: (len(x[-3]) > 0, *x[::-1][3:]), reverse=True)

    return summary, already


def check_upper(s: str):
    if s.isupper():
        return 2  # 'UPPER'
    elif s[0].isupper() and not all(v.islower() for v in s[1:]):
        return 3  # 'ATPase'
    elif s[0].isupper() and all(v.islower() for v in s[1:]):
        return 1  # 'Upper'
    elif s.islower():
        return 0  # 'lower'
    else:
        return 1  # 'cAMP'


def main():
    summary, already = list_up()
    for n, x in summary.items():
        with open(W_FILE.substitute(n=n), 'wt') as file:
            file.write('keyword, paper_matches, ngram_counts, case_insensitive_in_removed\n')
            for k, pm, nc, wh, al, entries, keywords in x:
                print(k, pm, nc, wh, al, entries, keywords, sep=', ', end='\n', file=file)
    return summary, already


if __name__ == '__main__':
    q, w = main()
