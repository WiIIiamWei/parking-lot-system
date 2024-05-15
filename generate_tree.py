# This file is only for report use. It is not part of the main project.
# Generate a tree structure from a Python file

import ast
from collections import deque

class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children is not None else []

def generate_tree(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        node = ast.parse(file.read())

    root = Node('root')
    queue = deque([(root, node.body)])

    while queue:
        parent, children = queue.popleft()
        for child in children:
            if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                new_node = Node(child.name)
                parent.children.append(new_node)
                if isinstance(child, ast.ClassDef):
                    queue.append((new_node, child.body))

    return root

def print_tree(node, prefix="", is_last=False, is_root=True):
    if not is_root:
        print(prefix, "└── " if is_last else "├── ", node.name, sep="")
    prefix += "    " if is_last else "│   "
    for i, child in enumerate(node.children):
        print_tree(child, prefix, i == len(node.children) - 1, is_root=False)

# Replace 'your_code.py' with the actual path to your Python file
root = generate_tree('main.py')
print_tree(root)
