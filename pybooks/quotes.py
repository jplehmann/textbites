

#!/usr/bin/env python
"""
Quotes are arranged by a top level which is the speaker name and then the quotes.
"""
import re
import logging

from api import Reference, Resource, UnparsableReferenceError, InvalidReferenceError
from .utils import *
from collections import defaultdict

log = logging.getLogger(__name__)


class QuotesResource(Resource, Reference):

  REF_DELIM = ':'

  @staticmethod
  def from_tsv(data):
    # multimap
    quote_dict = defaultdict(list)
    for line in data.readlines():
      vals = line.strip().split("\t")
      # assume if only 2 then date is missing
      if len(vals) == 2:
        vals.insert(1, None)
      # date must have a number in it
      if len(vals) == 3:
        name, date, quote = vals
        if date and not re.search("\d", date):
          log.debug("Discarding w/ no date: %s", vals)
        # name must be <= 4 tokens
        elif len(name.split(' ')) > 4:
          log.debug("Discarding b/c name too long: %s", vals)
        else:
          quote = quote.strip('"')
          quote_dict[name].append([date, quote])
      else:
        log.debug("Discarding w/ wrong # tokens: %s", vals)
    # build data
    people = []
    for person, data in quote_dict.items():
      quotes = []
      for qnum, quote_pair in enumerate(data, 1):
        date, quote = quote_pair
        #print qnum, date, quote
        qid = str(person+ ":" + str(qnum))
        quotes.append(Quote(person, quote, qid));
      people.append(Person(person, quotes))
    return QuotesResource(people)

  @staticmethod
  def from_json(data):
    """ Create a resource from json data.
        Assumes title, author, chapters/text
    """
    people = []
    for snum, person in enumerate(data.get("people"), 1):
      #print person
      name = person.get("person")
      quotes = []
      for qnum, quote in enumerate(person.get("quotes"), 1):
        qid = str(name + QuotesResource.REF_DELIM + str(qnum))
        quotes.append(Quote(name, quote.get("quote"), qid));
      people.append(Person(name, quotes))
    return QuotesResource(people)

  def __init__(self, people):
    """ Stores only the top reference.
    """
    self.people = people

  def reference(self, str_ref):
    """ Parse this string reference as a person name, and return
        the object. First try to see if it's an exact reference,
        and if so split into name and ref number, else just assume 
        a full name.
    """
    if str_ref.find(QuotesResource.REF_DELIM) != -1:
      name, num = str_ref.split(':') 
    else: 
      name = str_ref
      num = None
    lower_name = name.lower()
    for person in self.people:
      if person.name.lower() == lower_name:
        if num == None:
          return person
        else:
          try:
            ref = person.children()[int(num)-1]
            return ref
          except Exception as e:
            print e
            raise InvalidReferenceError
    return None

  def top_reference(self):
    return self
  
  def children(self):
    return self.people

  def pretty(self):
    return "Quotes"

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern):
    hits = []
    for q in self.people:
      hits.extend(q.search(pattern))
    return hits


#class ReferenceImpl(Reference):
#  """ Represents some section of text.
#  """
#  def __init__(self, resource):
#    self._resource = resource
#
#  def ref_prefix(self):
#    try:
#      return self._resource.top_reference().title
#    except Exception:
#      return "Chapter"


class Person(Reference):
  """ A single person's quotes.
  """
  def __init__(self, name, quotes):
    self.name = name
    self.quotes = quotes

  def children(self):
    return self.quotes

  def pretty(self):
    return self.name

  def text(self):
    """ Too much text. """
    raise NotImplementedError()

  def search(self, pattern):
    hits = []
    for q in self.quotes:
      hits.extend(q.search(pattern))
    return hits

class Quote(Reference):
  """ A single quote.
  """
  def __init__(self, speaker, quote, qid):
    self.speaker = speaker
    self.quote = quote
    self.qid = qid

  def children(self):
    return None

  def pretty(self):
    return self.qid

  def text(self):
    """ The quote. """
    return self.quote

  def search(self, pattern):
    if re.search(pattern, self.quote):
      return [self]
    return []

