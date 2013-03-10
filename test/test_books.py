#!/usr/bin/env python
"""
Test functionality of books.
"""

import unittest
import os
import os.path
import json

from books import api, books


DATA = os.path.join(os.path.dirname(__file__), "../data/pp-sample.json")


class TestBooks(unittest.TestCase):
  
  def setUp(self):
    self.sample_book = json.load(open(DATA))
    print self.sample_book

  def test_all(self):
    # create a Library
    # create a Resource
    # register resource in Library
    # get that resource and test it



    ## mp4 count
    #mp4s = [res for res in resources if res[0] == "mp4"]
    #self.assertEqual(len(mp4s), 102)
    pass


  
if __name__ == "__main__":
  unittest.main()


