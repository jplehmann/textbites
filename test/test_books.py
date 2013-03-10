#!/usr/bin/env python
"""
Test functionality of books.
"""

import unittest
import os
import os.path
import json

from books.api import Resource
from books.books import BookResource, Book, Chapter, Lines
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

    chaps = book.get_children()
    self.assertEquals(len(chaps), 3)
    # assert breaks book.text()

    c3 = chaps[2]
    self.assertIsInstance(c3, Chapter)
    self.assertEquals(c3.pretty(), "Chapter 3")
    self.assertEquals(len(c3.get_text()), 687)

    lines = c3.get_children()
    self.assertIsInstance(lines, Lines)
    self.assertEquals(lines.pretty(), "Chapter 3:1-7")
    # assert get_children breaks
    self.assertEquals(len(lines.get_text()), 687)

    # TODO individual line ranges


  
if __name__ == "__main__":
  unittest.main()


