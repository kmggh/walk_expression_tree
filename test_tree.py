#!/usr/bin/env python

"""Walk a tree of arithmetic operator nodes and numeric values leaves.

Evaluate all of the expressions.
"""

from __future__ import print_function

import unittest
import tree


class TestOp(unittest.TestCase):
  def setUp(self):
    self.adder = tree.Op('+')
    self.subber = tree.Op('-')
    self.prodder = tree.Op('*')
    self.divver = tree.Op('/')

  def test_create(self):
    self.assertNotEqual(self.adder, None)

  def test_types(self):
    self.assertEqual(self.adder.type, 'op')
    self.assertEqual(self.subber.type, 'op')
    self.assertEqual(self.prodder.type, 'op')
    self.assertEqual(self.divver.type, 'op')

  def test_add(self):
    self.assertEqual(self.adder.op(3, 5), 8)

  def test_sub(self):
    self.assertEqual(self.subber.op(5, 2), 3)

  def test_mul(self):
    self.assertEqual(self.prodder.op(5, 2), 10)

  def test_div(self):
    self.assertEqual(self.divver.op(6, 2), 3)

  def test_bogus(self):
    self.assertRaises(tree.OperatorNameError, tree.Op, 'bogus')

  def test_repr(self):
    self.assertEqual(repr(self.adder), '+')
    self.assertEqual(repr(self.subber), '-')
    self.assertEqual(repr(self.prodder), '*')
    self.assertEqual(repr(self.divver), '/')


class TestNum(unittest.TestCase):
  def setUp(self):
    self.num3 = tree.Num(3)
    self.num4 = tree.Num(4)

  def test_create(self):
    self.assertNotEqual(self.num3, None)

  def test_type(self):
    self.assertEqual(self.num3.type, 'num')
    self.assertEqual(self.num4.type, 'num')

  def test_val(self):
    self.assertEqual(self.num3.val, 3)
    self.assertEqual(self.num4.val, 4)

  def test_bogus_val(self):
    self.assertRaises(tree.NumValueError, tree.Num, 'bogus')

  def test_repr(self):
    self.assertEqual(repr(self.num3), '3')
    self.assertEqual(repr(self.num4), '4')


class TestNode(unittest.TestCase):
  def setUp(self):
    self.root = tree.Node(tree.Op('+'))
    self.left = tree.Node(tree.Num('3'))
    self.right = tree.Node(tree.Num('5'))

  def test_create(self):
    self.assertNotEqual(self.root, None)

  def test_create_values(self):
    self.assertEqual(self.root.obj.type, 'op')
    self.assertEqual(self.root.left, None)
    self.assertEqual(self.root.right, None)

  def test_types(self):
    self.assertEqual(self.root.type(), 'op')
    self.assertEqual(self.left.type(), 'num')
    self.assertEqual(self.right.type(), 'num')

  def test_repr(self):
    self.assertEqual(repr(self.root), '+')
    self.assertEqual(repr(self.left), '3')
    self.assertEqual(repr(self.right), '5')

  def test_num_val(self):
    self.assertEqual(self.left.val(), 3)
    self.assertEqual(self.right.val(), 5)

  def test_bogus_val(self):
    self.assertRaises(tree.NotNumError, self.root.val)

  def test_children(self):
    self.root.left = self.left
    self.root.right = self.right

    self.assertEqual(self.root.left.val(), 3)
    self.assertEqual(self.root.right.val(), 5)


