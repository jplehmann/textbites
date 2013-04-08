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
from api import UnparsableReferenceError
from api import InvalidReferenceError
from .utils import *

from .simple_books import Book, ChapterRange, Chapter, LineRange, Line

from pybible import api as bibleapi


class BibleResource(Resource):

  @staticmethod
  def with_simple(trans=None):
    bibleapi.init(trans)
    """ Load the pybible.Bible into SimpleBook data structures.
    """
    bible = bibleapi.get_bible(trans)
    new_books = []
    # this returns book names in order -- and assumes 
    # this implementation has them.
    for book in bible.getBooks():
      book_name = book.getName()
      #book_name = book.getName() if book_in_refs else "Chapter"
      new_chapters = []
      for cnum in xrange(1, book.getNumChapters()+1):
        chapter = book.getChapter(cnum)
        assert cnum == chapter.getNumber()
        new_lines = []
        for lnum in xrange(1, chapter.getNumVerses()+1):
          verse = chapter.getVerse(lnum)
          assert lnum == verse.getNumber()
          new_lines.append(Line(book_name, cnum, lnum, verse.getText()))
        new_chapters.append(Chapter(book_name, cnum, new_lines))
      new_books.append(Book(new_chapters, book_name))
    return BibleResource(Bible(new_books, bible.getVersion()))

  def __init__(self, bible):
    """ Stores only the top reference.
    """
    # Needs book to be set, now or later!
    self.bible = bible

  def reference(self, str_ref):
    """ Parse this string reference and return an object. 
    Note: this only handles a single reference, and since chapter
    ranges are handled as separate refs, only the first is returned.
    """
    str_ref = str_ref.strip()
    # TODO: reuse this across 3 implementations by passing in a 
    # classname? or factory to produce the objects
    m = re.match("(?:((?:(?:[\d\w]+) )*\w+?) )?(\d+)(?:-(\d+))?(?::(\d+)(?:-(\d+))?)?$", str_ref)
    if m:
      book_name = m.group(1)
      chap_start = safe_int(m.group(2))
      chap_end = safe_int(m.group(3))
      start = safe_int(m.group(4))
      end = safe_int(m.group(5))
      norm_book_name = bibleapi.normalize_book_name(book_name)
      #print book_name, norm_book_name, str_ref, m.groups()
      # handle implied book if they just said "chapter"
      if norm_book_name == None or book_name.lower() == "chapter":
        # if only 1 book, just return that
        if len(self.bible.books) > 1:
          raise UnparsableReferenceError("Book not found: " + book_name)
        book = self.bible.children()[0]
        book_name = book.title
      else:
        book = self.bible.get_book(norm_book_name)
        book_name = norm_book_name
      if not chap_start:
        return book
      # same as simple impl below here except changed self.book to book
      fc = zero_indexed(chap_start)
      if not start:
        if not chap_end:
          return book.children()[fc]
        else:
          if chap_end > len(book.children()):
            raise InvalidReferenceError()
          return ChapterRange(
              book_name, book.children()[fc:chap_end])
      chapter = book.children()[fc]
      if not end:
        # leverage LineRange to extract a line
        return LineRange(book_name, chapter, start, start).children()[0]
      return LineRange(book_name, chapter, start, end)
    # try to match a bookname by itself
    try:
      return self.bible.get_book(str_ref)
    except:
      pass
    norm_book_name = bibleapi.normalize_book_name(str_ref)
    if norm_book_name != None:
      return self.bible.get_book(norm_book_name)
    raise UnparsableReferenceError("Reference didn't match regex: " + str_ref)

  def top_reference(self):
    return self.bible


class Bible(Reference):
  """ 
  """
  def __init__(self, books, version):
    self.version = version
    self.books = books
    Reference.__init__(self)

  def get_book(self, book_name):
    """ Takes normalized book name.
    """
    for book in self.books:
      if book.title == book_name:
        return book
    raise InvalidReferenceError()

  def children(self):
    return self.books

  def pretty(self):
    return self.version

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern, first_chapter=None, last_chapter=None, 
                            first_line=None, last_line=None):
    hits = []
    for book in self.books:
      hits.extend(book.search(pattern, first_line, last_line))
    return hits

