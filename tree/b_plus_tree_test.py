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


