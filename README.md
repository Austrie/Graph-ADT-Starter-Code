# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

A BFS in a graph can end up in an infinite cycle. In order to prevent this, BFS in a graph need to keep track and prevent duplication of it's previously explored nodes. 

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

BFS can be used to explore files on an OS. Most newer operating systems allow "fake" links/nodes in its file system, which fundamentally changes a file system from tree-based to graph-based, since a node can have reference back to its self or it's children can link back to its self: essentially removing the idea of hierarchy.


# Homework 2: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. Compare and contrast Breadth-first Search and Depth-first Search by providing one similarity and one difference.
A: Both will allow you to traverse through a graph to find a goal. DFS optimizes under the assumption that the node being sought is going to be in then deepest path of the immediate child. However, BFS optimizes searching under the impression that the node being sought is near the starting point.

2. Explain why a Depth-first Search traversal does not necessarily find the shortest path between two vertices. What is one such example of a graph where a DFS search would not find the shortest path?
A: DFS search often folishly digs too deep into a singular path, before checking any other possible paths from the starting node. If one is trying to find the shortest path to point, one should use an algorithm (e.g. BFS) that optimizes to find the closest grandchild to the starting node, even if that means checking all paths without necessarily getting to deep any one path. If a starting has 5 possible starting paths (i.e. 5 children nodes), each of the first 3 paths are 20 nodes deep, the second child in the fourth path is the node we're searching for, then DFS won't find the node we're searching until 62 nodes later ((3 paths x 20 nodes) + 2 (two nodes in the fourth path)). BFS would've found the solution after around 9 nodes (the first child of each path, then second node of each path except the fifth path).

3. Explain why we cannot perform a topological sort on a graph containing a cycle.
A: You can not perform topological sort on a graph containing a cycle, because you can not determine which node should be done/ordered first, due a node(s) both being the (in)direct parent and child of another node: it's illogical from a hierarchy viewpoint.