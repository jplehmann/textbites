#!/usr/bin/env python

import os
import sys
import json

from api import Reference


class ReferenceImpl(Reference):
  """ None means ALL ? 
  Should be complete -- even a Line reference should know
  where it comes from, so have the book and chapter
  Whereas a high level reference will have None for children.

  Should it be able to span chapters? If so need chapters plural,
  else chapter is singular.
  """ 

  def __init__(self, book=None, chapter=None, lines=None):
    """ 
    book = None means 
    None = all chapters or lines

    So a resource with only 1 book should return the book resource? or None?
    Probably either one is okay.
    """
    this.book = book
    this.chapters = chapter
    this.lines = lines


#class Volume (Reference, Searchable)
#  this.books
#
#
#class Book (Reference, Searchable)
#  this.chapters
#
#
#class Chapter (Reference, Searchable)
#  this.lines
#
#
#class Line (Reference)
#  this.string
#

def main():
  # create a Library
  # create a Resource
  # register resource in Library
  # get that resource and test it
  pass


if __name__ == "__main__": 
  main()
