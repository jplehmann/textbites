#! /usr/bin/env python
"""
Adapt Bible API into that which pybooks expects.

reference
  can largely delegate to  pybible

will i have different objects depening onw hat got parsed?
- need to rcognize different types of refs
- need to be able to go through children




"""
import re

from api import Reference
from api import Resource
#from api import UnparsableReferenceError
from api import InvalidReferenceError
from .utils import *

from pybible.loader import loader
from pybible import bibref


class BibleResource(Resource):

  @staticmethod
  def init():
    loader.init()

  @staticmethod
  def load_default():
    return BibleResource()

  def __init__(self):
    """ Stores only the top reference.
    """

  def reference(self, str_ref):
    """ Parse this string reference and return an object. 
    Note: this only handles a single reference, and since chapter
    ranges are handled as separate refs, only the first is returned.
    """
    (text, ref) = bibref.getOneRef(str_ref)
    # TODO: currently doesn't handle ranges because
    # it splits those up into multiple references
    print "types:", str_ref, type(ref)
    str_ref = str(ref)
    print ref.book
    print ref.chapter
    print ref.verseNums
    print ref.range
    return BibleRef(str_ref)

  def top_reference(self):
    return self.book


class BibleRef(Reference):
  """ A single book.
  """
  def __init__(self, pretty):
    self._pretty = pretty

  def children(self):
    raise NotImplementedError()

  def pretty(self):
    return self._pretty

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern, first_chapter=None, last_chapter=None, 
                            first_line=None, last_line=None):
    raise NotImplementedError()



class Book(Reference):
  """ A single book.
  """
  def __init__(self, chapters, title=None, author=None):
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
    return self.chapter.children()[zero_indexed(self.start):self.end]

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
    self.line = line
    self.cnum = cnum
    self.lnum = lnum

  def children(self):
    raise NotImplementedError()

  def pretty(self):
    return "Chapter %d:%d" % (self.cnum, self.lnum)

  def text(self):
    return self.line

  def search(self, pattern):
    if re.search(pattern, self.line):
      return self
    return None


