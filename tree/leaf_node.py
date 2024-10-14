#!python3

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
    def __init__(self, order, value, key, next=None):
        self.length = 2 * order
        self.data = { value: [key] }
        self.values = self.data.keys
        self.next = next

    def add_value(self, value, key):
        if len(self.values) == self.length:
            return False
        elif self.data[value]:
            self.data[value].append(key)
        else:
            self.data[value] = [key]
        return True
