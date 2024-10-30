#!python3

from b_plus_tree import BPlusTree
from leaf_node import LeafNode
from inner_node import InnerNode
import unittest


class BPlusTreeTest(unittest.TestCase):
    '''
    Test class for the B+ tree
    '''
    def test_create_tree(self):
        '''
        Test creating a new tree
        '''
        tree = BPlusTree(3, 1, 'jim')
        assert tree.root.data == {'jim': [1]}
        assert tree.root.order == 3
        assert isinstance(tree.root, LeafNode)

    def test_basic_insert(self):
        '''
        Test inserting a new value into the tree with no splits
        '''
        tree = BPlusTree(3, 1, 'jim')
        tree.insert('bob', 2)
        self.assertEqual(tree.root.data,{'jim': [1], 'bob': [2]})

    def test_create_and_insert_higher_order(self):
        '''
        Test creating a tree with a higher order and building it up
        '''
        tree = BPlusTree(2, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 4)
        self.assertEqual(tree.root.data, {'jim': [1], 'bob': [2], 'joe': [3], 'jill': [4]})
        tree.insert('jane', 5)
        self.assertEqual(tree.root.values(), ['jane'])
        self.assertEqual(tree.root.children[0].data, {'bob': [2], 'jane': [5]})
        self.assertEqual(tree.root.children[1].data, {'jim': [1], 'joe': [3], 'jill': [4]})

    def test_split_leaf_node_create_root(self):
        '''
        Test inserting a new value into the tree that causes a leaf node split when the root is a leaf node
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        self.assertIsInstance(tree.root, InnerNode)
        self.assertEqual(tree.root.values(), ['bob'])
        self.assertIsInstance(tree.root.children[0], LeafNode)
        self.assertIsInstance(tree.root.children[1], LeafNode)
        self.assertEqual(tree.root.children[0].data, {'bob': [2]})
        self.assertEqual(tree.root.children[1].data, {'jim': [1], 'joe': [3]})
        self.assertEqual(tree.root.children[0].next, tree.root.children[1])
        self.assertEqual(tree.root.children[1].next, None)
        self.assertEqual(tree.root.children[0].parent, tree.root)
        self.assertEqual(tree.root.children[1].parent, tree.root)

    def test_inserting_existing_value(self):
        '''
        Test inserting a value that already exists in the tree
        '''
        tree = BPlusTree(3, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('bob', 3)
        self.assertEqual(tree.root.data, {'jim': [1], 'bob': [2, 3]})

    def test_split_leaf_node_root_exists(self):
        '''
        Test inserting a new value into the tree that causes a leaf node split
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 4)
        self.assertEqual(tree.root.values(), ['bob', 'jill'])
        self.assertEqual(tree.root.children[0].data, {'bob': [2]})
        self.assertEqual(tree.root.children[1].data, {'jill': [4]})
        self.assertEqual(tree.root.children[2].data, {'jim': [1], 'joe': [3]})
        self.assertEqual(tree.root.children[0].next, tree.root.children[1])
        self.assertEqual(tree.root.children[1].next, tree.root.children[2])
        self.assertEqual(tree.root.children[2].next, None)

    def test_split_root_node(self):
        '''
        Test inserting a new value into the tree that causes a root split
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 4)
        tree.insert('jane', 5)
        tree.insert('jackie', 6)
        self.assertEqual(tree.root.values(), ['jackie'])
        self.assertEqual(tree.root.children[0].values(), ['bob'])
        self.assertEqual(tree.root.children[1].values(), ['jill'])
        self.assertEqual(tree.root.children[0].children[0].data, {'bob': [2]})
        self.assertEqual(tree.root.children[0].children[0].next, tree.root.children[0].children[1])
        self.assertEqual(tree.root.children[0].children[1].data, {'jackie': [6]})
        self.assertEqual(tree.root.children[0].children[1].next, tree.root.children[1].children[0])
        self.assertEqual(tree.root.children[1].children[0].data, {'jane': [5], 'jill': [4]})
        self.assertEqual(tree.root.children[1].children[0].next, tree.root.children[1].children[1])
        self.assertEqual(tree.root.children[1].children[1].data, {'jim': [1], 'joe': [3]})
        self.assertEqual(tree.root.children[0].children[0].parent, tree.root.children[0])
        self.assertEqual(tree.root.children[0].children[1].parent, tree.root.children[0])
        self.assertEqual(tree.root.children[1].children[0].parent, tree.root.children[1])
        self.assertEqual(tree.root.children[1].children[1].parent, tree.root.children[1])

    def test_split_inner_node(self):
        '''
        Test inserting a new value into the tree that causes an inner node split
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 4)
        tree.insert('jane', 5)
        tree.insert('jackie', 6)
        tree.insert('jimmy', 7)
        self.assertEqual(tree.root.children[1].values(), ['jill', 'jim'])
        tree.insert('rick', 8)
        self.assertEqual(tree.root.values(), ['jackie', 'jim'])
        self.assertEqual(tree.root.children[0].values(), ['bob'])
        self.assertEqual(tree.root.children[1].values(), ['jill'])
        self.assertEqual(tree.root.children[2].values(), ['jimmy'])
        self.assertEqual(tree.root.children[0].children[0].data, {'bob': [2]})
        self.assertEqual(tree.root.children[0].children[1].data, {'jackie': [6]})
        self.assertEqual(tree.root.children[1].children[0].data, {'jane': [5], 'jill': [4]})
        self.assertEqual(tree.root.children[1].children[1].data, {'jim': [1]})
        self.assertEqual(tree.root.children[2].children[0].data, {'jimmy': [7]})
        self.assertEqual(tree.root.children[2].children[1].data, {'joe': [3], 'rick': [8]})

    def test_to_json_returns_an_accurate_representation_of_a_tree(self):
        '''
        Test that the to_json method returns an accurate representation of the tree
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 4)
        tree.insert('jane', 5)
        tree.insert('jackie', 6)
        tree.insert('jimmy', 7)
        tree.insert('rick', 8)
        result = tree.to_json()
        print(result)
        self.assertEqual(result, {
            '0': ['jackie', 'jim'],
            '1': [['bob'], ['jill'], ['jimmy']],
            '2': [['bob'], ['jackie'], ['jane', 'jill'], ['jim'], ['jimmy'], ['joe', 'rick']]
        })

    def test_delete_value_no_underflow(self):
        '''
        Test deleting a value from the tree that doesn't cause an underflow
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.delete('joe', 3)
        self.assertEqual(tree.root.values(), ['bob'])
        self.assertEqual(tree.root.children[0].data, {'bob': [2]})
        self.assertEqual(tree.root.children[1].data, {'jim': [1]})

    def test_delete_value_with_underflow_left_sibling(self):
        '''
        Test deleting a value from the tree that causes an underflow and the left sibling can transfer
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('abe', 4)
        tree.insert('jill', 5)
        tree.delete('jill', 5)
        # the pointer values just need to point correctly, its okay if they contain deleted values
        self.assertEqual(tree.root.values(), ['abe', 'jill'])
        self.assertEqual(tree.root.children[0].data, {'abe': [4]})
        self.assertEqual(tree.root.children[1].data, {'bob': [2]})
        self.assertEqual(tree.root.children[2].data, {'jim': [1], 'joe': [3]})

    def test_delete_value_with_underflow_right_sibling(self):
        '''
        Test deleting a value from the tree that causes an underflow and the right sibling can transfer
        '''
        tree = BPlusTree(1, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 5)
        tree.delete('jill', 5)
        self.assertEqual(tree.root.values(), ['bob', 'jim'])
        self.assertEqual(tree.root.children[0].data, {'bob': [2]})
        self.assertEqual(tree.root.children[1].data, {'jim': [1]})
        self.assertEqual(tree.root.children[2].data, {'joe': [3]})

    def test_delete_value_with_underflow_merge_left(self):
        '''
        Test deleting a value from the tree that causes an underflow and merge with left sibling
        '''
        tree = BPlusTree(2, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 4)
        tree.insert('jane', 5)
        tree.insert('rob', 6)
        tree.insert('rick', 7)
        self.assertEqual(tree.root.values(), ['jane','jim'])
        self.assertEqual(tree.root.children[0].data, {'bob': [2], 'jane': [5]})
        self.assertEqual(tree.root.children[1].data, {'jill': [4], 'jim': [1]})
        self.assertEqual(tree.root.children[2].data, {'joe': [3], 'rick': [7], 'rob': [6]})
        tree.delete('rob', 6)
        tree.delete('jim', 1)
        self.assertEqual(tree.root.values(), ['jim'])
        self.assertEqual(tree.root.children[0].data, {'bob': [2], 'jane': [5], 'jill': [4]})
        self.assertEqual(tree.root.children[1].data, {'joe': [3], 'rick': [7]})

    def test_delete_value_with_underflow_merge_right(self):
        '''

        Test deleting a value from the tree that causes an underflow and merge with right sibling
        '''
        tree = BPlusTree(2, 1, 'jim')
        tree.insert('bob', 2)
        tree.insert('joe', 3)
        tree.insert('jill', 4)
        tree.insert('jane', 5)
        tree.insert('rob', 6)
        tree.insert('rick', 7)
        self.assertEqual(tree.root.values(), ['jane','jim'])
        self.assertEqual(tree.root.children[0].data, {'bob': [2], 'jane': [5]})
        self.assertEqual(tree.root.children[1].data, {'jill': [4], 'jim': [1]})
        self.assertEqual(tree.root.children[2].data, {'joe': [3], 'rick': [7], 'rob': [6]})
        tree.delete('bob', 2)
        self.assertEqual(tree.root.values(), ['jim'])
        self.assertEqual(tree.root.children[0].data, {'jane': [5], 'jill': [4], 'jim': [1]})
        self.assertEqual(tree.root.children[1].data, {'joe': [3], 'rick': [7], 'rob': [6]})

    def test_delete_value_with_underflow_merge_then_transfer(self):
        '''
        Test deleting a value from the tree that causes an underflow and merge right, then a transfer of a leaf
        node from the right sibling of the parent
        '''
        tree = BPlusTree(2, 10, 10)
        tree.insert_many([20, 30, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160])
        tree.delete(50, 50)


