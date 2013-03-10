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

  def chapter_length(self, chapter_num):
    return len(self._chapters[chapter_num-1])

  def chapter_lines_ref(self, chapter_num):
    """ Produce Lines reference.
    """
    return Lines(self, chapter_num, 1, self.chapter_length(chapter_num))

  def chapter_text(self, chapter_num, first_line=None, last_line=None):
    """ Return text from a chapter. If no line numbers are given, it
        returns entire chapter.
    """
    chapter = self._chapters[chapter_num-1]
    first = first_line-1 if first_line != None else None
    return '\n'.join(chapter[first:last_line]).strip()

  def search(self, pattern, chapter_first, chapter_last, line_first, line_last):
    """ Return Line references for search hits within the specified limits.
        Unspecified boundaries default to open ended. e.g. chapter_last being None
        means it will search all following chapters.
    """
    # test illegal combinations
    assert chapter_last != None or chapter_first == None
    assert line_last != None or line_first == None
    assert chapter_first != None or line_first == None
    results = []
    # okay for bounds to be None; works properly
    for i, chapter in enumerate(chapters[chapter_first:chapter_last]):
      for j, line in enumerate(chapter[line_first:line_last], 1):
        if re.search(pattern, line):
          results.append(Line(self, i, j))
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
    return self._resource.search(pattern)


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
    return self_resource.search(
        pattern, chapter_first=self._chapter_num, 
        chapter_last=self._chapter_num)


class Lines(Reference):
  """ Represents 1 or more contiguous lines.
  """
  def __init__(self, resource, chapter_num, first, last):
    """ If a single line, then last == first.
        None means open ended.
    """
    Reference.__init__(self, resource)
    self._chapter_num = chapter_num
    self._first = first
    self._last = last
    assert self._first == None or self._last == None or self._first <= self._last

  def children(self):
    """ Maybe unnecessary?
    """
    # use python slice to handle Nones
    line_nums = range(1, self._resource.chapter_length(self._chapter_num)+1)
    first = self._first-1 if self._first != None else None
    return [Line(self._resource, self._chapter_num, num) 
        for num in line_nums[first:self._last]]

  def pretty(self):
    first = self._first if self._first != None else "*"
    last = self._last if self._last != None else "*"
    s = "Chapter %d:%s" % (self._chapter_num, first)
    return s if first == last else s + "-%s" % last

  def text(self):
    return self._resource.chapter_text(self._chapter_num, self._first, self._last)

  def search(self, pattern):
    cn = self._chapter_num
    return self_resource.search(pattern, 
        chapter_first=cn, chapter_last=cn,
        line_first=self._first, line_last=self._last)


class Line(Lines, Reference):
  """ Represents 1 line.  Implemented as special case of Lines.
  """
  def __init__(self, resource, chapter_num, line_num):
    assert line_num != None
    Lines.__init__(self, resource, chapter_num, line_num, line_num)

  def children(self):
    """ Must raise else will call Lines resulting in loop.
    """
    raise NotImplementedError()




