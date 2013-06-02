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
  return sorted(_resources.keys())

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
  from textbites.simple_books import SimpleBookResource
  from textbites.quotes import QuotesResource
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

  # Bible-based resources
  for trans in ["TEST2", "NASB", "NIV", "NKJV", "NLT"]:
    try:
      from textbites.bible.bible import BibleResource
      add(trans, BibleResource.from_fastformat(trans))
    except Exception as e:
      print "Could not load pybible-based resourcse. ", e


