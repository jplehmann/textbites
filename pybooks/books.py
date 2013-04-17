#!/usr/bin/env python
"""
This implementation of Resource and Reference provides references as views. The
references do not actually contain the data, but they contain the information
necessary to retrieve the data from the resource. Data is stored in the Resource
in lists of strings.

Another implementation might actually store the data in the same sorts of
objects which are handed back as references to the user.

The purpose of references is like the composite pattern, to allow the user to
easily traverse the structure while providing abstraction about the types of
objects being handled. Also, there is less overhead because the references
are not created until they are needed.

Restrictions:
1. single book
2. lines must be contiguous
3. can only reference a chapter at a time?
4. saves no paragraph whitespace
"""
import re

from api import Reference, Resource, UnparsableReferenceError, InvalidReferenceError
from .utils import *

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
      lines = [l.strip() for l in chapter.get("text").split('\n')]
      chapters.append(lines)
    res = BookResource(title, author, chapters)
    top_ref = res.top_reference()
    top_ref._resource = res
    return top_ref.resource()

  def __init__(self, title, author, chapters):
    """ Chapters should be a list of list of strings.
    """
    self._title = title
    self._author = author
    self._chapters = chapters

  def reference(self, str_ref):
    """ Parse this string reference and return an object. 
    """
    m = re.match("(?:(?:\w+ )*\w+ ?)?(\d+)(?:-(\d+))?(?::(\d+)(?:-(\d+))?)?", str_ref)
    if m:
      chap_start = m.group(1)
      chap_end = m.group(2)
      start = m.group(3)
      if not chap_start:
        return self.top_reference()
      if not start:
        if not chap_end:
          return Chapter(self, int(chap_start))
        else:
          if int(chap_end) > len(self._chapters):
            raise InvalidReferenceError()
          return ChapterRange(self, int(chap_start), int(chap_end))
      end = m.group(4)
      if not end:
        return Line(self, int(chap_start), int(start))
      if int(end) > self.chapter_length(int(chap_start)):
        raise InvalidReferenceError()
      return LineRange(self, int(chap_start), int(start), int(end))
    raise UnparsableReferenceError()

  def top_reference(self):
    """ Produce Book reference.
    """
    return Book(self)

  def title(self):
    return self._title
    
  def chapters(self):
    """ Produce list of Chapter reference.
    """
    c_refs = []
    for i, chapter in enumerate(self._chapters, 1):
      c_refs.append(Chapter(self, i))
    return c_refs

  def chapter_length(self, chapter_num):
    return len(self._chapters[zero_indexed(chapter_num)])

  def linegroup_for_chapter(self, chapter_num):
    """ Produce LineRange reference.
        Not really used any longer.
    """
    return LineRange(self, chapter_num, 1, self.chapter_length(chapter_num))

  def lines_for_chapter(self, chapter_num, first_line=None, last_line=None):
    # use python slice to handle Nones
    # create range so we have numbers for line numbers
    first = val_or_default(first_line, 1)
    last = val_or_default(last_line, self.chapter_length(chapter_num))
    return [Line(self, chapter_num, n) for n in range(first, last+1)]

  def chapter_text(self, chapter_num, first_line=None, last_line=None):
    """ Return text from a chapter. If no line numbers are given, it
        returns entire chapter.
    """
    chapter = self._chapters[zero_indexed(chapter_num)]
    return '\n'.join(chapter[zero_indexed(first_line):last_line]).strip()

  def search(self, pattern, first_chapter=None, last_chapter=None, 
                            first_line=None, last_line=None):
    """ Return Line references for search hits within the specified limits.
        Unspecified boundaries default to open ended. e.g. last_chapter being None
        means it will search all following chapters.
    """
    #print "chap boundary", first_chapter, last_chapter, first_line, last_line
    # don't allow line ranges across multiple chapters
    if ((first_chapter != last_chapter) and 
        not (first_line == None and last_line == None)):
      raise IllegalSearchError
    results = []
    # last value doesn't have to be converted since it's an exclusive selection
    fl = zero_indexed(first_line)
    fc = zero_indexed(first_chapter)
    line_offset = val_or_default(fl)
    chap_offset = val_or_default(fc)
    # slicing the arrays works well for handling None, but the challenge is
    # those items iterated over don't know what their numeric index is, so we
    # have to track the enumeration and an offset.
    for i, chapter in enumerate(self._chapters[fc:last_chapter], 1):
      for j, line in enumerate(chapter[fl:last_line], 1):
        #print "Searching chapter:verse", i, j
        if re.search(pattern, line):
          results.append(Line(self, i+chap_offset, j+line_offset))
    return results


