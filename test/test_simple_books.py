
#!/usr/bin/env python
"""
Test functionality of books.
"""

import unittest

from test_books_base import TestInterface
from books.simple_books import SimpleBookResource


class TestSimpleBooksImpl(TestInterface, unittest.TestCase):
  """ Create the implementation-specific system under test which 
  is the Resource.
  """

  def setUp(self):
    self.res = SimpleBookResource.from_json(TestInterface.data)

