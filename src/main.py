from collections import Counter
import numpy as np
from Communities import Community
from Fitting.fit_sum import TDGs, TRGs, Slopes
Community.import_cache()

if __name__ == '__main__':
    print('\n\n')
    print('========< About each communities or gene >========\n')
    print(Community[3720].info)
    print(Community[17386].info)
    print(Community[26729].more_info)

    print('========< About their occurrences within papers and patents >========\n')
    articles = list(Community[3720].get_articles().values())
    print(articles[0].info)
    yearly_counts = Counter(art.pub_date.get('Year', 0) for art in articles)
    print('Yearly occurrences of Cas9 (demo result)')
    for year, count in sorted(yearly_counts.items()):
        print(f'  {year}: {count}')
        
    print('\n========< Modeling Results >========\n')
    _, _, tdg01, _ = map(np.array, zip(*TDGs(load=True).fvalues()))  # tdg01 represents fraction already studied by Dec 31 2001
    _, _, trg01, trg21 = map(np.array, zip(*TRGs(load=True).fvalues()))  # trg01 represents fraction already studied by Dec 31 2001
    slopes = Slopes().fvalues()
    s_counts, s_starts = np.histogram(slopes, np.arange(0.09, 0.2, 0.01)-0.005, density=True)
    r_counts, r_starts = np.histogram(trg21, np.arange(0.4, 0.6, 0.01)-0.005, density=True)

    print(f'\n{tdg01.mean():.3%} +- {tdg01.std():.3%} taxonomically-dispersed genes (TDGs) studied as of 2021 had already been studied at least once before 2002')
    print(f'\n{trg01.mean():.3%} +- {trg01.std():.3%} taxonomically-restricted genes (TRGs) studied as of 2021 had already been studied at least once before 2002')
    print(f'\nEstimated fraction of species-specific gene sequences:')
    for i in range(s_counts.size):
        print(f'  {s_starts[i]:.3f}-{s_starts[i+1]:.3f}: {s_counts[i]:.2f}')
    print(f'\nEstimated fraction of species-specific genes (-2021):')
    for i in range(r_counts.size):
        print(f'  {r_starts[i]:.3f}-{r_starts[i+1]:.3f}: {r_counts[i]:.2f}')    

