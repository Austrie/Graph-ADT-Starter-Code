# Homework 1: Graph ADT & Traversals

Follow the instructions [here](https://make-school-courses.github.io/CS-2.2-Graphs-Recursion/#/Assignments/01-Graph-ADT) to complete this assignment.

## Discussion Questions

1. How is Breadth-first Search different in graphs than in trees? Describe the differences in your own words.

A BFS in a graph can end up in an infinite cycle. In order to prevent this, BFS in a graph need to keep track and prevent duplication of it's previously explored nodes. 

2. What is one application of Breadth-first Search (besides social networks)? Describe how BFS is used for that application. If you need some ideas, check out [this article](https://www.geeksforgeeks.org/applications-of-breadth-first-traversal/?ref=rp).

BFS can be used to explore files on an OS. Most newer operating systems allow "fake" links/nodes in its file system, which fundamentally changes a file system from tree-based to graph-based, since a node can have reference back to its self or it's children can link back to its self: essentially removing the idea of hierarchy.