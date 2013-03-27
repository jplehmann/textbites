#!/usr/bin/env python
"""
Test functionality of books.
"""
import unittest
import logging

#from test_books_base import TestInterface
from books.bible import BibleResource


logging.basicConfig(level=logging.WARN, format='%(name)s: %(message)s')

#class TestBibleBooksImpl(TestInterface, unittest.TestCase):
class TestBibleBooksImpl(unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  @classmethod
  def setUpClass(cls):
    BibleResource.init()

  def setUp(self):
    self.res = BibleResource.load_default()

  def test_one(self):
    ref = self.res.reference("jn 3:16")
    self.assertEquals(ref.pretty(), "John 3:16")

  def test_two(self):
    ref = self.res.reference("jn 3-4")
    print ref
    self.assertEquals(ref.pretty(), "John 3-4")


      

