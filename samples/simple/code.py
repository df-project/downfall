#!/bin/python
# -*- encoding:utf-8 -*-

import sys
from math import pi

def test():
  a = 1
  print "This is just a test"
  return a + 5

def a_function(value):
  """
     This is a comment
  """
  v = value * pi
  return v

if __name__ == "__main__":
  print "We start the program here!"
  print "Value of PI : %f" % (pi,)
