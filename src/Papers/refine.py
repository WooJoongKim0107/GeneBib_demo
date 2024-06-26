import gc
import gzip
import pickle
from multiprocessing import Pool
from lxml.etree import _Element as Element
from lxml.etree import parse
from mypathlib import PathTemplate
from Papers import START, STOP, MAX_WORKERS
from Papers.containers import Article, Journal  # Read0
from Papers.parse import parse_article, find_journal_key


_R_FILE0 = PathTemplate('$pdata/paper/journal_cache.pkl.gz').substitute()
_R_FILE1 = PathTemplate('$data/paper/pubmed22n$number.xml.gz', key='{:0>4}'.format)
_W_FILES = {'refined': PathTemplate('$pdata/paper/article22n$number.pkl.gz', key='{:0>4}'.format),
            'message': PathTemplate('$pdata/paper/article22n$number.txt', key='{:0>4}'.format)}


class Refine:
    R_FILE = PathTemplate('$data/paper/pubmed22n$number.xml.gz', key='{:0>4}'.format)
    W_FILES = {'refined': PathTemplate('$pdata/paper/article22n$number.pkl.gz', key='{:0>4}'.format),
               'message': PathTemplate('$pdata/paper/article22n$number.txt', key='{:0>4}'.format)}
    START = START
    STOP = STOP
    JNL = Journal

    @classmethod
    def read_eng_articles(cls, number):
        with gzip.open(cls.R_FILE.substitute(number=number)) as file:
            tree = parse(file)
        return tree.getroot().findall("./PubmedArticle/MedlineCitation/Article/Language[.='eng']/../../..")

    @classmethod
    def refine_article(cls, number, pubmed_article_elt: Element):
        article = Article.from_parse(*parse_article(pubmed_article_elt))
        article.location = number
        article._journal_title = cls.report_journal(number, pubmed_article_elt, article.pmid)
        return article

    @classmethod
    def write(cls, number):
        gc.collect()
        eng_arts = cls.read_eng_articles(number)
        res = [cls.refine_article(number, pubmed_article_elt) for pubmed_article_elt in eng_arts]
        with gzip.open(cls.W_FILES['refined'].substitute(number=number), 'wb') as file:
            pickle.dump(res, file)
        print(number)

    @classmethod
    def main(cls):
        with Pool(MAX_WORKERS) as p:
            p.map(cls.write, range(cls.START, cls.STOP))

    @classmethod
    def report_journal(cls, number, pubmed_article_elt: Element, pmid):
        key = find_journal_key(pubmed_article_elt)
        if key not in cls.JNL:
            with open(cls.W_FILES['message'].substitute(number), 'a') as file:
                file.write(f'Cannot find appropriate Journal for {number}: {pmid}\n')
        return key


main = Refine.main


if __name__ == '__main__':
    main()
