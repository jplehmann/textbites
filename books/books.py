#!/usr/bin/env python

import os
import sys
import json

from api import Reference
from api import Resource


class BookResource(Resource):

  @staticmethod
  def from_json(data):
    """ Create a resource from json data.
        Assumes title, author, chapters/text
    """
    title = data.get("title")
    author = data.get("author")
    chapters = []
    for chapter in data.get("chapters"):
      lines = chapter.get("text").split('\n')
      chapters.append(lines)
    return BookResource(title, author, chapters)

  def __init__(self, title, author, chapters):
    """
    Chapters should be a list of list of strings.
    """
    self._title = title
    self._author = author
    self._chapters = chapters

  def top_reference(self):
    """ Produce Book reference.
    """
    return Book(self)
    
  def chapter_refs(self):
    """ Produce list of Chapter reference.
    """
    c_refs = []
    for i, chapter in enumerate(self._chapters, 1):
      c_refs.append(Chapter(self, i))
    return c_refs

  def chapter_lines_ref(self, chapter_num):
    """ Produce Lines reference.
    """
    return Lines(self, chapter_num, 1, len(self._chapters[chapter_num-1]))

  def chapter_text(self, chapter_num, first_line=None, last_line=None):
    """ Return text from a chapter. If no line numbers are given, it
        returns entire chapter.
    """
    chapter = self._chapters[chapter_num-1]
    if first_line == None:
      first_line = 1
      last_line = len(chapter)
    return '\n'.join(chapter[first_line-1:last_line-1]).strip()

  def search(self, pattern):
    results = []
    for i, chapter in enumerate(self._chapters, 1):
      for j, line in enumerate(chapter, 1):
        if re.search(pattern, line):
          results.add(i, j)
    # TODO: create References
    return results


"""
create a reference (view), and give it a reference name
then when it wants anything, use that string

No, reference really needs to be able to get its own stuff
It should call methods on the bookresource, like getChapter()

Why not just give it back a book then, why give it a reference?
I think the answer is a) this is the composite pattern which
makes traversal easier. b) give it a object handle instead of
string ref handles

Restrictions:
1. single book
2. lines must be contiguous
3. can only reference a chapter at a time?
4. saves no paragraph whitespace
"""


class Book(Reference):
  """ Represents a single book.
  """
  def __init__(self, resource):
    Reference.__init__(self, resource)

  def children(self):
    return self._resource.chapter_refs()

  def pretty(self):
    return self._resource._title

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern):
    # TODO
    pass


class Chapter(Reference):
  """ Represents a single chapter.
  """
  def __init__(self, resource, chapter_num):
    Reference.__init__(self, resource)
    self._chapter_num = chapter_num

  def children(self):
    return self._resource.chapter_lines_ref(self._chapter_num)

  def pretty(self):
    return "Chapter %d" % self._chapter_num

  def text(self):
    return self._resource.chapter_text(self._chapter_num)

  def search(self, pattern):
    # TODO
    pass


class Lines(Reference):
  """ Represents 1 or more contiguous lines.
  """
  def __init__(self, resource, chapter_num, first, last=None):
    """ If a single line, then last == first (None okay too)
    """
    Reference.__init__(self, resource)
    self._chapter_num = chapter_num
    self._first = first
    self._last = last if last != None else first
    assert self._first != None and self._first <= self._last

  def children(self):
    raise NotImplementedError()

  def pretty(self):
    s = "Chapter %d:%d" % (self._chapter_num, self._first)
    return s if self._first == self._last else s + "-%d" % self._last

  def text(self):
    return self._resource.chapter_text(self._chapter_num, self._first, self._last)

  def search(self, pattern):
    raise NotImplementedError()



