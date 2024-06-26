import gzip
import pickle
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import parse as etree_parse
from myfunc import read_commented
from mypathlib import PathTemplate
from UniProt.containers import Entry, KeyWord


R_FILE0 = PathTemplate('$data/uniprot/uniprot_sprot.xml.gz').substitute()
R_FILE1 = PathTemplate('$data/curations/added/added_key.txt').substitute()
_W_FILES = {'keywords': PathTemplate('$pdata/uniprot/uniprot_keywords.pkl').substitute(),
            'entries': PathTemplate('$pdata/uniprot/uniprot_sprot_parsed.pkl.gz').substitute()}

HEADER = '{http://uniprot.org/uniprot}'
LEN_HEADER = len(HEADER)


def parse_date(x):
    return {k: int(v) for k, v in zip(['Year', 'Month', 'Day'], x.split('-'))}


def as_dict(entry_elt):
    targets = {'accession': [], 'name': [], 'protein': [], 'gene': [], 'reference': []}
    for elt in entry_elt:
        tag = elt.tag[LEN_HEADER:]
        if tag in targets:
            targets[tag].append(elt)
    return targets


def explore(elt, *tags):
    tags = *tags, elt.tag[28:]
    if len(elt):
        for child in elt:
            yield from explore(child, *tags)
    else:
        yield tags, elt.text


def explore_gene(elt, *tags):
    tags = *tags, elt.tag[28:]
    if len(elt):
        for child in elt:
            yield from explore_gene(child, *tags)
    else:
        yield (*tags, elt.attrib['type']), elt.text


def parse_ref(elt: Element):
    cit_elt = elt.find(f'{HEADER}citation')
    for db_ref in cit_elt.findall(f'{HEADER}dbReference'):
        if db_ref.get('type') == 'PubMed':
            pmid = int(db_ref.get('id'))
            break
    else:
        pmid = 0

    return dict(pub_date=parse_date(cit_elt.get('date')),  # YYYY / YYYY-MM / YYYY-MM-DD
                type=cit_elt.attrib.get('type', ''),
                # Counter({'submission': 171924,
                #          'journal article': 1099401,
                #          'thesis': 459,
                #          'book': 1858,
                #          'online journal article': 626,
                #          'unpublished observations': 510,
                #          'patent': 214})
                scopes=[elt.text if elt.text else '' for elt in elt.findall(f'{HEADER}scope')],
                pmid=pmid,  # 9,762 citations (~0.88%) does not include PMID among 1,099,401 journal article citations
                title=cit_elt.findtext(f'{HEADER}title'),)


def simple_parse(entry_elt):
    x = as_dict(entry_elt)
    return dict(created=parse_date(entry_elt.get('created')),  # YYYY-MM-DD
                name=x['name'][0].text,  # one and only one in ['name']
                accessions=[elt.text for elt in x['accession']],
                proteins=[(tag, text) for elt in x['protein'] for tag, text in explore(elt)],
                genes=[(tag, text) for elt in x['gene'] for tag, text in explore_gene(elt)],
                refs=[parse_ref(elt) for elt in x['reference']],)


def fill_cache(x: Element):
    for elt in x:
        Entry.from_parse(simple_parse(elt))


def add_cache():
    with open(R_FILE1, 'r') as file:
        typ = ('protein', 'alternativeName', 'fullName')
        for i, key in enumerate(read_commented(file)):
            Entry.from_parse(dict(name=f'Pseudo_Entry{i}',  # no real entry named such
                                  accessions=[f'PE{i:0>4}'],  # real entry never starts with "PE"
                                  proteins=[(typ, key)],
                                  genes=[],
                                  refs=[],))


def extract_keywords():
    keywords = {}
    for key_acc, entry in Entry.items():
        for k in entry.keywords:
            keywords.setdefault(k, set()).add(key_acc)
    return keywords


def main():
    with gzip.open(R_FILE0, 'rb') as file:
        root = etree_parse(file).getroot()[:-1]

    fill_cache(root)
    add_cache()
    Entry.export_cache()

    keywords = extract_keywords()
    with open(KeyWord.RW_FILE, 'wb') as file:
        pickle.dump(keywords, file)


if __name__ == '__main__':
    main()
