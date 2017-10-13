#!/usr/bin/env python
"""
Interactive interface for querying textbites resources.

usage: interactive.py [resource name]*

"""
import readline
import sys
import re

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
  # prefer single lines to block
  one_per_line = False

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

  def format_lines(ref):
    def ref_str(v):
      return "{}:{}".format(v.parent().short(), v.short())
    v_format = "{ref} {text}"
    lines = ref.children() or [ref]
    text="\n".join([v_format.format(ref=ref_str(v), text=v.text())
      for v in lines])
    return text

  def format_block(ref):
    # show reference per line if there are > 10
    v_format = ("{text}" if not ref.children() or len(ref.children()) < 10 
                           else "{ref} {text}")
    lines = ref.children() or [ref]
    text = " ".join([v_format.format(ref=v.short(), text=v.text())
        for v in lines])
    ref_str = " ({ref} {res})".format(ref=ref.pretty(), res=cur_resname())
    return text + ref_str

  def display_one_ref(ref):
    try:
      ref.text()
      # verse, multiple verses or one chapter
      print format_lines(ref) if one_per_line else format_block(ref)
    except Exception as e:
      print e
      # book or chapters
      print "Setting context to:", ref.pretty()
      del context[1:]
      context[0] = ref

  def tokenize_query(rawquery):
    def clean(q):
      return q.strip().replace('.', ':')
    # Split on ; or ,
    # Split on comma only if followed by book ref
    return [clean(q) for q in re.split(",|;", rawquery)]

  # REPL Loop.
  while True:
    print "---"
    raw_query = raw_input("> ")
    for query in tokenize_query(raw_query):
      if query in resources:
        cur_resource = resources.get(query)
        print "Setting resource to:", cur_resname()
        context = [cur_resource.top_reference()]
      elif query in BOOK_GROUPS:
        context = [cur_resource.reference(b) for b in BOOK_GROUPS.get(query)]
        print "Setting resource to:", context_str()
      elif query in ('help', '?'):
        print "Valid input: <resource|refernce|book or group to scope|search> or format <lines|block>"
      elif query.startswith("format"):
        if query == "format lines":
          one_per_line = True
        elif query == "format block":
          one_per_line = False
        else:
          print "Say 'format lines' or 'format block'"
      elif len(query.strip()):
        try:
          ref = cur_resource.reference(query)
          display_one_ref(ref)
          print
        except Exception as e:
          print e
          search(raw_query)

if __name__ == "__main__":
  main(sys.argv)


