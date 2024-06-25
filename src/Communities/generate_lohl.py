import pickle
from mypathlib import PathTemplate
from Communities import Community
Community.import_cache_if_empty()


R_FILES0 = {'paper': PathTemplate('$lite/paper/pmid2year.pkl').substitute(),
            'us_patent': PathTemplate('$lite/us_patent/pubnum2year.pkl').substitute(),
            'cn_patent': PathTemplate('$lite/cn_patent/pubnum2year.pkl').substitute(),
            'ep_patent': PathTemplate('$lite/ep_patent/pubnum2year.pkl').substitute(),}
R_FILES1 = {'paper': PathTemplate('$lite/paper/pmid2cmnt.pkl').substitute(),
            'us_patent': PathTemplate('$lite/us_patent/pubnum2cmnt.pkl').substitute(),
            'cn_patent': PathTemplate('$lite/cn_patent/pubnum2cmnt.pkl').substitute(),
            'ep_patent': PathTemplate('$lite/ep_patent/pubnum2cmnt.pkl').substitute(),}
W_FILES = {'paper': PathTemplate('$pdata/hitgene_list/paper_hitgene_list.txt').substitute(),
           'us_patent': PathTemplate('$pdata/hitgene_list/us_patent_hitgene_list.txt').substitute(),
           'cn_patent': PathTemplate('$pdata/hitgene_list/cn_patent_hitgene_list.txt').substitute(),
           'ep_patent': PathTemplate('$pdata/hitgene_list/ep_patent_hitgene_list.txt').substitute(),}


def write(mtype: str):
    with open(W_FILES[mtype], 'wt') as file:
        file.write('real_key,year,cmnt_idx...\n')
        for x in generate(mtype):
            file.write(','.join(map(str, x)))
            file.write('\n')


def generate(mtype: str):
    with open(R_FILES0[mtype], 'rb') as file:
        pmid2year = pickle.load(file)
    with open(R_FILES1[mtype], 'rb') as file:
        pmid2cmnt = pickle.load(file)

    it = ((pmid, year) for pmid, year in pmid2year.items())  # No recode without valid year - by the construction
    it = ((pmid, year, *pmid2cmnt[pmid]) for pmid, year in it if pmid in pmid2cmnt)  # No recode without hit cmnt
    yield from it


def main():
    for mtype in ['paper',
                  'us_patent',
                  'cn_patent',
                  'ep_patent',]:
        write(mtype)


if __name__ == '__main__':
    main()
