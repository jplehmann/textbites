#! /usr/bin/env python
"""
Clean, single interface to Bible code.
"""
import os.path
import data


def bible_file(name):
  #base = os.path.join(os.environ['HOME'], "data/bible/concat")
  # moved into this repo for disting
  # TODO: Load from other project?
  base = os.path.join(os.path.dirname(__file__), "../../data")
  return file(os.path.join(base, name), 'r')


def get_trans_file(trans):
  return bible_file("%s.bible.txt" % trans)


def get_trans_json_file(trans):
  return bible_file("%s.bible.json" % trans)


def abbrToName(abbr): 
  if not abbr: return abbr
  # strip all strings
  abbr = abbr.lower().replace(" ", "")
  if data.BIBLE_ABBR_MAP.has_key(abbr):
    book = data.BIBLE_ABBR_MAP[abbr]
    #log.debug("sucessfully mapped '" + abbr + "' -> '" + book + "'")
    return book
  else:
    return None


def to_book_case(book):
  if book:
    return book.title().replace(' Of', ' of')
  return None


def normalize_book_name(bname):
  """ Convert references to Bible book names into canonical, full form.
  """
  cased_bname = to_book_case(bname)
  if cased_bname in data.BIBLE_ABBRS:
    return cased_bname
  bname = abbrToName(bname)
  return to_book_case(bname)

