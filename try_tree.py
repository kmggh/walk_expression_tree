#!/usr/bin/env python

"""Try a tree."""

from __future__ import print_function

import tree


def main():
  my_tree = tree.Tree()

  left = my_tree.make_branch('+', 21, 34)
  right = my_tree.make_branch('+', 56, 78)
  my_tree.root = my_tree.make_branch('*', left, right)

  print(my_tree)
  print('= {0}'.format(my_tree.eval()))


if __name__ == '__main__':
  main()
