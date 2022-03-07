import random

from collections import deque

class TreeNode:
    def __init__(self, content, children):
        self.content = content
        self.children = children
    def print_tree(self):
        for child in self.children:
            print "{} -> {}".format(self.content, child.content)
            child.print_tree()
def tree_traversal(graph, root = None):
    """
    Graph as dict, root as key in graph or None.
    If no root selected, will select random root.
    graph[a] -> neighbours of a
    """
    if not root:
        root = random.choice(graph.keys())
    root_node = TreeNode(root, [])
    frontier = deque([root_node])
    explored = set([root])
    while frontier:
        exploring = frontier.pop()
        neighbours = graph[exploring.content]
        for n in filter(lambda x: x not in explored, neighbours):
            child = TreeNode(n, [])
            frontier.appendleft(child)
            exploring.children.append(child)
            explored.add(n)
    return root_node

def test_tree_traversal():
    graph = {
                1 : [2, 3],
                2 : [3, 4],
                3 : [],
                4 : [],
            }
    tree_traversal(graph, root = 1).print_tree()
    
if __name__ == '__main__':
    test_tree_traversal()
