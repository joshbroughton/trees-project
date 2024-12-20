#!python3

from tree.leaf_node import LeafNode

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
        node = self.root
        while node is not None:
            result += str(node) + ' -> '
            node = node.next

        return result

    def to_json(self):
        '''
        Build a json representation of the tree using a breadth first traversal. The output format is:
        {
            "0": [root_values],
            "1": [[second_level_values]],
            "2": [[third_level_values]],
            ...
            "n": [[leaf_values]]
            }
        '''
        result = {
            '0': [[self.root.values()]]
        }
        nodes = [self.root]
        level = 1
        while not isinstance(nodes[0], LeafNode):
            level_values = []
            next_nodes = []
            for node in nodes:
                node_values = []
                for child in node.children:
                    if isinstance(child, LeafNode):
                        node_values.append(child.values())
                        next_nodes.append(child)
                    else:
                        node_values.append(child.values())
                        next_nodes.append(child)
                level_values.append(node_values)
            result[str(level)] = level_values
            level += 1
            nodes = next_nodes

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

    def insert_many(self, values, keys=None):
        '''
        Insert multiple values into the tree
        '''
        if keys is None:
            keys = values
        for index, value in enumerate(values):
            self.insert(value, keys[index])

    def delete(self, value):
        '''
        Deletes the record with the given key from the tree. If deleting that key from the leaf
        node that contains it makes that node violate the tree rules, rebalance the tree starting from
        that node as needed
        '''
        search_result = self._search_value(value, self.root)
        if search_result is not None:
            search_result.delete_value(value)
            return True
        else:
            return None

    def search(self, value):
        '''
        Returns the record for the given key
        Like doing SELECT * FROM table WHERE key=key
        '''
        search_result = self._search_value(value, self.root)
        if search_result is not None:
            return search_result.data[value]
        else:
            return None

    def search_range(self, start_value, end_value):
        '''
        Search for and return all records within a given key range (include)
        Like doing SELECT * FROM table WHERE key BETWEEN start_key AND end_key
        '''
        search_result = self._search_value(start_value, self.root)
        results = []
        for value in search_result.data.keys():
            if value >= start_value:
                results.extend(search_result.data[value])
        search_result = search_result.next

        while search_result is not None:
            if end_value in search_result.data:
                for value in search_result.data.keys():
                    if value <= end_value:
                        results.extend(search_result.data[value])
                break
            else:
                results.extend(*search_result.data.values())
            search_result = search_result.next
        return results

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









