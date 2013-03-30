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

from .simple_books import Book, ChapterRange, Chapter, LineRange, Line

from pybible import api as bibleapi


class BibleResource(Resource):

  @staticmethod
  def init():
    bibleapi.init()

  @staticmethod
  def default_with_simple():
    """ Load the pybible.Bible into SimpleBook data structures.
    """
    bible = bibleapi.get_bible()
    new_books = []
    # this returns book names in order -- and assumes 
    # this implementation has them.
    for book_name in bibleapi.all_book_names():
      book = bible.getBook(book_name)
      new_chapters = []
      for cnum in xrange(1, book.getNumChapters()+1):
        chapter = book.getChapter(cnum)
        assert cnum == chapter.getNumber()
        new_lines = []
        for lnum in xrange(1, chapter.getNumVerses()+1):
          verse = chapter.getVerse(lnum)
          assert lnum == verse.getNumber()
          new_lines.append(Line(cnum, lnum, verse.getText()))
        new_chapters.append(Chapter(cnum, new_lines))
      new_books.append(Book(new_chapters, book_name))
    return BibleResource(Bible(new_books, "default"))

  def __init__(self, bible):
    """ Stores only the top reference.
    """
    self.bible = bible

  def reference(self, str_ref):
    """ Parse this string reference and return an object. 
    Note: this only handles a single reference, and since chapter
    ranges are handled as separate refs, only the first is returned.
    """
    # TODO: reuse this across 3 implementations by passing in a 
    # classname? or factory to produce the objects
    #(text, ref) = bibleapi.get_one_ref(str_ref)
    ## TODO: currently doesn't handle ranges because
    ## it splits those up into multiple references
    #print "types:", str_ref, type(ref)
    #str_ref = str(ref)
    #print ref.book
    #print ref.chapter
    #print ref.verseNums
    #print ref.range
    #return BibleRef(str_ref)
    m = re.match("((?:(?:\d) )?\w+?) (\d+)(?:-(\d+))?(?::(\d+)(?:-(\d+))?)?", str_ref)
    if m:
      book_name = m.group(1)
      chap_start = safe_int(m.group(2))
      chap_end = safe_int(m.group(3))
      start = safe_int(m.group(4))
      end = safe_int(m.group(5))
      print "--"
      book = bibleapi.normalize_book(book_name)
      # TODO: in future when getting ref maybe
      # don't get actual book?
      if book == None:
        raise UnparsableReferenceError()
      #print book, realBook.getName()
      #print chap_start
      #print chap_end
      #print start
      #print end
      #print "--"
      if not start:
        if not chap_end:
          return book.getChapter(chap_start)
        else:
          if chap_end > book.getNumChapters():
            raise InvalidReferenceError()
          return ChapterRange(book, chap_start, chap_end)
      chapter = book.getChapter(chap_start)
      if not end:
        # leverage LineRange to extract a line
        return LineRange(chapter, start, start) #??? .children()[0]
      return LineRange(chapter, start, end)
    raise UnparsableReferenceError()

  def top_reference(self):
    return self.bible


class Bible(Reference):
  """ 
  """
  def __init__(self, books, version):
    self.version = version
    self.books = books

  def children(self):
    return self.books

  def pretty(self):
    return self.version

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern, first_chapter=None, last_chapter=None, 
                            first_line=None, last_line=None):
    # TODO
    raise NotImplementedError()

