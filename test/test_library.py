#!/usr/bin/env python
"""
Test functionality of books.
"""

import unittest

from pybooks.api import Resource
from pybooks import library as Library

class TestLibrary(unittest.TestCase):

  def test_library(self):
    r = Resource()
    self.assertEqual(len(Library.list()), 0)
    Library.add("r1", r)
    self.assertEqual(len(Library.list()), 1)
    r1 = Library.get("r1")
    self.assertEqual(r1, r)

