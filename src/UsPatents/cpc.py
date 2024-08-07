import pickle
from functools import cached_property
from mypathlib import PathTemplate


R_FILE = PathTemplate('$data/cpc_updated_220525/cpc-keywsrch-total.txt').substitute()
_R_FILE0 = PathTemplate('$data/cpc_updated_220525/cpc-section-${sec}_20220501.txt')
_R_FILE1 = PathTemplate('$data/cpc_updated_220525/cpc-level${i}-titles-filtered_220524.txt')

_RW_FILES = {'tree': PathTemplate('$lite/us_patent/cpc_tree.pkl').substitute(),
             'cpc_selected': PathTemplate('$lite/us_patent/cpc_selected.pkl').substitute(),
             'ipc_selected': PathTemplate('$lite/us_patent/ipc_selected.pkl').substitute(),}


def read_cpc(f):
    x = (v.split('\t') for v in f.read().splitlines())
    code, _, text = next(x)
    yield code, 0, text

    lv1code = '~!@#$%'
    for v in x:
        match v:
            case (code, depth, text) if depth:
                yield code, int(depth) + 3, text

            case (code, '', text) if code.startswith(lv1code):
                yield code, 2, text  # A01B, A01C, ...

            case (code, '', text):
                lv1code = code
                yield code, 1, text  # A01, A21, ...

            case _:
                raise ValueError(f'{f.name} is not valid!')


def parse_hier(f):
    hier = {}
    level = [hier]
    for code, depth, text in read_cpc(f):
        level[depth+1:] = [level[depth].setdefault(code, {})]
    return hier


def get_greped():
    res = []
    with open(R_FILE, 'rt') as file:
        for line in file.read().splitlines():
            res.append(line.split()[0])
    return res


class CPCTree(dict):
    R_FILE = PathTemplate('$data/cpc_updated_220525/cpc-section-${sec}_20220501.txt')
    R_FILE_SELECTED = PathTemplate('$data/cpc_updated_220525/cpc-level${i}-titles-filtered_220524.txt')
    RW_FILE = PathTemplate('$lite/us_patent/cpc_tree.pkl').substitute()
    RW_FILE_SELECTED = PathTemplate('$lite/us_patent/cpc_selected.pkl').substitute()

    def __init__(self, load=True):
        if load:
            data, selected = self.load()
        else:
            data, selected = self.generate()
        super().__init__(data)
        self.selected = selected

    @cached_property
    def all_selected_descendant(self):
        return set(v for x in self.selected for v in self.descendant(x)) | set(self.selected)

    def any_selected(self, cpcs):
        return not self.all_selected_descendant.isdisjoint(cpcs)

    def children(self, target):
        if (path := self.where(target)) is None:
            return None
        return tuple(self.get_from(path))

    def descendant(self, target):
        if (path := self.where(target)) is None:
            return None
        return tuple(_deep_keys(self.get_from(path)))

    def is_descendant(self, sup, inf):
        descendant = self.descendant(sup)
        if (descendant is not None) and inf in descendant:
            return True
        return False

    def is_child(self, parent, child):
        children = self.children(parent)
        if (children is not None) and child in children:
            return True
        return False

    def where(self, target):
        res = tuple(_ascendant(self, target))
        if res == () and target not in self:
            return None
        return res

    def get_from(self, path):
        cur = self
        for key in path:
            cur = cur[key]
        return cur

    def deep_keys(self):
        return _deep_keys(self)

    def deep_items(self):
        return _deep_items(self)

    def dump(self):
        with open(self.RW_FILE, 'wb') as file:
            pickle.dump(dict(self), file)
        with open(self.RW_FILE_SELECTED, 'wb') as file:
            pickle.dump(self.selected, file)

    def load(self):
        with open(self.RW_FILE, 'rb') as file:
            data = pickle.load(file)
        with open(self.RW_FILE_SELECTED, 'rb') as file:
            selected = pickle.load(file)
        return data, selected

    @classmethod
    def generate(cls):
        data = super().__new__(cls)
        data.update(cls._full_hier())
        _selected = cls._get_selected()
        selected = tuple(data._find_highest(_selected))
        return data, selected

    @classmethod
    def _full_hier(cls):
        hier = {}
        for sec in 'ABCDEFGHY':
            with open(cls.R_FILE.substitute(sec=sec), 'rt') as file:  # Read0
                hier.update(parse_hier(file))
        return hier

    @classmethod
    def _get_selected(cls):
        res = []
        for i in range(3, 6):
            with open(cls.R_FILE_SELECTED.substitute(i=i), 'rt') as file:  # Read1
                for line in file.read().splitlines()[1:]:
                    res.append(line.split()[0])
        return res

    def _find_highest(self, x):
        s = set(x)
        anc = '~!@#$%'
        for k in self.deep_keys():
            if (k in s) and not self.is_descendant(anc, k):
                anc = k
                yield k


