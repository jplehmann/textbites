#!/usr/bin/env python
"""
Test functionality of books.
"""
import unittest
import logging
import os

from textbites.quotes import QuotesResource


JSON_DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/quotes.json")
TSV_DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/quotes.tsv")
logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')


class TestQuotesBooksImpl(unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  def setUp(self):
    #self.res = QuotesResource.from_json(json.load(open(JSON_DATA_FILE)))
    self.res = QuotesResource.from_tsv(open(TSV_DATA_FILE))
  
  def test_children(self):
    speakers = self.res.top_reference().children()
    self.assertEquals(len(speakers), 187)
    quotes1 = speakers[0].children()
    self.assertEquals(len(quotes1), 3)
    self.assertEquals(speakers[0].pretty(), "Abba Eban")
    quotes2 = speakers[1].children()
    self.assertEquals(len(quotes2), 2)
    self.assertEquals(speakers[1].pretty(), "Abraham Lincoln")

  def test_person_reference(self):
    ref = self.res.reference("Albert Einstein")
    self.assertEquals(len(ref.children()), 7)
    self.assertEquals(ref.pretty(), "Albert Einstein")
    self.assertIn("Make everything as simple as possible, but not simpler.", 
        [r.text() for r in ref.children()])

  def test_person_reference_lower(self):
    ref = self.res.reference("albert einstein")
    self.assertEquals(ref.pretty(), "Albert Einstein")

  def test_search_by_text(self):
    hits = self.res.top_reference().search("simple as possible") 
    self.assertEquals(len(hits), 1)
    self.assertEquals(hits[0].pretty(), "Albert Einstein::3")

  def test_person_quote_id_reference(self):
    ref = self.res.reference("Albert Einstein::3")
    self.assertEquals(ref.text().find("simple as possible"), 19)

  #@unittest.skip("json off")
  #def test_json(self):
  #  speakers = self.res.top_reference().children()
  #  self.assertEquals(len(speakers), 2)
  #  quotes1 = speakers[0].children()
  #  self.assertEquals(len(quotes1), 3)
  #  quotes2 = speakers[1].children()
  #  self.assertEquals(len(quotes2), 4)

