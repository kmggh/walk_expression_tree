Walk Operator Tree
==================

Ken Guyton<br />
Wed 2015-09-02

Walk a tree of (arithmetic) operators and values and process them.
Each node is an operator and each leaf node is a numeric value.

Brian presented this basic problem to me as a possible interview
question and I was inspired to write a developed version.


To Run
------


    ./try_parser.py --expr '2 3 + 4 5 + *'


To Test
-------

    ./test_tree
    

Parsing Rules
-------------

For RPN input, e.g.,   

    2 3 + 4 5 + *

It should go something like this.

1. Num -> save num
3. Op -> make branch with two previous, replace them with branch


Bugs
----

The data store in the parser shouldn't be called a "stack."
