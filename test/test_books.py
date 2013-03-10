#!/usr/bin/env python
"""
Test functionality of books.
"""

import unittest
import os
import os.path
import json

from books.api import Resource
from books.books import BookResource, Book, Chapter, Lines, Line
from books import library as Library


DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/pp-sample.json")


class TestBooks(unittest.TestCase):
  
  def setUp(self):
    self.data = json.load(open(DATA_FILE))

  def test_library(self):
    r = Resource()
    self.assertEqual(len(Library.list()), 0)
    Library.add("r1", r)
    self.assertEqual(len(Library.list()), 1)
    r1 = Library.get("r1")
    self.assertEqual(r1, r)

  def test_book_resource(self):
    print self.data
    bres = BookResource.from_json(self.data)

    book = bres.top_reference()
    self.assertIsInstance(book, Book)
    self.assertEquals(book.pretty(), "PRIDE AND PREJUDICE")
    # cannot get text on a book
    self.assertRaises(NotImplementedError, book.text)

    chaps = book.children()
    self.assertEquals(len(chaps), 3)
    c3 = chaps[2]
    self.assertIsInstance(c3, Chapter)
    self.assertEquals(c3.pretty(), "Chapter 3")
    self.assertEquals(len(c3.text()), 817)

    # TODO rename line above to line range?
    lines = c3.children()
    self.assertIsInstance(lines, Lines)
    self.assertEquals(lines.pretty(), "Chapter 3:1-7")
    self.assertEquals(len(lines.text()), 817)

    line_range = lines.children()
    self.assertEquals(len(line_range), 7)
    one_line = line_range[-1]
    self.assertIsInstance(one_line, Line)
    self.assertEquals(one_line.pretty(), "Chapter 3:7")
    self.assertEquals(len(one_line.text()), 128)


    # TODO individual line ranges
    # adn test open ended ranges

  def test_book_search(self):
    bres = BookResource.from_json(self.data)
    book = bres.top_reference()
    hits = book.search("daughter")
    self.assertEquals(len(hits), 3)
    self.assertIsInstance(hits[0], Line)
    self.assertEquals(hits[0].pretty(), "Chapter 1:2")
    self.assertEquals(hits[1].pretty(), "Chapter 2:4")
    self.assertEquals(hits[2].pretty(), "Chapter 3:1")
    self.assertRaises(NotImplementedError, hits[0].children)
    self.assertTrue(hits[2].text().startswith("Not all that Mrs."))
    self.assertTrue(hits[2].text().endswith("of Mr. Bingley."))

    # TODO put this in a different test
    # TODO: test searching withing different scopes
    # chapter scope
    chaps = book.children()
    c3 = chaps[2]
    chap_hits = c3.search("daughter")
    self.assertEquals(len(chap_hits), 1)
    self.assertEquals(chap_hits[0].pretty(), "Chapter 3:1")

    # Lines scope

  
if __name__ == "__main__":
  unittest.main()


