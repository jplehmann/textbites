#!/usr/bin/env python
"""
API for textual resources. These are abstract base classes.
"""
from collections import namedtuple


class Resource:
  """ Represents a textual resource which can provide references into it.
  """

  def name(self):
    """ Name is the pretty of the top reference.
    """
    return self.top_reference().pretty()

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
  def __init__(self):
    # set parent for children
    if self.children():
      for child in self.children():
        #print "Setting parent of %s to %s" % (child, self)
        child._parent = self

  def resource(self):
    """ Return the resource that this is part of.
    """
    return self.root()._resource

  def pretty(self):
    """ Return a canonical string of this reference.
    """
    raise NotImplementedError()

  def path(self):
    """ Default relative path is pretty() except for root. This is
        because resources are already namespaced under their resource
        name which is this top level description.
    """
    if self == self.root():
      return ""
    return self.pretty()

  def short(self):
    """ Shorter version of pretty with relative information.
        e.g. a line would only include its number.
    """
    return self.pretty()

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

  def parent(self):
    """ Return parent reference or None.
        For this, subclasses must have called Reference's ctor.
    """
    try:
      return self._parent
    except:
      return None

  def root(self):
    """ Top-most reference.
    """
    top = self
    while top.parent() != None:
      top = top.parent()
    return top

  def previous(self):
    """ Return reference for previous or None.
        For this, subclasses must have called Reference's ctor.
    """
    if self.parent():
      try:
        idx = self.parent().children().index(self)
        if idx != -1 and idx >= 1:
          return self.parent()[idx-1]
      except:
        pass
    return None

  def __next__(self):
    """ Return reference for next or None.
        For this, subclasses must have called Reference's ctor.
    """
    if self.parent():
      try:
        idx = self.parent().children().index(self)
        if idx != -1 and idx+1 < len(self.parent()):
          return self.parent()[idx+1]
      except:
        pass
    return None

  def indices(self):
    """ Return a pair of integers representing the order of this reference
    within the resource. Used for determining overlap between references
    in the database. Base on start and end.
    Defined recursively, so only lowest level needs an overridden impl.
    """
    return Index(self.children()[0].indices().start, 
                 self.children()[-1].indices().end)

  def __len__(self):
    if self.children():
      return len(self.children())
    return 0

  def __getitem__(self, key):
    return self.children()[key]

  def __str__(self):
    return "%s:%s" % (type(self), self.pretty())

  def __bool__(self):
    """ Don't want evaluation based on len(). """
    return 1

Index = namedtuple('Index', ['start', 'end'])

class UnparsableReferenceError(Exception):
  """ Reference format is not supported.
  """
  def __init__(self, val=""):
    self.val = val
  def __str__(self):
    return repr(self.val)


class InvalidReferenceError(Exception):
  """ Reference is out of bounds. 
  """
  def __init__(self, val=""):
    self.val = val
  def __str__(self):
    return repr(self.val)
