#!python3

from node import Node

class BPlusTree:
    '''
    An implementation of a B+ tree meant to demonstrate how B-plus trees
    are used to implement database indexes. Allows the creation of a B-plus
    tree of any order. Supports Inserts, Deletions, and Searches.

    Definitions of B+ trees vary, for this one: Root and internal nodes
    contain keys for the index, and pointers to child nodes. Each leaf node contains a pointer
    to a record that store the actual data. The leaf nodes are singly linked to eachother for range
    searches.
    '''
    def __init__(self, order, root_key):
        self.root = Node.new(order, root_key)
        self.order = order

    def insert(self, key):
        '''
        Insert a new index key into the tree. Searches for a space in an existing
        node, else shifts keys into siblings, else if both siblings are full creates
        a new internal node
        '''

    def delete(self, key):
        '''
        Deletes the record with the given key from the tree. If deleting that key from the leaf
        node that contains it makes that node violate the tree rules, rebalance the tree starting from
        that node as needed
        '''

    def search(self, key):
        '''
        Search for a record with the given key and return it, else return null.
        Returns the data stored in the leaf node
        Like doing SELECT * FROM table WHERE key=key
        '''

    def range_search(self, start_key, end_key):
        '''
        Search for and return all records within a given key range (include)
        Like doing SELECT * FROM table WHERE key BETWEEN start_key AND end_key
        '''


