#!/usr/bin/env python
"""
Test functionality of books.
"""
import unittest
import os

from textbites.quotes import QuotesResource


TSV_DATA_FILE = os.path.join(os.path.dirname(__file__), "../textbites/data/Quotes.quotes.tsv")


class TestQuotesBooksImpl(unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  def setUp(self):
    self.res = QuotesResource.from_tsv(TSV_DATA_FILE)
  
  def test_children(self):
    speakers = self.res.top_reference().children()
    self.assertEqual(len(speakers), 187)
    quotes1 = speakers[0].children()
    self.assertEqual(len(quotes1), 3)
    self.assertEqual(speakers[0].pretty(), "Abba Eban")
    quotes2 = speakers[1].children()
    self.assertEqual(len(quotes2), 2)
    self.assertEqual(speakers[1].pretty(), "Abraham Lincoln")

  def test_person_reference(self):
    ref = self.res.reference("Albert Einstein")
    self.assertEqual(len(ref.children()), 7)
    self.assertEqual(ref.pretty(), "Albert Einstein")
    self.assertIn("Make everything as simple as possible, but not simpler.", 
        [r.text() for r in ref.children()])

  def test_person_reference_lower(self):
    ref = self.res.reference("albert einstein")
    self.assertEqual(ref.pretty(), "Albert Einstein")

  def test_search_by_text(self):
    hits = self.res.top_reference().search("simple as possible") 
    self.assertEqual(len(hits), 1)
    self.assertEqual(hits[0].pretty(), "Albert Einstein::3")

  def test_person_quote_id_reference(self):
    ref = self.res.reference("Albert Einstein::3")
    self.assertEqual(ref.text().find("simple as possible"), 19)

  #@unittest.skip("json off")
  #def test_json(self):
  #  speakers = self.res.top_reference().children()
  #  self.assertEquals(len(speakers), 2)
  #  quotes1 = speakers[0].children()
  #  self.assertEquals(len(quotes1), 3)
  #  quotes2 = speakers[1].children()
  #  self.assertEquals(len(quotes2), 4)

