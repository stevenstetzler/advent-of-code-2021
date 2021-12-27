import numpy as np
import io
import argparse

# We'll represent snailfish numbers as a Binary tree since
# they come in recursive pairs
class BinaryTree(object):
    def __init__(self, parent=None, left=None, right=None, data=None, level=0):
        self.parent = parent
        self.level = level

        if self.parent is not None and self.level == 0:
            self.level = self.parent.level + 1

        self.left = left
        if self.left is not None:
            self.left.parent = self
            self.left.increment_level()
        
        self.right = right
        if self.right is not None:
            self.right.parent = self
            self.right.increment_level()
        
        self.data = data

    def __format__(self, spec):
        if self.left is not None and self.right is not None:
            return f"[{self.left},{self.right}]"
        elif self.left is not None:
            return f"[{self.left},_]"
        elif self.right is not None:
            return f"[_,{self.right}]"
        elif self.data is not None:
            return f"{self.data}"
        else:
            return f"BinaryTree(level={self.level})"

    def __repr__(self):
        return f"{self}"

    def copy(self):
        left = self.left        
        if left:
            left = left.copy()
        right = self.right        
        if right:
            right = right.copy()

        # parent and level will be set automatically
        b = BinaryTree(
            left=left,
            right=right,
            data=self.data
        )
        return b

    def increment_level(self):
        self.level += 1
        if self.left:
            self.left.increment_level()
        if self.right:
            self.right.increment_level()
        
    def decrement_level(self):
        self.level -= 1
        if self.left:
            self.left.decrement_level()
        if self.right:
            self.right.decrement_level()

def get_nodes(n):
    nodes = []
    if n.left and n.right:
        nodes += get_nodes(n.left) + get_nodes(n.right)
    elif n.left:
        nodes += get_nodes(n.left)
    elif n.right:
        nodes += get_nodes(n.right)
    else:
        nodes = [n]
    return nodes

def find_left(node):
    # reached root without finding a left
    if node.parent is None:
        return None
    if node.parent.left is node:
        # this node is the left of the parent
        # so we should find the node that is left of the parent
        return find_left(node.parent)
    else:
        # this node is the right of the parent, so there is a left
        # and we should find its right-most node
        n = node.parent.left
        while n.right:
            n = n.right
        return n

def find_right(node):
    # reached root without finding a right
    if node.parent is None:
        return None
    if node.parent.right is node:
        # this node is the right of the parent
        # so we should find the node that is right of the parent
        return find_right(node.parent)
    else:
        # this node is the left of the parent, so there is a right
        # and we should find its left-most node
        n = node.parent.right
        while n.left:
            n = n.left
        return n

def add(n1, n2):
    n = BinaryTree()
    n.left = n1
    n.right = n2
    n1.parent = n
    n2.parent = n
    n1.increment_level()
    n2.increment_level()
    return n

def explode(pair):
    left = find_left(pair.left)
    right = find_right(pair.right)
    if left:
        left.data += pair.left.data
    if right:
        right.data += pair.right.data
    
    pair.left = None
    pair.right = None
    pair.data = 0

def split(node):
    data = node.data
    node.left = BinaryTree(data=int(data/2), parent=node)
    if int(data/2) != data/2:
        node.right = BinaryTree(data=int(data/2) + 1, parent=node)
    else:
        node.right = BinaryTree(data=int(data/2), parent=node)
    
    node.data = None

def parse_number(number):
    if type(number) is list:
        return BinaryTree(left=parse_number(number[0]), right=parse_number(number[1]))
    elif type(number) is int:
        return BinaryTree(data=number)

def reduce(number, verbose=False):
    nodes = get_nodes(number)
    # print(nodes)
    nodes_to_explode = []
    nodes_to_split = []
    for node in nodes:
        if node.level > 4:
            if node.parent not in nodes_to_explode:
                nodes_to_explode.append(node.parent)
        if node.data > 9:
            if node not in nodes_to_split:
                nodes_to_split.append(node)
    if len(nodes_to_explode) > 0:
        if verbose:
            print("exploding", nodes_to_explode[0], "in", number)
        explode(nodes_to_explode[0])
        return reduce(number, verbose=verbose)
    if len(nodes_to_split) > 0:
        if verbose:
            print("splitting", nodes_to_split[0], "in", number)
        split(nodes_to_split[0])
        return reduce(number, verbose=verbose)
    return number

def magnitude(number):
    mag = 0
    if number.left is not None:
        mag += 3 * magnitude(number.left) 
    if number.right is not None:
        mag += 2 * magnitude(number.right)
    if number.data:
        mag += number.data
    return mag

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    verbose = args.verbose

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    numbers = []
    for line in lines:
        numbers.append(parse_number(eval(line)))

    number = numbers[0]
    for i in range(1, len(numbers)):
        number = add(number, numbers[i])
        number = reduce(number, verbose=verbose)
    
    print("Final sum is", number)
    print("Magnitude of final sum is", magnitude(number))

if __name__ == "__main__":
    main()
