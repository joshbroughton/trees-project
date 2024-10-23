#!python3

from inner_node import InnerNode
from leaf_node import LeafNode

class BPlusTree:
    '''
    An implementation of a B+ tree meant to demonstrate how B-plus trees
    are used to implement database indexes. Allows the creation of a B-plus
    tree of any order. Supports Inserts, Deletions, and Searches.

    Definitions of B+ trees vary, for this one: Root and internal nodes
    contain the values for the index, and pointers to child nodes. Each leaf node contains a pointer
    to a record/records that store the actual data; they contain the column value that the index is on
    and a list of associated primary keys for the value. The leaf nodes are singly linked to eachother for range
    searches.
    '''
    def __init__(self, order, primary_key, root_value):
        self.root = LeafNode(order, {root_value: [primary_key]}, self)
        self.order = order
        self.start = self.root

    def __str__(self):
        '''
        Build a string representation of the tree using a breadth first traversal
        '''
        result = ''
        node = self.start
        while node is not None:
            result += str(node) + ' -> '
            node = node.next

        return result

    def insert(self, value, key):
        '''
        Insert a new index key into the tree. Searches for a space in an existing
        node, else shifts keys into siblings, else if both siblings are full creates
        a new internal node
        '''
        # find the node to insert the value into
        search_result = self._search_value(value, self.root)
        if search_result is not None:
            search_result.add_value(value, key)
        # update the root if it has changed
        if self.root.parent is not None:
            self.root = self.root.parent

    def delete(self, value, key):
        '''
        Deletes the record with the given key from the tree. If deleting that key from the leaf
        node that contains it makes that node violate the tree rules, rebalance the tree starting from
        that node as needed
        '''
        search_result = self._search_value(value, self.root)
        if search_result is not None:
            search_result.delete_value(value, key)

    def search(self, key):
        '''
        Returns the record for the given key
        Like doing SELECT * FROM table WHERE key=key
        '''

    def range_search(self, start_key, end_key):
        '''
        Search for and return all records within a given key range (include)
        Like doing SELECT * FROM table WHERE key BETWEEN start_key AND end_key
        '''

    def make_root(self, node):
        '''
        Makes node the root of the tree
        '''
        self.root = node

    def _search_value(self, value, node):
        '''
        Search for a leaf node where the given index value should be stored and return it
        '''
        if type(node) is LeafNode:
            return node
        else:
            return self._search_value(value, node.get_child(value))









