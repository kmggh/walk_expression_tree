#!/usr/bin/env python

"""Try the parser to parse and eval an RPN expression."""

from __future__ import print_function

import tree
import argparse


def get_args():
  """Process the command line args.

  Returns:
    An args object with options as attributes.
  """

  parser = argparse.ArgumentParser()
  parser.add_argument('--expr',  
                      help='The expression to evaluate.')
  return parser.parse_args()


def main():
  options = get_args()
  my_tree = tree.Tree()

  my_tree.parse(options.expr)

  print(my_tree)
  print('= {0}'.format(my_tree.eval()))


if __name__ == '__main__':
  main()
