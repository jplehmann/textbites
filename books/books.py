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
    """ Chapters should be a list of list of strings.
    """
    self._title = title
    self._author = author
    self._chapters = chapters

  def reference(self, str_ref):
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
    m = re.match("(?:[Cc]hapter ?)?(\d+)(?:-(\d+))?(?::(\d+)(?:-(\d+))?)?", str_ref)
    if m:
      chap_start = m.group(1)
      chap_end = m.group(2)
      start = m.group(3)
      if not start:
        if not chap_end:
          return Chapter(self, int(chap_start))
        else:
          return ChapterRange(self, int(chap_start), int(chap_end))
      end = m.group(4)
      if not end:
        return LineRange(self, int(chap_start), int(start), int(start))
      return LineRange(self, int(chap_start), int(start), int(end))
    raise UnparsableReferenceError()

  def top_reference(self):
    """ Produce Book reference.
    """
    return Book(self)
    
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

  def search(self, pattern):
    return self._resource.search(pattern)


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
    # XXX this is not right
    #return self._resource.chapters_for_chapter(self._chapter_num)
    raise NotImplementedError()

  def pretty(self):
    first = self._first if self._first != None else "*"
    last = self._last if self._last != None else "*"
    return "Chapter %d-%d" % (first, last)

  def text(self):
    #return self._resource.chapter_text(self._chapter_num, self._first, self._last)
    raise NotImplementedError()

  def search(self, pattern):
    return self._resource.search(pattern, 
        first_chapter=self.first, last_chapter=self.last)


class Chapter(ReferenceImpl):
  """ View of a single chapter.
  """
  def __init__(self, resource, chapter_num):
    ReferenceImpl.__init__(self, resource)
    self._chapter_num = chapter_num

  def children(self):
    return self._resource.lines_for_chapter(self._chapter_num)

  def pretty(self):
    return "Chapter %d" % self._chapter_num

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
    """ Maybe unnecessary?
    """
    # XXX this is not right, because it shouldn't return all lines
    #return self._resource.lines_for_chapter(self._chapter_num)
    raise NotImplementedError()

  def pretty(self):
    first = self._first if self._first != None else "*"
    last = self._last if self._last != None else "*"
    s = "Chapter %d:%s" % (self._chapter_num, first)
    return s if first == last else s + "-%s" % last

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
    raise NotImplementedError()


class UnparsableReferenceError(Exception):
  pass

class IllegalSearchError(Exception):
  pass

def zero_indexed(val, none_val=None):
  """ Convert this 1-based index to a 0-based one,
      Also considering that None should not be modified.
  """
  return val-1 if val != None else none_val

def increment(val, none_val=None):
  return val+1 if val != None else none_val

def val_or_default(val, none_val=0):
  return val if val != None else none_val

