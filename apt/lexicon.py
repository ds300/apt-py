from .apt import APT
# from functools import lru_cache
import plyvel
from os import environ
from struct import pack

def packint(i):
  return pack(">i", i)

class Lexicon(object):
  def __init__(self, directory):
    self.dir = directory

  def __enter__(self):
    self.db = plyvel.DB(self.dir, create_if_missing=False)
    return self

  def __exit__(self, type, value, tb):
    self.db.close() # NOPE switch to leveldb-py ? why are these things so shit?


  def get(self, i):
    gotten = self.db.get(packint(i))
    if gotten:
      return APT.from_byte_array(gotten)
    else:
      return APT()




# @lru_cache(maxSize=environ['APT_CACHE_SIZE'] || 10000)