class ReferenceImpl(Reference):
  """ Represents some section of text.
  """
  def __init__(self, resource):
    self._resource = resource


class Book(ReferenceImpl):
  """ View of a single book.
  """
  def __init__(self, resource):
    ReferenceImpl.__init__(self, resource)

  def children(self):
    return self._resource.chapters()

  def pretty(self):
    return self._resource._title

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern, first_chapter=None, last_chapter=None, 
                            first_line=None, last_line=None):
    return self._resource.search(pattern, 
        first_chapter, last_chapter, first_line, last_line)


class ChapterRange(ReferenceImpl):
  """ View of 1 or more contiguous chapters. This is not returned
      as a result of Reference.children() for consistency, but it is
      the result of calls to Resource.reference() for convenience.
  """
  def __init__(self, resource, first, last):
    """ If a single chapter, then last == first.
        None means open ended.
    """
    ReferenceImpl.__init__(self, resource)
    self._first = first
    self._last = last
    assert self._first <= self._last

  def children(self):
    """ Maybe unnecessary?
    """
    fc = zero_indexed(self._first)
    return self._resource.chapters()[fc:self._last]

  def pretty(self):
    first = self._first if self._first != None else "*"
    last = self._last if self._last != None else "*"
    return self._resource.title() + " %d-%d" % (first, last)

  def text(self):
    raise NotImplementedError()

  def search(self, pattern):
    return self._resource.search(pattern, 
        first_chapter=self._first, last_chapter=self._last)


class Chapter(ReferenceImpl):
  """ View of a single chapter.
  """
  def __init__(self, resource, chapter_num):
    ReferenceImpl.__init__(self, resource)
    self._chapter_num = chapter_num

  def children(self):
    return self._resource.lines_for_chapter(self._chapter_num)

  def pretty(self):
    return self._resource.title() + " %d" % self._chapter_num

  def text(self):
    return self._resource.chapter_text(self._chapter_num)

  def search(self, pattern):
    return self._resource.search(
        pattern, first_chapter=self._chapter_num, 
        last_chapter=self._chapter_num)

  def num(self):
    return self._chapter_num


class LineRange(ReferenceImpl):
  """ View of 1 or more contiguous lines. This is not returned
      as a result of Reference.children() for consistency, but it is
      the result of calls to Resource.reference() for convenience.
  """
  def __init__(self, resource, chapter_num, first, last):
    """ If a single line, then last == first.
        None means open ended.
    """
    ReferenceImpl.__init__(self, resource)
    self._chapter_num = chapter_num
    self._first = first
    self._last = last
    assert self._first <= self._last
    assert self._first == None or self._last == None or self._first <= self._last

  def children(self):
    """ Return Line(s) for chapter.
    """
    return self._resource.lines_for_chapter(self._chapter_num, 
        self._first, self._last)

  def pretty(self):
    first = self._first if self._first != None else "*"
    last = self._last if self._last != None else "*"
    s = self._resource.title() + " %d:%d" % (self._chapter_num, first)
    return s if first == last else s + "-%d" % last

  def text(self):
    return self._resource.chapter_text(self._chapter_num, self._first, self._last)

  def search(self, pattern):
    cn = self._chapter_num
    return self._resource.search(pattern, 
        first_chapter=cn, last_chapter=cn,
        first_line=self._first, last_line=self._last)


class Line(LineRange, ReferenceImpl):
  """ View of 1 line.  Implemented as special case of LineRange.
  """
  def __init__(self, resource, chapter_num, line_num):
    assert line_num != None
    LineRange.__init__(self, resource, chapter_num, line_num, line_num)

  def children(self):
    """ Must raise else will call LineRange resulting in loop.
    """
    return None


class IllegalSearchError(Exception):
  pass

