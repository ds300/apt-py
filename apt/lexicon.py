from .apt import APT
import base64
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
    self.db.close()


  def get(self, i):
    from_db = self.db.get(packint(i))
    if from_db:
      return APT.from_byte_array(from_db)
    else:
      return APT()
