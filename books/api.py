#!/usr/bin/env python
"""
API for textual resources. These are abstract base classes.
"""


class Resource:
  """ Represents a textual resource which can provide references into it.
  """

  def reference(self, string_ref):
    """ Parse this string reference and return an object. 
        Supports the following formats:
          Chapter N
          chapter N
          N
          Chapter N:M
          Chapter N:M-P
        Doesn't support chapter range
        Doesn't support open ended line ranges
        Currently doesn't do any validation.
    """
    raise NotImplementedError()

  def top_reference(self):
    """ Top-most reference for this resource, which can be traversed.
    """
    raise NotImplementedError()


class Reference(object):
  """ Represents some section of text.
      
      NOTE: in future may want to add:
      - parent()
      - get_number() (e.g. line number), though
        the goal is that the impl doesn't need to have that level of 
        detail.
      - next()/prev() - for walking the chain
  """

  def pretty(self):
    """ Return a canonical string of this reference.
    """
    raise NotImplementedError()

  def text(self):
    """ Return string of the text corresponding to this reference.
        Should probably be unsupported for entire book.
        NOTE: how do we promise to handle whitespace? Currently,
        line ranges are joined by lines.
    """
    raise NotImplementedError()

  def search(self, pattern):
    """ Return list of Reference which match within this scope, which 
        indicate line matches.
    """
    raise NotImplementedError()

  def children(self):
    """ Return an iterable of References under this item.
    """
    raise NotImplementedError()


class UnparsableReferenceError(Exception):
  """ Reference format is not supported.
  """
  pass

class InvalidReferenceError(Exception):
  """ Reference is out of bounds. 
  """
  pass

