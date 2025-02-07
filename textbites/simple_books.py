#!/usr/bin/env python
"""
An implementation where the actual objects stored are returned to the
user.
"""
import re
import logging

from .api import Reference, Resource, UnparsableReferenceError, InvalidReferenceError, Index
from .utils import *
import json

log = logging.getLogger(__name__)


class SimpleBookResource(Resource):

  @staticmethod
  def from_json(json_filename):
    """ Create a XXX book & resource from json data.
        Assumes title, author, chapters/text
    """
    data = json.load(open(json_filename, 'r'))
    chapters = []
    title = data.get("title")
    author = data.get("author")
    line_num = 0
    for cnum, chapter in enumerate(data.get("chapters"), 1):
      lines = []
      for lnum, line in enumerate(chapter.get("text").split('\n'), 1):
        line_num += 1
        lines.append(Line(title, cnum, lnum, line.strip(), line_num))
      chapters.append(Chapter(title, cnum, lines))
    book = Book(chapters, title, author)
    book._resource = SimpleBookResource(book)
    #return book
    return book.resource()

  def __init__(self, book):
    """ Stores only the top reference.
    """
    self.book = book

  def reference(self, str_ref):
    """ Parse this string reference and return an object. 
    """
    m = re.match("(?:(?:\w+ )*\w+ ?)?(\d+)(?:-(\d+))?(?::(\d+)(?:-(\d+))?)?", str_ref)
    #book_name = "Chapter"
    book_name = self.top_reference().title
    if m:
      chap_start = safe_int(m.group(1))
      chap_end = safe_int(m.group(2))
      start = safe_int(m.group(3))
      end = safe_int(m.group(4))
      fc = zero_indexed(chap_start)
      if not chap_start:
        return self.top_reference()
      if not start:
        if not chap_end:
          return self.top_reference().children()[fc]
        else:
          if chap_end > len(self.top_reference().children()):
            raise InvalidReferenceError()
          return ChapterRange(book_name,
              self.top_reference().children()[fc:chap_end])
      chapter = self.top_reference().children()[fc]
      if not end:
        # leverage LineRange to extract a line
        return LineRange(book_name, chapter, start, start).children()[0]
      return LineRange(book_name, chapter, start, end)
    raise UnparsableReferenceError("Reference didn't match regex.")

  def top_reference(self):
    return self.book


class ReferenceImpl(Reference):
  """ Represents some section of text.
  """
  def __init__(self):
    Reference.__init__(self)


class Book(ReferenceImpl):
  """ A single book.
  """
  def __init__(self, chapters, title=None, author=None):
    self.chapters = chapters
    self.author = author
    self.title = title
    ReferenceImpl.__init__(self)

  def children(self):
    return self.chapters

  def pretty(self):
    return self.title

  def short(self):
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


class ChapterRange(ReferenceImpl):
  """ A range of chapters.
  """
  def __init__(self, book, chapters):
    """ chapters is an array of Chapter objects.
    """
    self.book = book 
    self.chapters = chapters
    self.first = self.chapters[0].num
    self.last = self.chapters[-1].num
    # don't overwrite parent! ReferenceImpl.__init__(self)

  def children(self):
    return self.chapters

  def pretty(self):
    return "%s %d-%d" % (
        self.book, self.first, self.last)

  def short(self):
    return "%d-%d" % (self.first, self.last)

  def text(self):
    raise NotImplementedError()

  def search(self, pattern, first_line=None, last_line=None):
    hits = []
    for chap in self.chapters:
      hits.extend(chap.search(pattern))
    return hits

  def parent(self):
    return self.book


class Chapter(ReferenceImpl):
  """ A single chapter.
  """
  def __init__(self, book, num, lines):
    self.book = book
    self.num = num
    self.lines = lines 
    ReferenceImpl.__init__(self)

  def children(self):
    return self.lines

  def pretty(self):
    return "%s %d" % (self.book, self.num)

  def short(self):
    return str(self.num)

  def text(self):
    return '\n'.join([l.text() for l in self.lines]).strip()

  def search(self, pattern, first_line=None, last_line=None):
    fl = zero_indexed(first_line)
    return [l for l in self.lines[fl:last_line] if l.search(pattern)]
    # unfold list
    #return [inner for outer in lists for inner in outer]


class LineRange(ReferenceImpl):
  """ A range of lines.
  """
  def __init__(self, book, chapter, start, end):
    """ chapter is a Chapter object.
    """
    if end > len(chapter.children()):
      raise InvalidReferenceError("%d > the # chapters" % end)
    self.book = book
    self.chapter = chapter
    self.start = start
    self.end = end
    # don't overwrite parent! ReferenceImpl.__init__(self)

  @staticmethod
  def from_lines(lines):
    """ From a list of Line objects.
    """
    if not lines:
      raise InvalidReferenceError("can't create LineRange from 0 lines");
    chapter = lines[0].parent()
    book = chapter.parent()
    return LineRange(book, chapter, lines[0].lnum, lines[-1].lnum)

  def children(self):
    return self.chapter.children()[zero_indexed(self.start):self.end]

  def pretty(self):
    s = self.chapter.pretty() + ":%d" % self.start
    return s if self.start == self.end else s+"-%d" % self.end

  def short(self):
    return "%d-%d" % (self.first, self.last)

  def text(self):
    return " ".join([l.text() for l in 
        self.chapter.children()[self.start-1:self.end]])

  def search(self, pattern):
    return self.chapter.search(pattern, self.start, self.end)

  def parent(self):
    return self.chapter


class Line(ReferenceImpl):
  """ A single line.
  """
  def __init__(self, book, cnum, lnum, line, line_num):
    self.book = book
    self.line = line
    self.cnum = cnum
    self.lnum = lnum
    self.line_num = line_num
    ReferenceImpl.__init__(self)

  def children(self):
    return None

  def pretty(self):
    return "%s %d:%d" % (self.book, self.cnum, self.lnum)

  def short(self):
    return str(self.lnum)

  def text(self):
    return self.line

  def search(self, pattern):
    """ Return a list for consistency.
    """
    if re.search(pattern, self.line):
      return [self]
    return []

  def context(self, size):
    """ Return a line range of references including self, with its
        'size' number of siblings before and after.
    """
    siblings = self.parent().children()
    idx = siblings.index(self)
    # ending index beyond size is not a problem for slice
    return LineRange.from_lines(siblings[max(idx-size, 0):idx+size+1])

  def indices(self):
    return Index(self.line_num, self.line_num)


