#!/usr/bin/env python

import os
import sys

"""
API for textual resources.

TODO:
  - how to walk the chain? (next/prev)
"""


class Library:
  """ Like a service locator for book resources.
  """
  
  def resources_list(self):
    """ Return list of Resources available in this library.
    """
    raise NotImplementedError()

  def get_resource(self, name):
    """ Retrieve resource of this name.
    """
    raise NotImplementedError()


class Resource:
  """ Represents a textual resource which can provide references into it.
  """

  def from_string(self, string_ref):
    """ Return an object representation of this string.
    """
    raise NotImplementedError()

  def top_reference(self):
    """ Top-most reference for this resource, which can be traversed.
    """
    raise NotImplementedError()


# abstract base class
class Reference:
  """ Represents some section of text.
  """

  def pretty(self):
    """ Return clean, pretty, canonical string of this reference.
    """
    raise NotImplementedError()

  def get_text(self):
    """ Return string of the text corresponding to this reference.
        Should probably be unsupported for entire book.
        NOTE: how is whitespace handled?
    """
    raise NotImplementedError()

  def search(self, pattern):
    """ Return list of Reference which match within this scope, which probably
        indicates line matches.
    """
    raise NotImplementedError()

  def get_children(self):
    """ Return an iterable of References under this item.
    """
    raise NotImplementedError()

