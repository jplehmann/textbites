#!/usr/bin/env python
"""
Like a service locator for book resources.
As a module to be a singleton.
"""

_resources = {}


import os.path


def list():
  """ Return list of Resources available in this library.
  """
  return _resources.keys()

def get(name):
  """ Retrieve resource of this name.
  """
  return _resources.get(name)

def add(name, resource):
  """ Add item to the library.
  """
  _resources[name] = resource


# TODO Move this somewhere!!
def load_resources():
  from pybooks.simple_books import SimpleBookResource
  from pybooks.bible import BibleResource
  from pybooks.quotes import QuotesResource
  import json
  try:
    TEST1 = json.load(
        open(os.path.join(os.path.dirname(__file__), "../data/pp-sample.json")))
    add("TEST1", SimpleBookResource.from_json(TEST1))
  except Exception as e:
    print "Couldn't load TEST1: " + str(e)
  try:
    QUOTES = open(os.path.join(os.path.dirname(__file__), "../data/quotes.tsv"))
    add("QUOTES", QuotesResource.from_tsv(QUOTES))
  except Exception as e:
    print "Couldn't load TEST1: " + str(e)
  add("TEST2", BibleResource.with_simple("TEST"))
  add("NASB", BibleResource.with_simple("NASB"))
  add("NIV", BibleResource.with_simple("NIV"))


