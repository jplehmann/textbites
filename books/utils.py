#!/usr/bin/env python

def zero_indexed(val, none_val=None):
  """ Convert this 1-based index to a 0-based one,
      Also considering that None should not be modified.
  """
  return val-1 if val != None else none_val

def increment(val, none_val=None):
  return val+1 if val != None else none_val

def val_or_default(val, none_val=0):
  return val if val != None else none_val

def safe_int(val):
  return int(val) if val != None else val
