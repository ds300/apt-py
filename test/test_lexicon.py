import unittest
import apt

class TestLexicon(unittest.TestCase):
  def runTest(self):
    print "apt dir"
    print dir(apt)
    with apt.Lexicon("db") as lex:
      self.assertEqual(lex.get(1), "jub") 