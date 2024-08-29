# About This Repository
This repository contains the code used to produce the core data for the research paper "Long-term Innovative Potential of Genetic Research and Its Suppression". By the end of these demo scripts, you will obtain results such as:

### $${\color{red}\text{Please note that all results presented below are based solely on the demo resource data provided in this repository!!}}$$

## Demo Result 1: Information on Each Gene
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

## Demo Result 3. Mathematical Modeling of New Gene Research Over Time
```python
>>> import numpy as np
>>> from Fitting.fit_sum import TDGs, TRGs, Slopes
>>> _, _, tdg01, _ = map(np.array, zip(*TDGs(load=True).fvalues()))  # tdg01 represents fraction already studied by Dec 31 2001
>>> _, _, trg01, trg21 = map(np.array, zip(*TRGs(load=True).fvalues()))  # trg01 represents fraction already studied by Dec 31 2001
>>> slopes = Slopes().fvalues()
>>> s_counts, s_starts = np.histogram(slopes, np.arange(0.09, 0.2, 0.01)-0.005, density=True)
>>> r_counts, r_starts = np.histogram(trg21, np.arange(0.4, 0.6, 0.01)-0.005, density=True)

>>> print(f'\n{tdg01.mean():.3%} +- {tdg01.std():.3%} taxonomically-dispersed genes (TDGs) studied as of 2021 had already been studied at least once before 2002')
71.315% +- 5.436% taxonomically-dispersed genes (TDGs) studied as of 2021 had already been studied at least once before 2002

>>> print(f'\n{trg01.mean():.3%} +- {trg01.std():.3%} taxonomically-restricted genes (TRGs) studied as of 2021 had already been studied at least once before 2002')
7.963% +- 0.846% taxonomically-restricted genes (TRGs) studied as of 2021 had already been studied at least once before 2002

>>> print(f'\nEstimated fraction of species-specific gene sequences:')
>>> for i in range(s_counts.size):
>>>     print(f'  {s_starts[i]:.3f}-{s_starts[i+1]:.3f}: {s_counts[i]:.2f}')
Estimated fraction of species-specific gene sequences:  
  0.085-0.095: 0.00  
  0.095-0.105: 12.12  
  0.105-0.115: 15.15  
  0.115-0.125: 27.27  
  0.125-0.135: 15.15  
  0.135-0.145: 21.21  
  0.145-0.155: 0.00  
  0.155-0.165: 0.00  
  0.165-0.175: 9.09  
  0.175-0.185: 0.00  
  0.185-0.195: 0.00

>>> print(f'\nEstimated fraction of species-specific genes (-2021):')
>>> for i in range(r_counts.size):
>>>     print(f'  {r_starts[i]:.3f}-{r_starts[i+1]:.3f}: {r_counts[i]:.2f}')  
Estimated fraction of species-specific genes (-2021):  
  0.395-0.405: 0.00  
  0.405-0.415: 0.00  
  0.415-0.425: 0.00  
  0.425-0.435: 6.06  
  0.435-0.445: 6.06  
  0.445-0.455: 12.12  
  0.455-0.465: 21.21  
  0.465-0.475: 15.15  
  0.475-0.485: 12.12  
  0.485-0.495: 9.09  
  0.495-0.505: 6.06  
  0.505-0.515: 9.09  
  0.515-0.525: 3.03  
  0.525-0.535: 0.00  
  0.535-0.545: 0.00  
  0.545-0.555: 0.00  
  0.555-0.565: 0.00  
  0.565-0.575: 0.00  
  0.575-0.585: 0.00
```

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
pip install more-itertools
conda install numpy pandas scipy matplotlib lxml
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
The `Papers` module processes research articles provided in XML format and extracts relevant information from them.

```bash
python -m UsPatents
```
The `UsPatents` module processes US patent documents provided in JSON format and extracts pertinent information from them. During the preprocessing steps for the JSON files, duplicated records belonging to the same DOCDB patent family are resolved.

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

## (Optional) Fitting From Scratch
Although this repository includes the fitting results of the mathematical modeling and their interpretations, those eager to reproduce the fitting results from scratch should run:
```python
python -m Fitting
```

We have only tested this on a system equipped with approximately 300GB of RAM and 48/96 CPU cores/threads, which took about 5 hours. You may need to make slight modifications to the code to ensure it runs properly on your system.

# Contact Information
henrik@unist.ac.kr
