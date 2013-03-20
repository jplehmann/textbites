#!/usr/bin/env python
"""
An implementation where the actual objects stored are returned to the
user.
"""
import re

from api import Reference
from api import Resource


class SimpleBookResource(Resource):

  @staticmethod
  def from_json(data):
    """ Create a resource from json data.
        Assumes title, author, chapters/text
    """
    chapters = []
    for chapter in data.get("chapters"):
      lines = []
      for line in chapter.get("text").split('\n'):
        lines.append(line)
      chapters.append(Chapter(lines))
    title = data.get("title")
    author = data.get("author")
    return SimpleBookResource(Book(chapters, title, author))

  def __init__(self, book):
    """ Chapters should be a list of list of strings.
    """
    self.book = book

  def reference(self, str_ref):
    pass

  def top_reference(self):
    return self.book


class Book(Reference):
  """ A single book.
  """
  def __init__(self, chapters, title=None, author=None):
    #Reference.__init__(self, resource)
    self.chapters = chapters
    self.author = author
    self.title = title

  def children(self):
    return self.chapters

  def pretty(self):
    return self.title

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern):
    # TODO
    #return self._resource.search(pattern)
    raise NotImplementedError()


def Chapter(Reference):
  """ A single chapter.
  """
  def __init__(self, lines):
    #Reference.__init__(self, lines)
    self.lines = lines 

  def children(self):
    return self.lines

  def pretty(self):
    # TODO
    #return self._resource._title
    raise NotImplementedError()

  def text(self):
    return '\n'.join(self.lines).strip()

  def search(self, pattern):
    # TODO
    #return self._resource.search(pattern)
    raise NotImplementedError()


def Line(Reference):
  """ A single line.
  """
  def __init__(self, line):
    #Reference.__init__(self, resource)
    self.line = line

  def children(self):
    # TODO
    raise NotImplementedError()

  def pretty(self):
    # TODO
    #return self._resource._title
    raise NotImplementedError()

  def text(self):
    return self.line

  def search(self, pattern):
    # TODO
    #return self._resource.search(pattern)
    raise NotImplementedError()

