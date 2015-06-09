import gzip

def indices_from_tsv_file(f):
    o = gzip.open if f.endswith(".gz") else open
    val2idx = {}
    idx2val = {}
    with o(f) as r:
        for line in r:
            val, idx_str = line.split("\t")
            idx = int(idx_str)
            val2idx[val] = idx
            idx2val[idx] = val

    return val2idx, idx2val

class MockIndex(object):
    def resolve(self, index):
        return index

    def getIndex(self, value):
        return value

class IntBidirectionalIndexer(object):
    def __init__(self, val2idx=None, idx2val=None):
        self.val2idx = val2idx or {}
        self.idx2val = idx2val or {v: k for k, v in self.val2idx}
        self._nextIndex = reduce(max, self.idx2val.keys(), 0)

    def resolve(self, index):
        return self.idx2val[index]

    def get_index(self, value):
        idx = self.val2idx.get(value, None)
        if idx is None:
            idx = self._nextIndex
            self._nextIndex += 1
            self.val2idx[value] = idx
            self.idx2val[idx] = value
        return idx

    def has_index(self, index):
        return index in self.idx2val

    def has_value(self, value):
        return value in self.val2idx

class RelationIndexer(IntBidirectionalIndexer):
    def has_index(self, index):
        if index < 0:
            return -index in self.idx2val
        else:
            return index in self.idx2val

    def has_value(self, value):
        if value.startswith("_"):
            return value[1:] in self.val2idx
        else:
            return value in self.val2idx

    def resolve(self, index):
        if index < 0:
            rel = self.idx2val[-index]
            if rel:
                return "_" + rel
        else:
            if index not in self.idx2val:
                print "burp", self.idx2val
            return self.idx2val[index]

    def get_index(self, value):
        if value.startswith("_"):
            idx = self.val2idx.get(value[1:], None)
            if idx is None:
                idx = self._nextIndex
                self._nextIndex += 1
                self.idx2val[idx] = value[1:]
                self.val2idx[value[1:]] = idx
            return -idx
        else:
            idx = self.val2idx.get(value, None)
            if idx is None:
                idx = self._nextIndex
                self._nextIndex += 1
                self.idx2val[idx] = value
                self.val2idx[value] = idx
            return idx

def entity_index(f):
    v2i, i2v = indices_from_tsv_file(f)
    return IntBidirectionalIndexer(v2i, i2v)

def relation_index(f):
    v2i, i2v = indices_from_tsv_file(f)
    return RelationIndexer(v2i, i2v)
