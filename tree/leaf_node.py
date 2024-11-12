#!python3

from tree.inner_node import InnerNode

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
    def __init__(self, order, data, tree, parent=None, next=None):
        self.length = 2 * order
        self.parent = parent
        self.data = data
        self.next = next
        self.order = order
        self.tree = tree

    def __str__(self):
        return str(self.data)

    def values(self):
        return sorted(self.data.keys())

    def is_full(self):
        return len(self.values()) > self.length

    def can_transfer(self):
        return len(self.values()) > self.order

    def right_value(self):
        value = self.values()[-1]
        return (value, self.data[value])

    def left_value(self):
        value = self.values()[0]
        return (value, self.data[value])

    def add_leaf_entry(self, value, keys):
        '''
        Add a new dict entry with all the primary keys for the value
        '''
        self.data[value] = keys

    def delete_leaf_entry(self, value):
        '''
        Delete the entire dict entry for the value
        '''
        del self.data[value]

    def merge_node(self, node):
        '''
        Merge the data from the given node into this node
        '''
        for key, value in node.data.items():
            if key in self.data:
                self.data[key].extend(value)
            else:
                self.data[key] = value

    def add_value(self, value, key):
        '''
        Add a new value to this leaf node. If the node is over-full after, split it into two nodes
        '''
        if value in self.data:
            self.data[value].append(key)
        else:
            self.data[value] = [key]
        if self.is_full():
            self.split_node()

    def delete_value(self, value):
        '''
        Delete a value from the leaf node.
        Cases:
        1. Basic case - we delete the value from the leaf, and the node still has enough values
        2. Underflow #1 - after deleting the node has too few values, but a sibling transfer rebalances
        3. Underflow #2 - after deleting the node has too few values, and a leaf node merge is needed
        4. Underflow #3 - after a leaf merge, the tree still isn't balanced and an inner node transfer is needed
        5. Underflow #4 - after a leaf merge, the tree still isn't balanced and an inner node merge is needed
        Using https://www.cs.emory.edu/~cheung/Courses/554/Syllabus/3-index/B-tree=delete3.html as a reference
        '''
        if value in self.data:
            del self.data[value]
        # node is not in an underflow state
        print("deleting value: ", value)
        print("values: ", self.values())
        if len(self.values()) >= self.order:
            return
        # node is in an underflow state
        # delegate rebalancing up to the inner node, as it has the knowledge of the siblings and its own pointers
        if self.parent is not None:
            self.parent.balance_child(self)


    def split_node(self):
        '''
        Splits the node into two. Updates the current node in place, then adds a new node
        with half the values to the parent. The parent will handle splitting itself if needed.
        '''
        split_index = self.length // 2
        # there's enough going on here that I'm gonna let the built in handle this
        items = sorted(self.data.items())
        data1 = dict(items[:split_index])
        data2 = dict(items[split_index:])
        self.data = data1
        # new node points to parent and current node's next
        new_node = LeafNode(self.order, data2, self.tree, self.parent, self.next)
        self.next = new_node
        if self.parent is None:
            self.parent = InnerNode(self.order, [self.values()[-1]], self.tree)
            new_node.parent = self.parent
            self.parent.add_child(self)
            self.parent.add_child(new_node)
            self.tree.make_root(self.parent)
        else:
            self.parent.add_value(self.values()[-1])
            self.parent.add_child(new_node)

