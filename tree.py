"""A tree with operator nodes and numeric value leaves."""

from __future__ import print_function

import re

OP_NAMES = ('+', '-', '*', '/')
RE_OPS = re.compile('^[\+\-\*\/]$')
RE_NUM = re.compile('^\d+$')


class TreeError(Exception):
  """The super class for tree errors."""


class OperatorNameError(TreeError):
  """Returned if an operator is given a bad name."""


class NumValueError(TreeError):
  """Raised if the Num object value is not a valid number."""


class NotNumError(TreeError):
  """Raised if the object doesn't have a numeric value."""


class NotAnOp(TreeError):
  """This node is not an operator."""


class Op(object):
  """An arithmetic operator."""

  def __init__(self, name):
    """Initialize the name and operator type."""

    if name not in OP_NAMES:
      raise OperatorNameError('Name {0} not an op name.'.format(name))

    self.name = name
    self.type = 'op'

  def op(self, val_a, val_b):
    """Operate on the two numbers."""

    num_a = int(val_a)
    num_b = int(val_b)

    if self.name == '+':
      return num_a + num_b
    elif self.name == '-':
      return num_a - num_b
    elif self.name == '*':
      return num_a * num_b
    elif self.name == '/':
      return num_a / num_b
    else:
      raise OperatorNameError('Name not found {0}.'.format(self.name))

  def __repr__(self):
    """Represent the object."""

    return self.name


class Num(object):
  """A number."""

  def __init__(self, val):
    """Save a value and set the type."""

    self.type = 'num'

    try:
      self.val = int(val)
    except ValueError:
      raise NumValueError('Value {0} is not a valid number.'.format(val))

  def __repr__(self):
    """Return the str representation of this object."""

    return str(self.val)


class Node(object):
  """A node that can be an operator or a numeric value."""

  def __init__(self, obj):
    """Save the object for this node."""

    self.obj = obj
    self.left = None
    self.right = None

  def type(self):
    """Return the type of the object."""

    return self.obj.type

  def val(self):
    """Return the value of the object."""

    if self.obj.type == 'num':
      return self.obj.val
    else:
      raise NotNumError('Not a number {0}.'.format(self.obj))

  def op(self, val_a, val_b):
    """Operate on the two numbers."""

    return self.obj.op(val_a, val_b)

  def __repr__(self):
    """Return a str repr based on the object type."""

    return repr(self.obj)


class Tree(object):
  """A tree of nodes with an operator and left and right sides.

  The left and right can be Nums or each another Tree.
  """

  def __init__(self):
    """Initialize the root which is usually filled in later."""

    self.root = None

  def _get_val(self, value):
    """Turn a value into a Num Node if needed."""

    if isinstance(value, Node):
      return value
    else:
      return Node(Num(value))

  def make_branch(self, op_name, left_val, right_val):
    """Make a branch which is an op node with left and right values."""

    node = Node(Op(op_name))
    node.left = self._get_val(left_val)
    node.right = self._get_val(right_val)

    return node

  def _eval_node(self, node):
    """Recursively walk the tree from a node, evaluating each op.

    We assume that the given node has an op with a left and right.
    """

    if node.type() != 'op':
      raise NotAnOp('This node {0} is not an operator.'.format(node))

    if node.left.type() == 'op':
      left_val = self._eval_node(node.left)
    else:
      left_val = node.left.val()

    if node.right.type() == 'op':
      right_val = self._eval_node(node.right)
    else:
      right_val = node.right.val()

    return node.op(left_val, right_val)

  def eval(self):
    """Evaluate the tree starting at root."""

    return self._eval_node(self.root)

  def parse(self, input_str):
    """Parse and the input_str and populate the tree.

    After this the tree is ready to eval.

    Args:
      input_str: str. A str containing an RPN expression, e.g.,
        '2 3 + 4 5 + *'.
    """

    parser = Parser()
    parser.parse(input_str)
    self.root = parser.stack[0]

  def _rpn_str(self, node, template):
    """Build a str in RPN notation from the tree."""

    if node.type() != 'op':
      raise NotAnOp('This node {0} is not an operator.'.format(node))

    if node.left.type() == 'op':
      left_str = self._rpn_str(node.left, template)
    else:
      left_str = repr(node.left)

    if node.right.type() == 'op':
      right_str = self._rpn_str(node.right, template)
    else:
      right_str = repr(node.right)

    return template.format(left_str, right_str, repr(node))

  def rpn_str(self):
    return self._rpn_str(self.root, '{0} {1} {2}')

  def infix_str(self):
    return self._rpn_str(self.root, '({0} {2} {1})')

  def __repr__(self):
    return self.rpn_str()


class Parser(object):
  """Parse a str in RPN to make a tree."""

  def __init__(self):
    """Initialize the stack."""

    self.stack = []
    self.input = []

  def split_input(self, input_str):
    """Split the input str.

    Args:
      input_str: str. A str containing an RPN expression, e.g.,
        '2 3 + 4 5 + *'.
    """

    self.input = input_str.split()

  def tokenize(self):
    """Tokenize the next value and place on stack.

    Returns:
      A str indicating the type of token found, 'op' or 'num'.
    """

    item = self.input.pop(0)
    if RE_OPS.search(item):
      self.stack.append(Node(Op(item)))
      return 'op'
    elif RE_NUM.search(item):
      self.stack.append(Node(Num(item)))
      return 'num'

  def interpret(self):
    """Interpret the bottom elements on the stack.

    If the bottom node is an op, create a branch with the op and two
    preceeding nodes on the stack as it's left and right.
    """

    if self.stack[-1].type() != 'op':
      template = 'The bottom item on the stack is not an operator {0}'
      raise NotAnOp(template.format(self.stack[-1]))

    op_node = self.stack.pop()
    right = self.stack.pop()
    if right.type() == 'op' and len(self.stack) > 1:
      self.stack.append(right)
      self.interpret()
      right = self.stack.pop()
    op_node.right = right

    left = self.stack.pop()
    if left.type() == 'op' and len(self.stack) > 1:
      self.stack.append(left)
      self.interpret()
      left = self.stack.pop()
    op_node.left = left

    self.stack.append(op_node)

  def parse(self, input_str):
    """Parse the input_str and leave a full tree on the stack.

    One Node object is left on the internal stack which is the root of the
    entire tree.

    Args:
      input_str: str. A str containing an RPN expression, e.g.,
        '2 3 + 4 5 + *'.
    """

    self.split_input(input_str)

    while self.input:
      self.tokenize()

    self.interpret()
