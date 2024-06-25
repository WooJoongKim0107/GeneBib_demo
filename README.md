# About This Repository
This repository contains the code used to produce the core data for the research paper "Long-term Innovative Potential of Genetic Research and Its Suppression". By the end of these demo scripts, you will obtain results such as:

## Demo Result 1: Information on Each Genes
```python
>>> from Communities import Community
>>> Community.import_cache()
>>> print(Community[3720].info)
Community(3720), bka., Cas9
       Entries: ['A0Q5Y3', 'A1IQ68', 'C9X1G5', 'G3ECR1', 'J3F2B0', 'J7RUA5', 'Q0P897', 'Q6NKI3', 'Q8DTE3', 'Q927P4', 'Q9CLT2']
      Keywords: ['AnaCas9', 'CRISPR-associated endonuclease Cas9', 'HMPREF1129_2620', 'SaCas9', 'St-Cas9', 'cas9']
    Total hits:
                    388 hits (Paper)
                    353 hits (US Patent)
                    380 hits (CN Patent)
                    350 hits (EP Patent)

>>> print(Community[17386].info)
Community(17386), bka., mTOR
       Entries: ['P42345', 'P42346', 'Q9JLN9']
      Keywords: ['FK506-binding protein 12-rapamycin complex-associated protein 1', 'FKBP12-rapamycin complex-associated protein', 'FRAP1', 'FRAP2', 'Frap', 'Frap1', 'MTOR', 'Mammalian target of rapamycin', 'Mechanistic target of rapamycin', 'Mtor', 'RAFT1', 'RAPT1', 'Raft1', 'Rapamycin and FKBP12 target 1', 'Rapamycin target protein 1', 'Serine/threonine-protein kinase mTOR', 'mTOR']
    Total hits:
                    205 hits (Paper)
                    365 hits (US Patent)
                    393 hits (CN Patent)
                    392 hits (EP Patent)
                    
>>> print(Community[26729].more_info)
Community(26729)
       Entries: ['Q9EP73', 'Q9NZQ7']
      Keywords: ['B7-H1', 'B7H1', 'B7h1', 'CD274', 'Cd274', 'PD-L1', 'PDCD1 ligand 1', 'PDCD1L1', 'PDCD1LG1', 'PDL1', 'Pdcd1l1', 'Pdcd1lg1', 'Pdl1', 'Programmed cell death 1 ligand 1', 'Programmed death ligand 1', 'hPD-L1']
    Total hits:
                    101 hits (Paper)
                    390 hits (US Patent)
                    351 hits (CN Patent)
                    365 hits (EP Patent)
       Details:
                                  Keyword  Paper  US Patent  CN Patent  EP Patent
                                    PD-L1     91        390        351        365
                                     PDL1      4          0          0          0
                                    CD274      3          0          0          0
                programmed death ligand 1      2          0          0          0
                                    Cd274      1          0          0          0
```

## Demo Result 2: Occurrences of Genes Within the Demo Paper and Patent Dataset
```python
>>> from collections import Counter
>>> from Communities import Community
>>> Community.import_cache()
>>> articles = list(Community[3720].get_articles().values())
>>> print(articles[0].info)
Article(24445736)
    Journal: Nat Commun
    PubDate: {'Year': 2014}
   Location: 109
       PMID: 24445736
        URL: https://pubmed.ncbi.nlm.nih.gov/24445736/
      Title: Genotyping with CRISPR-Cas-derived RNA-guided endonucleases.
   Abstract: Restriction fragment length polymorphism (RFLP) analysis is one of the oldest, most convenient and least expensive methods of genotyping, but is limited by the availability of restriction endonuclease sites. Here we present a novel method of employing CRISPR/Cas-derived RNA-guided engineered nucleases (RGENs) in RFLP analysis. We prepare RGENs by complexing recombinant Cas9 protein derived from Streptococcus pyogenes with in vitro transcribed guide RNAs that are complementary to the DNA sequences of interest. Then, we genotype recurrent mutations found in cancer and small insertions or deletions (indels) induced in cultured cells and animals by RGENs and other engineered nucleases such as transcription activator-like effector nucleases (TALENs). Unlike T7 endonuclease I or Surveyor assays that are widely used for genotyping engineered nuclease-induced mutations, RGEN-mediated RFLP analysis can detect homozygous mutant clones that contain identical biallelic indel sequences and is not limited by sequence polymorphisms near the nuclease target sites.
   
>>> yearly_counts = Counter(art.pub_date.get('Year', 0) for art in articles)
>>> dict(sorted(yearly_counts.items()))
{2014: 12,
 2015: 11,
 2016: 25,
 2017: 55,
 2018: 64,
 2019: 76,
 2020: 76,
 2021: 69}
```

