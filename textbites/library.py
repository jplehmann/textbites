#!/usr/bin/env python
"""
Like a service locator for book resources.
As a module to be a singleton.
"""

import os
import re
import os.path

_resources = {}



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

def load(datafile):
  """ Returns true if loaded.
  """
  from textbites.simple_books import SimpleBookResource
  from textbites.quotes import QuotesResource
  from textbites.bible.bible import BibleResource

  suffix_map = { "simple.json" : SimpleBookResource.from_json,
                 "quotes.tsv" : QuotesResource.from_tsv,
                 "bible.json" : BibleResource.from_json }

  # load file according to its type based on the map
  for pattern in suffix_map:
    if (datafile.endswith(pattern)):
      file_handle = suffix_map.get(pattern)(datafile)
      add(re.sub("\." + pattern + "$", "", os.path.basename(datafile)), file_handle)
      return True

  return False

def dynamically_load_dir(dirname):
  """ Load resources in given directory based on suffix.
  """
  for f in os.listdir(dirname):
    print f
    datafile = os.path.join(dirname, f)

    # don't load files staring with underscore
    if (f.startswith("_")):
      continue

    if not load(datafile):
      print "Unknown resource format for file:", f

  print "Dynamically loaded library of:", _resources.keys()


# TODO Move this somewhere!!
def load_resources():
  # for disting
  data_dir = os.path.join(os.path.dirname(__file__), "data")
  dynamically_load_dir(data_dir)

  #from textbites.simple_books import SimpleBookResource
  #from textbites.quotes import QuotesResource
  #import json
  #try:
  #  TEST1 = json.load(
  #      open(os.path.join(os.path.dirname(__file__), "data/pp-sample.json")))
  #  add("TEST1", SimpleBookResource.from_json(TEST1))
  #except Exception as e:
  #  print "Couldn't load TEST1: " + str(e)
  #try:
  #  QUOTES = open(os.path.join(os.path.dirname(__file__), "data/quotes.tsv"))
  #  add("QUOTES", QuotesResource.from_tsv(QUOTES))
  #except Exception as e:
  #  print "Couldn't load TEST1: " + str(e)

  ## Bible-based resources
  #for trans in ["TEST2", "NASB", "NIV", "NKJV", "NLT"]:
  #  try:
  #    from textbites.bible.bible import BibleResource
  #    add(trans, BibleResource.from_fastformat(trans))
  #  except Exception as e:
  #    print "Could not load pybible-based resourcse. ", e


#dynamically_load_dir("/home/john/git/textbites/data")
