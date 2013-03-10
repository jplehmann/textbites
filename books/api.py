#!/usr/bin/env python

import os
import sys

"""
API for textual resources.

TODO:
  - how to walk the chain? (next/prev)
"""


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
class Reference(object):
  """ Represents some section of text.
  """
  
  def __init__(self, resource):
    self._resource = resource

  def pretty(self):
    """ Return clean, pretty, canonical string of this reference.
    """
    raise NotImplementedError()

  def text(self):
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

  def children(self):
    """ Return an iterable of References under this item.
    """
    raise NotImplementedError()