class IPCTree(CPCTree):
    """
    R_FILE
    """
    R_FILE = PathTemplate('$lite/us_patent/cpc_tree.pkl').substitute()  # NO TYPO HERE
    R_FILE_SELECTED = PathTemplate('$lite/us_patent/ipc_selected.pkl').substitute()  # NO TYPO HERE

    def __init__(self, load=True):
        if load:
            data, selected = self.load()
        else:
            raise NotImplementedError('IPCTree should not generate its contents, but only read those.')
        super().__init__(data)
        self.selected = selected

    @cached_property
    def all_selected_descendant(self):
        return set(v for x in self.selected for v in self.descendant(x)) | set(self.selected)

    def any_selected(self, cpcs):
        return not self.all_selected_descendant.isdisjoint(cpcs)

    def children(self, target):
        if (path := self.where(target)) is None:
            return None
        return tuple(self.get_from(path))

    def descendant(self, target):
        if (path := self.where(target)) is None:
            return None
        return tuple(_deep_keys(self.get_from(path)))

    def is_descendant(self, sup, inf):
        descendant = self.descendant(sup)
        if (descendant is not None) and inf in descendant:
            return True
        return False

    def is_child(self, parent, child):
        children = self.children(parent)
        if (children is not None) and child in children:
            return True
        return False

    def where(self, target):
        res = tuple(_ascendant(self, target))
        if res == () and target not in self:
            return None
        return res

    def get_from(self, path):
        cur = self
        for key in path:
            cur = cur[key]
        return cur

    def deep_keys(self):
        return _deep_keys(self)

    def deep_items(self):
        return _deep_items(self)

    def _find_highest(self, x):
        s = set(x)
        anc = '~!@#$%'
        for k in self.deep_keys():
            if (k in s) and not self.is_descendant(anc, k):
                anc = k
                yield k

    def dump(self):
        raise NotImplementedError('IPCTree should not generate its contents, but only read those.')

    def load(self):
        with open(self.R_FILE, 'rb') as file:
            data = pickle.load(file)
        with open(self.R_FILE_SELECTED, 'rb') as file:
            selected = pickle.load(file)
        return data, selected

    @classmethod
    def generate(cls):
        raise NotImplementedError('IPCTree should not generate its contents, but only read those.')


def _children(x, target):
    if target in x:
        yield from x.keys()
    else:
        for k, v in x.items():
            yield from _children(v, target)


def _ascendant(x, target, *keys):
    if target in x:
        yield from (*keys, target)
    else:
        for k, v in x.items():
            yield from _ascendant(v, target, *keys, k)


def _deep_keys(x):
    for k, v in x.items():
        yield k
        yield from _deep_keys(v)


def _deep_items(x):
    for k, v in x.items():
        yield k, v
        yield from _deep_items(v)


def main():
    cpc_tree = CPCTree(load=False)
    cpc_tree.dump()


if __name__ == '__main__':
    main()
