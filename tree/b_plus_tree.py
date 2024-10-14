#!python3

from node import Node
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
    def __init__(self, order, root_key, root_value):
        self.root = LeafNode.new(order, root_key, root_value)
        self.data = { root_key: root_value }
        self.order = order

    def insert(self, value, key):
        '''
        Insert a new index key into the tree. Searches for a space in an existing
        node, else shifts keys into siblings, else if both siblings are full creates
        a new internal node
        '''
        # first insertion
        if type(self.root) is LeafNode:
            new_node = Node.new(self.order, value)
            self.root.add_value(value, key)
            new_node.add_child(self.root)
            self.root = new_node

        # if a leaf node with this value exists
        search_result = self._search_value(value, self.root)
        if search_result is not None:
            insert_result = search_result.add_value(value, key)
            # insert successful; value exists or node has room
            if insert_result is True:
                return True
            # not successful; we need to split the leaf node
            else





    def delete(self, key):
        '''
        Deletes the record with the given key from the tree. If deleting that key from the leaf
        node that contains it makes that node violate the tree rules, rebalance the tree starting from
        that node as needed
        '''

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

    def _search_value(self, value, node):
        '''
        Search for a leaf node where the given index value should be stored and return it, else return None.
        '''
        if type(node) is LeafNode:
            return node
        else:
            return self._search_value(node.get_child(value))







