#! /usr/bin/env python
"""
Subclass of SimpleBook for Bible which includes parsing a JSON format
and resolving references.
"""
import re
import logging
import json

from textbites.api import Reference
from textbites.api import Resource
from textbites.api import UnparsableReferenceError
from textbites.api import InvalidReferenceError
from textbites.utils import *
from textbites.simple_books import Book, ChapterRange, Chapter, LineRange, Line

from . import bibleapi

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger(__name__)


class BibleResource(Resource):

  @staticmethod
  def from_json(json_filename=None):
    """ Load the bible into SimpleBook data structures.
    """
    bible = json.load(open(json_filename, 'r'))
    new_books = []
    # this returns book names in order -- and assumes 
    # this implementation has them.
    line_num = 0
    for book in bible['books']:
      book_name = book['name']
      new_chapters = []
      for chapter in book['chapters']:
        #assert cnum == chapter.getNumber()
        cnum = chapter['num']
        new_lines = []
        for line in chapter['verses']:
          line_num += 1
          #assert lnum == verse.getNumber()
          new_lines.append(Line(book_name, cnum, line['num'], line['text'], line_num))
        new_chapters.append(Chapter(book_name, cnum, new_lines))
      new_books.append(Book(new_chapters, book_name))
    bible_ref = Bible(new_books, bible['version'])
    bible_ref._resource = BibleResource(bible_ref)
    return bible_ref.resource()

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
        if len(self.top_reference().books) > 1:
          raise UnparsableReferenceError("Book not found: " + book_name)
        book = self.top_reference().children()[0]
        book_name = book.title
      else:
        book = self.top_reference().get_book(norm_book_name)
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
      return self.top_reference().get_book(str_ref)
    except:
      pass
    norm_book_name = bibleapi.normalize_book_name(str_ref)
    if norm_book_name != None:
      return self.top_reference().get_book(norm_book_name)
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

