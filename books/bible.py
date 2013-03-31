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
    res = BibleResource()
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
          new_lines.append(Line(res, cnum, lnum, verse.getText()))
        new_chapters.append(Chapter(res, cnum, new_lines))
      new_books.append(Book(res, new_chapters, book_name))
    res.bible = Bible(res, new_books, "default")
    return res

  def __init__(self, bible=None):
    """ Stores only the top reference.
    """
    # Needs book to be set, now or later!
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
      bname = bibleapi.normalize_book_name(book_name)
      if bname == None:
        raise UnparsableReferenceError()
      book = self.bible.get_book(bname)
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
              self, book.children()[fc:chap_end])
      chapter = book.children()[fc]
      if not end:
        # leverage LineRange to extract a line
        return LineRange(self, chapter, start, start).children()[0]
      print start,end, type(start), type(end)
      return LineRange(self, chapter, start, end)
    raise UnparsableReferenceError()
    #  if not start:
    #    if not chap_end:
    #      return xx book.getChapter(chap_start)
    #    else:
    #      if chap_end > xx book.getNumChapters():
    #        raise InvalidReferenceError()
    #      return ChapterRange(xx book, chap_start, chap_end)
    #  # simple excepts an array of line strings
    #  chapter = xx book.getChapter(chap_start).getVerseList()
    #  if not end:
    #    # leverage LineRange to extract a line
    #    return LineRange(chapter, start, start).children()[0]
    #  return LineRange(chapter, start, end)
    #raise UnparsableReferenceError()

  def top_reference(self):
    return self.bible


from simple_books import ReferenceImpl

class Bible(ReferenceImpl):
  """ 
  """
  def __init__(self, resource, books, version):
    ReferenceImpl.__init__(self, resource)
    self.version = version
    self.books = books

  def get_book(self, book_name):
    """ Takes normalized book name.
    """
    for book in self.books:
      if book.title == book_name:
        return book
    return InvalidReferenceError()

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

