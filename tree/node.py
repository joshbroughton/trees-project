#!python3

class Node:
    def __init__(self, order, value):
        self.length = order * 2
        self.values = [value]
        self.children = []

    def get_child(self, target_value):
        index = 0

        for value in self.values:
            if target_value <= value:
                return self.children[index]
        return self.children[-1]

    def add_child(self, leaf_node):
        if len(self.values) == self.length:
            return False
        else:
            self.children.append(leaf_node)

