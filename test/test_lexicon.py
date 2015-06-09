import unittest
import apt

class TestLexicon(unittest.TestCase):
    def runTest(self):
        with apt.Lexicon("db") as lex:
            clothes = lex.get(19)
            clothes.write(lex)

