#!/usr/bin/env python
"""
Test functionality of books.
"""

import os
import os.path
import json

from books.api import Reference, InvalidReferenceError


DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/pp-sample.json")


class TestInterface():
  """ Tests the contract for the interfaces Resource and Reference.
  Subclass this and define self.res as the resource.
  """

  @classmethod
  def setUpClass(cls):
    TestInterface.data = json.load(open(DATA_FILE))
    print TestInterface.data

  # Resource top_reference()
  def test_resource_top_reference(self):
    ref = self.res.top_reference()
    self.assertIsInstance(ref, Reference)

  # Resource reference() parsing
  #{{{
  def test_resource_parse_chapter_reference(self):
    ref = self.res.reference("Chapter 2")
    self.assertIsInstance(ref, Reference)
    self.assertEquals(ref.pretty(), "Chapter 2")

  def test_resource_parse_chapter_reference_lower(self):
    ref = self.res.reference("chapter 2")
    self.assertEquals(ref.pretty(), "Chapter 2")

  def test_resource_parse_chapter_reference_without_chapter(self):
    ref = self.res.reference("2")
    self.assertEquals(ref.pretty(), "Chapter 2")

  def test_resource_parse_chapter_range_illegal(self):
    self.assertRaises(InvalidReferenceError, self.res.reference, "chapter 2-5")

  def test_resource_parse_chapter_range_lower(self):
    ref = self.res.reference("chapter 2-3")
    self.assertEquals(ref.pretty(), "Chapter 2-3")

  def test_resource_parse_chapter_reference_with_one_line(self):
    ref = self.res.reference("2:1")
    self.assertEquals(ref.pretty(), "Chapter 2:1")

  def test_resource_parse_line_range_illegal(self):
    self.assertRaises(InvalidReferenceError, self.res.reference, "chapter 2:1-50")

  def test_resource_parse_chapter_reference_with_start_and_end_lines(self):
    ref = self.res.reference("2:1-3")
    self.assertIsInstance(ref, Reference)
    self.assertEquals(ref.pretty(), "Chapter 2:1-3")
  #}}}

  # Reference children(), pretty(), and text()
#{{{
  def test_reference_book_refs(self):
    """ Walk the reference chain, testing children(),
        pretty(), and text() along the way.
    """
    book = self.res.top_reference()
    self.assertIsInstance(book, Reference)
    #self.assertIsInstance(book, Book)
    self.assertEquals(book.pretty(), "PRIDE AND PREJUDICE")
    # cannot get text on a book
    self.assertRaises(NotImplementedError, book.text)

    chaps = book.children()
    self.assertEquals(len(chaps), 3)
    c3 = chaps[2]
    self.assertIsInstance(c3, Reference)
    #self.assertIsInstance(c3, Chapter)
    self.assertEquals(c3.pretty(), "Chapter 3")
    self.assertEquals(len(c3.text()), 817)

    lines = c3.children()
    self.assertEquals(len(lines), 7)
    one_line = lines[-1]
    self.assertIsInstance(one_line, Reference)
    #self.assertIsInstance(one_line, Line)
    self.assertEquals(one_line.pretty(), "Chapter 3:7")
    self.assertEquals(len(one_line.text()), 128)
#}}}

  # Reference search()
#{{{
  def test_book_search(self):
    book = self.res.top_reference()
    hits = book.search("daughter")
    self.assertEquals(len(hits), 3)
    #self.assertIsInstance(hits[0], Line)
    self.assertEquals(hits[0].pretty(), "Chapter 1:2")
    self.assertEquals(hits[1].pretty(), "Chapter 2:4")
    self.assertEquals(hits[2].pretty(), "Chapter 3:1")
    self.assertRaises(NotImplementedError, hits[0].children)
    self.assertTrue(hits[2].text().startswith("Not all that Mrs."))
    self.assertTrue(hits[2].text().endswith("of Mr. Bingley."))

  def test_book_search_one_chapter(self):
    book = self.res.top_reference()
    chaps = book.children()
    c3 = chaps[2]
    hits = c3.search("daughter")
    self.assertEquals(len(hits), 1)
    self.assertEquals(hits[0].pretty(), "Chapter 3:1")

  def test_book_search_from_chapter(self):
    book = self.res.top_reference()
    # chapter 2-
    hits = book.search("daughter", first_chapter=2)
    self.assertEquals(len(hits), 2)
    self.assertEquals(hits[0].pretty(), "Chapter 2:4")

  def test_book_search_to_chapter(self):
    book = self.res.top_reference()
    # chapter -2
    hits = book.search("daughter", last_chapter=2)
    self.assertEquals(len(hits), 2)
    self.assertEquals(hits[0].pretty(), "Chapter 1:2")

  def test_book_search_line_range(self):
    book = self.res.top_reference()
    # chapter 2:1-6
    hits = book.search("Mr\.", first_chapter=2, last_chapter=2, first_line=1, last_line=6)
    self.assertEquals(len(hits), 3)
    self.assertEquals(hits[0].pretty(), "Chapter 2:1")
    self.assertEquals(hits[1].pretty(), "Chapter 2:5")
    self.assertEquals(hits[2].pretty(), "Chapter 2:6")

  def test_book_search_from_line(self):
    book = self.res.top_reference()
    # chapter 2:1-
    hits = book.search("Mr\.", first_chapter=2, last_chapter=2, first_line=2)
    self.assertEquals(len(hits), 2)
    self.assertEquals(hits[0].pretty(), "Chapter 2:5")

  def test_book_search_to_line(self):
    book = self.res.top_reference()
    # chapter 2:-5
    hits = book.search("Mr\.", first_chapter=2, last_chapter=2, last_line=5)
    self.assertEquals(len(hits), 2)
    self.assertEquals(hits[1].pretty(), "Chapter 2:5")

  def test_book_search_of_chapters(self):
    # chapter 2:1-5
    lines = self.res.reference("2-3")
    hits = lines.search("Mr\.")
    self.assertEquals(len(hits), 5)
    self.assertEquals(hits[1].pretty(), "Chapter 2:5")

  def test_book_search_of_lines(self):
    # chapter 2:1-5
    lines = self.res.reference("2:1-5")
    hits = lines.search("Mr\.")
    self.assertEquals(len(hits), 2)
    self.assertEquals(hits[1].pretty(), "Chapter 2:5")
#}}}
  

