Execution instructions:
To compile: g++ 2019202007.cpp
To execute: ./a.out <input_file>

Format for input file:

Only one of these instructions per line

For insert : INSERT <value>
For find   : FIND <value>
For count  : COUNT <value>
For range  : RANGE <value1> <value2>

Implementation details:

1) Insertion: 
If the node has an empty space, insert the key into the node. 
If the node is already full, split it into two nodes, distributing the keys evenly between the two nodes.

2) Count:
Go to leaf node and traverse left to right until the value exceeds the given value

3) Range:
Go to leaf node search for lower bound and traverse till upper bound does not exceed

4) FIND:
Go to leaf node search for given value. If it exceeds search value and not found, return "NO"



