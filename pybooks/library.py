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


from pybooks.simple_books import SimpleBookResource
import json
TEST1 = json.load(
    open(os.path.join(os.path.dirname(__file__), "../data/pp-sample.json")))
add("TEST1", SimpleBookResource.from_json(TEST1))