class TestTree(unittest.TestCase):
  def setUp(self):
    self.tree = tree.Tree()

  def test_create(self):
    self.assertNotEqual(self.tree, None)
    self.assertEqual(self.tree.root, None)

  def test_make_branch(self):
    branch = self.tree.make_branch('+', 5, 3)

    self.assertEqual(branch.type(), 'op')
    self.assertEqual(branch.obj.name, '+')

    self.assertEqual(branch.left.type(), 'num')
    self.assertEqual(branch.left.val(), 5)

    self.assertEqual(branch.right.type(), 'num')
    self.assertEqual(branch.right.val(), 3)

  def test_make_branches(self):
    branch_right = self.tree.make_branch('+', 5, 3)
    branch = self.tree.make_branch('+', 2, branch_right)

    self.assertEqual(branch.type(), 'op')
    self.assertEqual(branch.obj.name, '+')
    self.assertEqual(branch.left.type(), 'num')
    self.assertEqual(branch.left.val(), 2)

    self.assertEqual(branch.right.type(), 'op')
    self.assertEqual(branch.right.obj.name, '+')
    self.assertEqual(branch.right.left.type(), 'num')
    self.assertEqual(branch.right.left.val(), 5)
    self.assertEqual(branch.right.right.type(), 'num')
    self.assertEqual(branch.right.right.val(), 3)

  def test_eval_1_branch(self):
    self.tree.root = self.tree.make_branch('+', 5, 3)
    self.assertEqual(self.tree.eval(), 8)

  def test_eval_2_branches(self):
    right = self.tree.make_branch('+', 5, 3)
    self.tree.root = self.tree.make_branch('+', 2, right)
    self.assertEqual(self.tree.eval(), 10)

  def test_eval_3_branches(self):
    left = self.tree.make_branch('+', 2, 3)
    right = self.tree.make_branch('+', 4, 5)
    self.tree.root = self.tree.make_branch('*', left, right)
    self.assertEqual(self.tree.eval(), 45)

  def test_rpn_str_1_branch(self):
    self.tree.root = self.tree.make_branch('+', 2, 3)

    self.assertEqual(self.tree.rpn_str(), '2 3 +')

  def test_rpn_str(self):
    left = self.tree.make_branch('+', 2, 3)
    right = self.tree.make_branch('+', 4, 5)
    self.tree.root = self.tree.make_branch('*', left, right)

    self.assertEqual(self.tree.rpn_str(), '2 3 + 4 5 + *')

  def test_infix_str(self):
    left = self.tree.make_branch('+', 2, 3)
    right = self.tree.make_branch('+', 4, 5)
    self.tree.root = self.tree.make_branch('*', left, right)

    self.assertEqual(self.tree.infix_str(), '((2 + 3) * (4 + 5))')

  def test_parse(self):
    self.tree.parse('2 3 + 4 5 + *')
    self.assertEqual(str(self.tree), '2 3 + 4 5 + *')
    self.assertEqual(self.tree.eval(), 45)


class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = tree.Parser()

  def test_create(self):
    self.assertNotEqual(self.parser, None)

  def test_init_val(self):
    self.assertEqual(self.parser.stack, [])
    self.assertEqual(self.parser.input, [])

  def test_split_input(self):
    self.parser.split_input('2 3 +')
    self.assertEqual(self.parser.input, ['2', '3', '+'])

  def test_tokenize(self):
    self.parser.split_input('2 3 +')

    self.assertEqual(self.parser.tokenize(), 'num')

    self.assertEqual(self.parser.input, ['3', '+'])
    self.assertEqual(self.parser.stack[0].type(), 'num')
    self.assertEqual(self.parser.stack[0].val(), 2)

  def test_tokenize2(self):
    self.parser.split_input('2 3 +')

    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'num')

    self.assertEqual(self.parser.input, ['+'])
    self.assertEqual(self.parser.stack[0].type(), 'num')
    self.assertEqual(self.parser.stack[1].type(), 'num')
    self.assertEqual(self.parser.stack[0].val(), 2)
    self.assertEqual(self.parser.stack[1].val(), 3)

  def test_tokenize3(self):
    self.parser.split_input('2 3 +')

    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'op')
    self.assertEqual(self.parser.input, [])
    self.assertEqual(self.parser.stack[2].type(), 'op')

  def test_interpret(self):
    self.parser.split_input('2 3 +')

    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'op')

    self.parser.interpret()
    self.assertEqual(len(self.parser.stack), 1)
    self.assertEqual(self.parser.stack[0].type(), 'op')
    self.assertEqual(self.parser.stack[0].left.val(), 2)    
    self.assertEqual(self.parser.stack[0].right.val(), 3)    

  def test_interpret2(self):
    self.parser.split_input('2 3 4 + +')

    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'op')
    self.assertEqual(self.parser.tokenize(), 'op')

    self.parser.interpret()
    self.assertEqual(len(self.parser.stack), 1)
    self.assertEqual(self.parser.stack[0].type(), 'op')

    this_tree = tree.Tree()
    this_tree.root = self.parser.stack[0]
    self.assertEqual(str(this_tree), '2 3 4 + +')
    self.assertEqual(this_tree.eval(), 9)

  def test_interpret3(self):
    self.parser.split_input('2 3 + 4 5 + *')

    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'op')
    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'num')
    self.assertEqual(self.parser.tokenize(), 'op')
    self.assertEqual(self.parser.tokenize(), 'op')

    self.parser.interpret()
    self.assertEqual(len(self.parser.stack), 1)
    self.assertEqual(self.parser.stack[0].type(), 'op')

    this_tree = tree.Tree()
    this_tree.root = self.parser.stack[0]
    self.assertEqual(str(this_tree), '2 3 + 4 5 + *')
    self.assertEqual(this_tree.eval(), 45)

  def test_parse(self):
    self.parser.parse('2 3 + 4 5 + *')

    self.assertEqual(len(self.parser.stack), 1)
    self.assertEqual(self.parser.stack[0].type(), 'op')

    this_tree = tree.Tree()
    this_tree.root = self.parser.stack[0]
    self.assertEqual(str(this_tree), '2 3 + 4 5 + *')
    self.assertEqual(this_tree.eval(), 45)


if __name__ == '__main__':
  unittest.main()
