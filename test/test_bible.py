#!/usr/bin/env python
"""
Test functionality of books.
"""
import unittest

from textbites.bible.bible import BibleResource

import test_simple_books

TEST_BIBLE = "TEST"


class TestBibleBooksImpl(test_simple_books.TestSimpleBooksImpl, unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  @classmethod
  def setUpClass(cls):
    cls.res = BibleResource.from_json(TEST_BIBLE)

  def setUp(self):
    self.res = TestBibleBooksImpl.res
  
  def get_test_book(self):
    return self.res.top_reference().children()[0]


class TestBibleBooksImplWithBible(unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  These are Bible-specific tests (on the Bible text).
  """

  @classmethod
  def setUpClass(cls):
    cls.res = BibleResource.from_json("NKJV")

  def test_first_and_last_books(self):
    bible = self.res.top_reference()
    self.assertEquals(len(bible.children()), 66)
    self.assertEquals(bible.children()[0].title, "Genesis")
    self.assertEquals(bible.children()[-1].title, "Revelation")

  def test_parse_reference(self):
    # Line
    ref = self.res.reference("jn 3:16")
    self.assertEquals(ref.pretty(), "John 3:16")
    # LineRange
    ref = self.res.reference("1 jn 4:2-5")
    self.assertEquals(ref.pretty(), "1 John 4:2-5")
    # Chapter
    ref = self.res.reference("jn 3")
    self.assertEquals(ref.pretty(), "John 3")
    # Chapter
    ref = self.res.reference("john 3")
    self.assertEquals(ref.pretty(), "John 3")
    # ChapterRange
    ref = self.res.reference("jn 3-4")
    self.assertEquals(ref.pretty(), "John 3-4")
    # Book
    ref = self.res.reference("1 jn")
    self.assertEquals(ref.pretty(), "1 John")

  def test_search_chapter(self):
    ref = self.res.reference("jn 3")
    hits = ref.search("love")
    hit_refs = [h.pretty() for h in hits]
    self.assertEquals(len(hit_refs), 3)
    self.assertTrue("John 3:16" in hit_refs)

  def test_search_book(self):
    ref = self.res.reference("jn")
    hits = ref.search("believe")
    hit_refs = [h.pretty() for h in hits]
    self.assertEquals(len(hit_refs), 84)
    self.assertTrue("John 5:24" in hit_refs)

  # TODO: move these into simple but I wanted
  # easy test cases
  # Move into base, but only if I make the other impls
  # support it
  def test_previous_edge(self):
    ref = self.res.reference("jn 3:1")
    self.assertEquals(ref.previous(), None)
    ref = self.res.reference("jn 3:2")
    self.assertEquals(ref.previous().pretty(), "John 3:1")

  def test_next(self):
    ref = self.res.reference("jn 3:16")
    self.assertEquals(ref.next().pretty(), "John 3:17")

  def test_next_edge(self):
    ref = self.res.reference("jn 3:36")
    self.assertEquals(ref.next(), None)
    ref = self.res.reference("jn 3:35")
    self.assertEquals(ref.next().pretty(), "John 3:36")

  def test_parent_line(self):
    ref = self.res.reference("jn 3:1")
    self.assertEquals(ref.parent().pretty(), "John 3")

  def test_parent_line_group(self):
    ref = self.res.reference("jn 3:1-3")
    self.assertEquals(ref.parent().pretty(), "John 3")
  
  def test_parent_chapter(self):
    ref = self.res.reference("jn 3")
    self.assertEquals(ref.parent().pretty(), "John")

  def test_chapter_length(self):
    ref = self.res.reference("jn 3")
    self.assertEquals(len(ref), 36)

  def test_book_length(self):
    ref = self.res.reference("jn")
    self.assertEquals(len(ref), 21)

  def test_indices_line(self):
    ref1 = self.res.reference("jn 3:1")
    ref2 = self.res.reference("jn 3:2")
    self.assertTrue(ref1.indices().start == ref1.indices().end)
    self.assertTrue(ref2.indices().start == ref2.indices().end)
    self.assertTrue(ref1.indices().start < ref2.indices().start)
    self.assertTrue(ref1.indices().end < ref2.indices().end)
    self.assertTrue(ref1.indices().end < ref2.indices().start)

  def test_indices_range(self):
    ref1 = self.res.reference("jn 3:1-3")
    ref2 = self.res.reference("jn 3:2")
    self.assertTrue(ref1.indices().start < ref1.indices().end)
    self.assertTrue(ref1.indices().start < ref2.indices().start)
    self.assertTrue(ref1.indices().end > ref2.indices().end)
    self.assertTrue(ref1.indices().end > ref2.indices().start)

  def test_indices_chapter(self):
    ref1 = self.res.reference("jn 3")
    self.assertTrue(ref1.indices().start < ref1.indices().end)
    ref2 = self.res.reference("jn 3:1-36")
    ref3 = self.res.reference("jn 2:25")
    ref4 = self.res.reference("jn 4:1")
    self.assertTrue(ref1.indices().start == ref2.indices().start)
    self.assertTrue(ref1.indices().end == ref2.indices().end)
    self.assertTrue(ref3.indices().end < ref1.indices().start)
    self.assertTrue(ref4.indices().start > ref1.indices().end)

  #def test_line_length(self):
  #  ref = self.res.reference("jn 3:1")
  #  self.assertEquals(len(ref), None)

  def test_path(self):
    ref = self.res.reference("jn 3:1-3")
    self.assertEquals(ref.path(), "John 3:1-3")

  # TODO: move these into Bible project
  def test_normalize_book_name(self):
    from textbites.bible.bibleapi import normalize_book_name
    self.assertEquals(normalize_book_name("John"), "John")
    self.assertEquals(normalize_book_name("jn"), "John")
    self.assertEquals(normalize_book_name("jN"), "John")
    self.assertEquals(normalize_book_name("1jn"), "1 John")
    self.assertEquals(normalize_book_name("1jn"), "1 John")
    self.assertEquals(normalize_book_name("mk"), "Mark")



  """
TODO: Move to bible project
#from pybible.bibref import BibleReference
#from pybible.bibref import newBibleReferences
#from pybible.bibref import newBibleText
#from pybible.loader import loader
#from pybible import data

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
