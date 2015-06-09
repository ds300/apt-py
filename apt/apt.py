import struct
import sys

def _read_int (bytes, offset):
    return struct.unpack_from(">i", bytes, offset=offset)[0]

def _read_float (bytes, offset):
    return struct.unpack_from(">f", bytes, offset=offset)[0]


class APT(object):
    """The Anchored-Packed-Tree"""
    def __init__(self):
        self.edges = dict()
        self.counts = dict()
        self.sum = 0

    @staticmethod
    def from_byte_array(bytes):
        _, apt = APT._from_byte_array(bytes, 0, 0, None)
        return apt

    @staticmethod
    def _from_byte_array(bytes, offset, return_path, parent):
        result = APT()

        num_counts = _read_int(bytes, offset) >> 3
        num_kids = _read_int(bytes, offset + 8)
        result.sum = _read_float(bytes, offset + 12)

        offset += 16

        if num_counts > 0:
            for i in xrange(num_counts):
                result.counts[_read_int(bytes, offset)] = _read_float(bytes, offset+4)
                offset += 8

        if parent is not None:
            result.edges[return_path] = parent

        for i in xrange(num_kids):
            edge_label = _read_int(bytes, offset)
            offset, kid = APT._from_byte_array(bytes, offset + 4, -edge_label, result)
            result.edges[edge_label] = kid

        return offset, result

    def __str__(self):
        return "APT of weight " + str(self.sum) + "."

    def write(self, lex, out=sys.stdout):
        self._write_to(out, 0, 0, lex)

    def _write_to(self, out, depth, return_path, lex):
        space = depth * "|   "

        out.write(space + "LABELS\n")
        for k, v in self.counts.iteritems():
            out.write(space + "| " + lex.entity_index.resolve(k) + " (" + str(v) + ")\n")

        out.write(space + "EDGES\n")
        for rel, child in self.edges.iteritems():
            if rel is not return_path:
                out.write(space + "| " + lex.relation_index.resolve(rel) + "\n")
                child._write_to(out, depth+1, -rel, lex)





