#!/usr/bin/env python
"""
Test functionality of books.
"""
import unittest
import logging

#from test_simple_books import TestSimpleBooksImpl

#from test_books_base import TestInterface
from books.bible import BibleResource


logging.basicConfig(level=logging.WARN, format='%(name)s: %(message)s')

#class TestBibleBooksImpl(TestSimpleBooksImpl, unittest.TestCase):
class TestBibleBooksImpl(unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  @classmethod
  def setUpClass(cls):
    BibleResource.init()

  def setUp(self):
    self.res = BibleResource.default_with_simple()

  def test_load_simple_adapter(self):
    print len(self.res.top_reference().children())

  def test_first_and_last_books(self):
    bible = self.res.top_reference()
    self.assertEquals(len(bible.children()), 66)
    self.assertEquals(bible.children()[0].title, "Genesis")
    self.assertEquals(bible.children()[-1].title, "Revelation")

  def test_parse_reference(self):
    ref = self.res.reference("jn 3:16")
    self.assertEquals(ref.pretty(), "John 3:16")

  """
TODO: Move to bible project
#from pybible.bibref import BibleReference
#from pybible.bibref import newBibleReferences
#from pybible.bibref import newBibleText
#from pybible.loader import loader
#from pybible import data
TRANS = data.DEFAULT_VERSION
  @unittest.skip
  def test_test(self):
    ref = self.res.reference("jn 3:16")
    ref = self.res.reference("1 jn 3:16")
    ref = self.res.reference("1 jn 3:16-17")
    ref = self.res.reference("1 jn 3-4")
    ref = self.res.reference("1 asdf 3-4")
    #self.assertEquals(ref.pretty(), "John 3:16")

  @unittest.skip
  def test_one(self):
    ref = self.res.reference("jn 3:16")
    self.assertEquals(ref.pretty(), "John 3:16")

  @unittest.skip
  def test_whole_book(self):
    ref = self.res.reference("jn")
    # NOTE: currently only returns first in a range
    # doesn't handle whole chapters
    self.assertEquals(ref.pretty(), "John")

  @unittest.skip
  def test_chapter_range(self):
    ref = self.res.reference("jn 3-4")
    # NOTE: currently only returns first in a range
    self.assertEquals(ref.pretty(), "John 3")

  @unittest.skip
  def test_bible_reference_parsing(self):
    #ref = newBibleReferences("jn 3:16")
    #bibleTexts = parseBibleReferences("jn 3:16")
    bibleTexts = newBibleText("jn 3:16; jn 3:17")
    bt = bibleTexts[0]
    self.assertEquals(str(bt.reference), "John 3:16")

  @unittest.skip
  def test_bible_direct_lookup(self):
    # From bibref.BibleText.
      # given a BibleReference, returns a string of content?
      # self.text = loader.getTranslationText(ref, trans)
    # 
    ref = BibleReference("John", 3, [16], TRANS)
    text = loader.getTranslationText(ref, TRANS)
    self.assertRegexpMatches(text, "so loved the world")
  """
