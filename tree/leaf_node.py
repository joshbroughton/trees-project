#!python3

from inner_node import InnerNode

class LeafNode:
    '''
    Leaf Node class. For efficiency of range queries, leaf nodes form a linked list.
    Database indexes generally want to optimize for search queries, so the increased
    cost to insertions/deletions of the linked list is worth it.
    In this implementation, leaf nodes hold pointers to the actual records; the pointer
    is a unique primary key for fetching records from a python dictionary. If the column
    that the index is on is not the primary key, internal nodes store the index value, and the leaf
    nodes store both the index value and all primary keys with that value to facilitate lookup of
    non-unique values
    '''
    def __init__(self, order, data, parent=None, next=None):
        self.length = 2 * order
        self.parent = parent
        self.data = data
        self.next = next
        self.order = order

    def values(self):
        return sorted(self.data.keys())

    def add_value(self, value, key, tree):
        if value in self.data:
            self.data[value].append(key)
        else:
            self.data[value] = [key]
        print(len(self.values()))
        if len(self.values()) > self.length:
            self.split_node(tree)

    def split_node(self, tree):
        '''
        Splits the node into two. Updates the current node in place, then adds a new node
        with half the values to the parent. The parent will handle splitting itself if needed.
        '''
        print('splitting leaf node')
        split_index = self.length // 2
        # there's enough going on here that I'm gonna let the built in handle this
        items = sorted(self.data.items())
        data1 = dict(items[:split_index])
        data2 = dict(items[split_index:])
        self.data = data1
        # new node points to parent and current node's next
        new_node = LeafNode(self.order, data2, self.parent, self.next)
        self.next = new_node
        if self.parent is None:
            print(self.values()[0])
            self.parent = InnerNode(self.order, self.values()[0])
            new_node.parent = self.parent
            self.parent.add_child(self)
            self.parent.add_child(new_node)
            tree.make_root(self.parent)
        else:
            self.parent.add_value(self.values()[0])
            self.parent.add_child(new_node)