Please note that all results presented here are based solely on the demo resource data provided in this repository.

# Data Coverage
Due to GitHub file size limits and legal restrictions on some datasets, we can only provide *demo* versions of the data. You can reproduce the research data by making minor modifications to the Python code if you replace our demo dataset with the complete dataset.

We used four types of raw data for our research:
1. Research paper dataset from PubMed
2. Patent dataset from EPO
3. Protein and gene dataset from UniProtKB
4. Data for filtering non-biological phrases from the Google Books Ngram Corpus

For data (1), we provide most research papers published by Nature Communications if available from PubMed. Due to legal restrictions on data (2), we could not provide any real patent data and have replaced it with imaginary patents generated for this demo. To make the demo results meaningful while adhering to file size limits, we provide the full set of *processed* data for (3) and (4), along with the source code to produce them.

# Requirements
1. Python version 3.11 or higher
2. A minimum of 13GB of available RAM

# Preparation
## Download Codes and Demo Files
You can download the entire repository, including demo resource files, by pressing the "Code" button in the top right corner. Place them in a single directory, such as `GeneBib_demo`.

## Install Python
If Python version 3.11.0 or later is not installed, please follow the instructions on the official website: [Download Python | Python.org](https://www.python.org/downloads/)

## Install Required Libraries
```bash
pip install pandas matplotlib lxml more-itertools
```

## Important
Depending on the number of available CPU threads, you may need to modify `GeneBib_demo/src/system_dep_paras.py` accordingly. The current parameters are based on a system with 32/64 CPU cores/threads. If your system has 8/16 CPU cores/threads, we recommend setting:
```python
"""<GeneBib_demo/src/system_dep_paras.py>"""
MAX_WORKERS = 10
```

Both `MAX_WORKERS` and `MIN_WORKERS` must be set to values less than the total number of threads. Additionally, `MIN_WORKERS` should be constrained by the available RAM. If you have more than 13GB of RAM and your system has more than 10 threads, setting `MIN_WORKERS` to 10 will be sufficient.

# How to Run
First, navigate to the `GeneBib_demo/src` directory, as it must be included in `sys.path`.
```bash
cd /path/to/GeneBib_demo/src
```

Afterward, you can execute the following modules in sequence:
```bash
python -m Papers
```
The `Papers` module processes research articles in XML format and extracts relevant information.

```bash
python -m UsPatents
```
The `UsPatents` module processes US patent documents in JSON format and extracts pertinent information.

```bash
python -m CnPatents
```
Similar to `UsPatents`

```bash
python -m EpPatents
```
Similar to `UsPatents`

```bash
python -m StringMatching
```
The `StringMatching` module identifies occurrences of protein and gene names within research papers and patent documents.

This process typically takes about 2 minutes with `MAX_WORKERS=50`. The required time does not significantly increase as the number of `MAX_WORKERS` decreases, though it may take a few additional minutes.

```bash
python -m Communities
```
The `Communities` module categorizes each occurrence of protein and gene names into the corresponding group of protein and gene entries. For instance, all matches for 'mTOR', 'mechanistic target of rapamycin', and 'mammalian target of rapamycin' are grouped into a single community with the index 17386.

The process described above typically takes approximately 30 minutes when configured with `MAX_WORKERS=50` and `MIN_WORKERS=10`.

Please ensure that the modules are executed in the specified order and verify that each previous run has completed successfully before proceeding.

If all processes complete successfully, you can view the demo results presented at the beginning of this document by running `GeneBib_demo/src/main.py`.

```bash
python main.py
```

# Contact Information
henrik@unist.ac.kr
