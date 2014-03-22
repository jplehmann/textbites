#!/usr/bin/env python
"""
Interactive interface for querying textbites resources.

usage: interactive.py [resource name]*

"""
import readline
import sys

from textbites import library
try:
  from pybible.data import BOOK_GROUPS
except ImportError:
  BOOK_GROUPS = {}


def setup_readline():
  """ Load readline history.
  """
  import os
  histfile = os.path.join(os.path.expanduser("~"), ".pyhist")
  try:
      readline.read_history_file(histfile)
  except IOError:
      pass
  import atexit
  atexit.register(readline.write_history_file, histfile)
  del os, histfile

def load_library(resources):
  """ Load textual resources given by command-line args 
  else all default.
  """
  if len(resources) > 0:
    import os
    for arg in resources:
      f = os.path.realpath(
        os.path.join(os.path.dirname(library.__file__), 
          "data/{}.bible.json".format(arg.upper())))
      library.load(f)
  else:
    # load everything we find
    library.load_resources()
  print "Loading into library:", library.list()
  # map to lowercase resource names
  return dict([(k.lower(),library.get(k)) for k in library.list()])

def main(args):
  def cur_resname():
    return cur_resource.top_reference().pretty()

  setup_readline()
  resources = load_library(args[1:])
  # default is first resource loaded
  cur_resource = resources.values()[0]
  print "Setting resource to:", cur_resname()
  # for searching
  context = [cur_resource.top_reference()]

  def context_str():
    return [str(c.pretty()) for c in context]

  def search_context(query, context):
    """ Search case in-sensitive if all lower and all alpha chars, 
    else no special flags are applied (case-sensitive).
    """
    if query.isalpha() and query.islower():
      return context.search("(?i)" + query)
    else:
      return context.search(query)

  def search(query):
    print "Searching context {} with query...\n".format(context_str())
    results = [r for c in context for r in search_context(query, c)]
    for ref in results:
      print "{text} ({ref} {res})".format(
        text=ref.text(), 
        ref=ref.pretty(),
        res=cur_resname()
      )
      print
    print "Displayed", len(results), "results."

  def display_one_ref(ref):
    try:
      text = ref.text()
    except:
      text = None
    # verse(s)/line(s)
    if text and not ref.children():
      print "{text} ({ref} {res})".format(
        text=ref.text(), 
        ref=ref.pretty(),
        res=cur_resname()
      )
    # multiple verses or one chapter
    elif text and ref.children():
      v_format = "{text}" if len(ref.children()) < 10 else "{num} {text}"
      print "{text} ({ref} {res})".format(
        text=" ".join([v_format.format(num=v.short(), text=v.text()) 
                                           for v in ref.children()]),
        ref=ref.pretty(),
        res=cur_resname()
      )
    # book or chapters
    elif not text:
      print "Setting context to:", ref.pretty()
      del context[1:]
      context[0] = ref
    else:
      # search terms
      print "Not sure what this is", ref

  # REPL Loop.
  while True:
    print "---"
    query = raw_input("> ")
    if query in resources:
      cur_resource = resources.get(query)
      print "Setting resource to:", cur_resname()
      context = [cur_resource.top_reference()]
    elif query in BOOK_GROUPS:
      context = [cur_resource.reference(b) for b in BOOK_GROUPS.get(query)]
      print "Setting resource to:", context_str()
    elif len(query.strip()):
      try:
        ref = cur_resource.reference(query)
        display_one_ref(ref)
      except:
        search(query)

if __name__ == "__main__":
  main(sys.argv)


