#!/usr/bin/env python
"""
An implementation where the actual objects stored are returned to the
user.
"""
import re

from api import Reference, Resource, UnparsableReferenceError, InvalidReferenceError
from .utils import *


class SimpleBookResource(Resource):

  @staticmethod
  def from_json(data):
    """ Create a resource from json data.
        Assumes title, author, chapters/text
    """
    chapters = []
    for cnum, chapter in enumerate(data.get("chapters"), 1):
      lines = []
      for lnum, line in enumerate(chapter.get("text").split('\n'), 1):
        lines.append(Line(cnum, lnum, line))
      chapters.append(Chapter(cnum, lines))
    title = data.get("title")
    author = data.get("author")
    return SimpleBookResource(Book(chapters, title, author))

  def __init__(self, book):
    """ Chapters should be a list of list of strings.
    """
    self.book = book

  def reference(self, str_ref):
    """ Parse this string reference and return an object. 
    """
    m = re.match("(?:[Cc]hapter ?)?(\d+)(?:-(\d+))?(?::(\d+)(?:-(\d+))?)?", str_ref)
    if m:
      chap_start = m.group(1)
      chap_end = m.group(2)
      start = m.group(3)
      fc = zero_indexed(int(chap_start))
      if not start:
        if not chap_end:
          return Chapter(int(chap_start), int(chap_start))
        else:
          if int(chap_end) > len(self.book.children()):
            raise InvalidReferenceError()
          return ChapterRange(
              self.book.children()[fc:int(chap_end)])
      end = m.group(4)
      chapter = self.book.children()[fc]
      if not end:
        return LineRange(chapter, int(start), int(start))
      return LineRange(chapter, int(start), int(end))
    raise UnparsableReferenceError()

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

  def search(self, pattern, first_chapter=None, last_chapter=None, 
                            first_line=None, last_line=None):
    hits = []
    fc = zero_indexed(first_chapter)
    for chap in self.chapters[fc:last_chapter]:
      hits.extend(chap.search(pattern, first_line, last_line))
    return hits


class ChapterRange(Reference):
  """ A range of chapters.
  """
  def __init__(self, chapters):
    self.chapters = chapters

  def children(self):
    return self.chapters

  def pretty(self):
    for c in self.chapters:
        print c.pretty()
    return "Chapter %d-%d" % (self.chapters[0].num, self.chapters[-1].num)

  def text(self):
    raise NotImplementedError()

  def search(self, pattern, first_line=None, last_line=None):
    hits = []
    for chap in self.chapters:
      hits.extend(chap.search(pattern))
    return hits


class Chapter(Reference):
  """ A single chapter.
  """
  def __init__(self, num, lines):
    self.num = num
    self.lines = lines 

  def children(self):
    return self.lines

  def pretty(self):
    return "Chapter %d" % self.num

  def text(self):
    return '\n'.join([l.text() for l in self.lines]).strip()

  def search(self, pattern, first_line=None, last_line=None):
    fl = zero_indexed(first_line)
    return [l for l in self.lines[fl:last_line] if l.search(pattern)]


class LineRange(Reference):
  """ A range of lines.
  """
  def __init__(self, chapter, start, end):
    if end > len(chapter.children()):
      raise InvalidReferenceError()
    self.chapter = chapter
    self.start = start
    self.end = end

  def children(self):
    return self.chapters

  def pretty(self):
    s = self.chapter.pretty() + ":%d" % self.start
    return s if self.start == self.end else s+"-%d" % self.end

  def text(self):
    raise NotImplementedError()

  def search(self, pattern):
    return self.chapter.search(pattern, self.start, self.end)


class Line(Reference):
  """ A single line.
  """
  def __init__(self, cnum, lnum, line):
    #Reference.__init__(self, resource)
    self.line = line
    self.cnum = cnum
    self.lnum = lnum

  def children(self):
    # TODO
    raise NotImplementedError()

  def pretty(self):
    return "Chapter %d:%d" % (self.cnum, self.lnum)

  def text(self):
    return self.line

  def search(self, pattern):
    # TODO
    #return self._resource.search(pattern)
    if re.search(pattern, self.line):
      return self
    return None

