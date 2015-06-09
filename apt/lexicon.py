from .apt import APT
from .index import entity_index, relation_index, MockIndex
import base64
# from functools import lru_cache
import plyvel
import os
from struct import pack

def packint(i):
    return pack(">i", i)

class Lexicon(object):
    def __init__(self, directory):
        self.dir = directory

    def __enter__(self):
        self.db = plyvel.DB(self.dir, create_if_missing=False)
        self.entity_index = entity_index(os.path.join(self.dir, "entity-index.tsv.gz"))
        self.relation_index = relation_index(os.path.join(self.dir, "relation-index.tsv.gz"))
        return self

    def __exit__(self, type, value, tb):
        self.db.close()


    def get(self, i):
        from_db = self.db.get(packint(i))
        if from_db:
            return APT.from_byte_array(from_db)
        else:
            return APT()

class MockLexicon(object):
    def __init__(self):
        self.entity_index = MockIndex()
        self.relation_index = MockIndex()
