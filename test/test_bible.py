#!/usr/bin/env python
"""
Test functionality of books.
"""
import unittest
import logging

import test_simple_books

#from test_books_base import TestInterface
from books.bible import BibleResource

# TODO remove this
from pybible import data


TEST_BIBLE = "TEST"


logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

class TestBibleBooksImpl(test_simple_books.TestSimpleBooksImpl, unittest.TestCase):
#class TestBibleBooksImpl(unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  @classmethod
  def setUpClass(cls):
    #BibleResource.init()
    cls.res = BibleResource.with_simple(TEST_BIBLE)

  def setUp(self):
    self.res = TestBibleBooksImpl.res
  
  def get_test_book(self):
    return self.res.top_reference().children()[0]

  #def test_first_and_last_books(self):
  #  bible = self.res.top_reference()
  #  self.assertEquals(len(bible.children()), 66)
  #  self.assertEquals(bible.children()[0].title, "Genesis")
  #  self.assertEquals(bible.children()[-1].title, "Revelation")

  #def test_parse_reference(self):
  #  # Line
  #  ref = self.res.reference("jn 3:16")
  #  self.assertEquals(ref.pretty(), "John 3:16")
  #  # LineRange
  #  ref = self.res.reference("1 jn 4:2-5")
  #  self.assertEquals(ref.pretty(), "1 John 4:2-5")
  #  # Chapter
  #  ref = self.res.reference("jn 3")
  #  self.assertEquals(ref.pretty(), "John 3")
  #  # ChapterRange
  #  ref = self.res.reference("jn 3-4")
  #  self.assertEquals(ref.pretty(), "John 3-4")

  #def test_search(self):
  #  ref = self.res.reference("jn 3")
  #  hits = ref.search("love")
  #  hit_refs = [h.pretty() for h in hits]
  #  self.assertEquals(len(hit_refs), 3)
  #  self.assertTrue("John 3:16" in hit_refs)
  #  self.method()


  ## TODO: move these into Bible project
  #def test_normalize_book_name(self):
  #  self.assertEquals(data.normalize_book_name("John"), "John")
  #  self.assertEquals(data.normalize_book_name("jn"), "John")
  #  self.assertEquals(data.normalize_book_name("jN"), "John")
  #  self.assertEquals(data.normalize_book_name("1jn"), "1 John")
  #  self.assertEquals(data.normalize_book_name("1jn"), "1 John")
  #  self.assertEquals(data.normalize_book_name("mk"), "Mark")


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
