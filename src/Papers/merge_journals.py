from collections import Counter


def find_links(cache):
    counter = {}
    for j in cache.values():
        for issn in j.issns:
            counter.setdefault(str(issn), []).append(j)
        counter.setdefault(j.medline_ta.lower().strip(), []).append(j)
    return {edge: neighbors for edge, neighbors in counter.items() if len(neighbors) > 1}


def directly_linked(links):
    neighborhoods = {}
    for edge, neighbors in links.items():
        for nb in neighbors:
            neighborhoods.setdefault(nb, set()).update(neighbors)
    return neighborhoods


def find_clusters(neighborhoods):
    clusters = {}
    for j, neighbors in neighborhoods.copy().items():
        for nb in neighbors:
            if nb in neighborhoods:
                x = neighborhoods.pop(nb)
                clusters.setdefault(j, set()).update(x)
    return clusters


def merge_all_equivalent_journals(cache, clusters):
    merged_cache = cache.copy()
    for k, x in clusters.items():
        for v in x:
            if v is not k:
                k.merge(v)
                merged_cache[v.medline_ta] = k
    return merged_cache


def merge(cache):
    clusters = find_clusters(directly_linked(find_links(cache)))
    counter = Counter(j for x in clusters.values() for j in x)
    assert sum(k for k, v in counter.items() if v > 1) == 0, 'Clustering failed'
    new_cache = merge_all_equivalent_journals(cache, clusters)
    assert len(set(new_cache.values())) == len(set(cache.values())) - len(counter) + len(clusters), 'Merging failed'
    return new_cache
