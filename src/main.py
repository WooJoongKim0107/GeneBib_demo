from collections import Counter
from Communities import Community
Community.import_cache()

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

