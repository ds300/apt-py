from numpy import array
from scipy import sparse, float32
import struct

def _read_int (bytes, offset):
  return struct.unpack_from(">i", bytes, offset)

def _read_float (bytes, offset):
  return struct.unpack_from(">f", bytes, offset)

class APT:
  """The Anchored-Packed-Tree"""
  def __init__(self):
    self.edges = dict()
    self.counts = sparse.csr_matrix((1,1), dtype=float32)
    self.sum = 0

  @staticmethod
  def from_byte_array(bytes):
    _, apt = _from_byte_array(bytes, 0, 0, None)
    return apt

  @staticmethod
  def _from_byte_array(bytes, offset, return_path, parent):
    result = APT()

    num_counts = _read_int(bytes, offset) >> 3
    num_kids = _read_int(bytes, offset + 8)
    result.sum = _read_int(bytes, offset + 12)

    offset += 16

    if num_counts > 0:
      keys = []
      vals = []
      for i in xrange(num_counts):
        keys[i] = _read_int(bytes, offset)
        offset += 4
        vals[i] = _read_float(bytes, offset)
        offset += 4
      result.counts = sparse.csr_matrix(keys, vals, [0, num_counts])

    if parent != None:
      result.edges[return_path] = parent

    for i in xrange(num_kids):
      edge_label = _read_int(bytes, offset)
      offset, kid = _from_byte_array(bytes, offset + 4, -edge_label, result)
      result.edges[edge_label] = kid

    return offset, result


