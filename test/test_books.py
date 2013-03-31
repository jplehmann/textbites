#!/usr/bin/env python
"""
Test functionality of books.
"""

import unittest

from test_books_base import TestInterface
from books.books import BookResource


class TestBooksImpl(TestInterface, unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  def setUp(self):
    self.res = BookResource.from_json(TestInterface.data)

  # BookResource chapter-specific tests
#{{{
  def test_chapters(self):
    chaps = self.res.chapters()
    self.assertEquals(len(chaps), 3)

  def test_chapter_length(self):
    chaps = self.res.chapters()
    c3 = chaps[2]
    self.assertEquals(self.res.chapter_length(c3.num()), 7)

  def test_chapter_text_for_whole_chapter_default(self):
    chaps = self.res.chapters()
    c3 = chaps[2]
    text = self.res.chapter_text(c3.num())
    self.assertEquals(len(text), 815)

  def test_chapter_text_for_whole_chapter_from_one(self):
    chaps = self.res.chapters()
    c3 = chaps[2]
    text = self.res.chapter_text(c3.num(), first_line=1)
    self.assertEquals(len(text), 815)

  def test_chapter_text_for_whole_chapter_to_last(self):
    chaps = self.res.chapters()
    c3 = chaps[2]
    last = self.res.chapter_length(c3.num())
    text = self.res.chapter_text(c3.num(), last_line=last)
    self.assertEquals(len(text), 815)

  def test_chapter_text_for_whole_chapter_from_first_to_last(self):
    chaps = self.res.chapters()
    c3 = chaps[2]
    last = self.res.chapter_length(c3.num())
    text = self.res.chapter_text(c3.num(), first_line=1, last_line=last)
    self.assertEquals(len(text), 815)

  def test_lines_for_chapter_whole_chapter(self):
    lines = self.res.lines_for_chapter(3)
    self.assertEquals(len(lines), 7)

  def test_lines_for_chapter_whole_from_one(self):
    lines = self.res.lines_for_chapter(3, 1)
    self.assertEquals(len(lines), 7)

  def test_lines_for_chapter_whole_to_last(self):
    lines = self.res.lines_for_chapter(3, last_line=7)
    self.assertEquals(len(lines), 7)

  def test_lines_for_chapter_from_first_to_last(self):
    lines = self.res.lines_for_chapter(3, 1, 7)
    self.assertEquals(len(lines), 7)
    
#}}}


