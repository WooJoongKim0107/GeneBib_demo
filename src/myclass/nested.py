"""
KLV is dictionary of dictionaries with some additional methods.
These additional methods are simply alternatives of dict.keys(), dict.values(), and dict.items()
 and therefore it can be treated as simple Python dictionary object.
"""


class KLV(dict):
    def vkeys(self):
        """
        for lv in self.values():
            for l in lv.keys():
                <...>

        is equivalent to

        for l in self.vkeys():
            <...>
        """
        return vkeys(self)

    def vvalues(self):
        """
        for lv in self.values():
            for v in lv.values():
                <...>

        is equivalent to

        for v in self.vvalues():
            <...>
        """
        return vvalues(self)

    def vitems(self):
        """
        for lv in self.values():
            for l, v in lv.items():
                <...>

        is equivalent to

        for l, v in self.vitems():
            <...>
        """
        return vitems(self)

    def ikeys(self):
        """
        for k, lv in self.items():
            ls = list(lv.keys())
            <...>

        is equivalent to

        for k, ls in self.ikeys():
            <...>
        """
        return ikeys(self)

    def ivalues(self):
        """
        for k, lv in self.items():
            vs = list(lv.values())
            <...>

        is equivalent to

        for k, vs in self.ivalues():
            <...>
        """
        return ivalues(self)

    def iitems(self):
        """
        for k, lv in self.items():
            lvs = list(lv.items())
            <...>

        is equivalent to

        for k, lvs in self.iitems():
            <...>
        """
        return iitems(self)

    def fkeys(self):
        """
        for k, lv in self.items():
            for l in lv.keys():
                <...>

        is roughly equivalent to

        for k, l in self.fkeys():
            <...>
        """
        return fkeys(self)

    def fvalues(self):
        """
        for k, lv in self.items():
            for v in lv.values():
                <...>

        is roughly equivalent to

        for k, v in self.fvalues():
            <...>
        """
        return fvalues(self)

    def fitems(self):
        """
        for k, lv in self.items():
            for l, v in lv.items():
                <...>

        is roughly equivalent to

        for (k, l), v in self.fitems():
            <...>
        """
        return fitems(self)

    def leys(self):
        """
        self.leys() is roughly equivalent to

        set_leys = set()
        for lv in self.values():
            set_leys.update(lv.keys())
        leys = list(set_leys)
        """
        return leys(self)

    def first_key(self):
        return first_key(self)

    def first_lv(self):
        return first_lv(self)

    def first_ley(self):
        return first_ley(self)

    def first_value(self):
        return first_value(self)

    @property
    def transposed(self):
        """
        self: dict, {k -> {l -> v}}
        self.transposed: dict, {l -> {k -> v}}
        """
        return transpose(self, dtype=KLV)

    @staticmethod
    def from_lkv(lkv):
        return transpose(lkv, dtype=KLV)

    @classmethod
    def from_fitems(cls, it):
        return from_fitems(it, dtype=cls)

    def zip_fitems(self, *others):
        for (k, l), v in fitems(self):
            yield (k, l), (v,) + tuple(other[k][l] for other in others)


def vkeys(klv):
    return [list(lv.keys()) for lv in klv.values()]


def vvalues(klv):
    return [list(lv.values()) for lv in klv.values()]


def vitems(klv):
    return [tuple(lv.items()) for lv in klv.values()]


def ikeys(klv):
    return [[k, list(lv.keys())] for k, lv in klv.items()]


def ivalues(klv):
    return [[k, list(lv.values())] for k, lv in klv.items()]


def iitems(klv):
    return [(k, list(lv.items())) for k, lv in klv.items()]


# noinspection PyPep8
def fkeys(klv):
    return [(k, l) for k, lv in klv.items() for l in lv.keys()]


def fvalues(klv):
    return [v for lv in klv.values() for v in lv.values()]


# noinspection PyPep8
def fitems(klv):
    return [((k, l), v) for k, lv in klv.items() for l, v in lv.items()]


# noinspection PyPep8
def tfkeys(klv):
    lk = ((l, k) for k, lv in klv.items() for l in lv.keys())
    return sorted(lk)


# noinspection PyPep8
def tfvalues(klv):
    lk = tfkeys(klv)
    return [klv[k][l] for l, k in lk]


# noinspection PyPep8
def tfitems(klv):
    lk = tfkeys(klv)
    return [((l, k), klv[k][l]) for l, k in lk]


# noinspection PyPep8
def leys(klv):
    # return list(Counter(l for lv in klv.values() for l in lv.keys()))
    return list({l: 0 for lv in klv.values() for l in lv.keys()})


def first_key(klv):
    return next(iter(klv))


def first_lv(klv):
    return next(iter(klv.values()))


def first_ley(klv):
    return next(iter(first_lv(klv)))


def first_value(klv):
    return next(iter(first_lv(klv).values()))


# noinspection PyPep8
def transpose(klv, dtype=dict):
    """{k: {l: v}} -> {l: {k: v}}"""
    lkv = dtype()
    for k, lv in klv.items():
        for l, v in lv.items():
            lkv.setdefault(l, {})[k] = v
    return lkv


# noinspection PyPep8
def from_fitems(it, dtype=dict):
    new = dtype()
    for (k, l), v in it:
        new.setdefault(k, {})[l] = v
    return new