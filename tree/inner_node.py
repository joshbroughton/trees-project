#!python3

class InnerNode:
    def __init__(self, order, values, parent=None):
        self.length = order * 2
        self.parent = parent
        self.list_values = values # these stay sorted
        self.children = []
        self.order = order

    def values(self):
        return self.list_values

    def can_transfer(self):
        return len(self.values()) > self.order

    def get_child(self, target_value):
        for index, value in enumerate(self.list_values):
            if target_value <= value:
                return self.children[index]
        return self.children[-1]

    def create_child(self):
        '''
        TODO: Maybe not actually needed
        Creates a new leaf node child when a path to insertion does not find an
        exisitng leaf node that fits the value
        '''

    def add_child(self, new_node):
        '''
        Add a child node. Called by an existing child when it splits into
        two leaf nodes, this handles updating pointers, and calls to split
        itself if it is now neccesary
        '''
        for index, value in enumerate(self.list_values):
            if new_node.values()[-1] <= value:
                self.children.insert(index, new_node)
                if len(self.list_values) > self.length:
                    self.split_node()
                return
        # if it wasn't inserted above, it belongs at the end
        self.children.append(new_node)
        if len(self.list_values) > self.length:
                self.split_node()

    def add_value(self, new_value):
        '''
        Add a new pointer value to the list
        '''
        for index, value in enumerate(self.list_values):
            if new_value <= value:
                self.list_values.insert(index, new_value)
                return
        self.list_values.append(new_value)

    def split_node(self):
        '''
        Splits this inner node into two, shares children between them, updates parent pointers
        '''
        divider = len(self.list_values) // 2
        middle_value = self.list_values.pop(divider)

        if self.parent is None:
            self.parent = InnerNode(self.order, [])
            self.parent.add_child(self)

        new_node = InnerNode(self.order, self.list_values[divider:], self.parent)
        self.list_values = self.list_values[:(divider)]

        new_node.children = self.children[(divider+1):]
        for child in new_node.children:
            child.parent = new_node
        self.children = self.children[:(divider+1)]

        self.parent.add_value(middle_value)
        self.parent.add_child(new_node)

    def balance_child(self, child):
        '''
        Balance a child node that is in an underflow state
        '''
        children_length = len(self.children)
        # if this is the only child what do we do?
        if children_length == 1:
            #something?
            return

        # get the siblings
        index = self.children.index(child)
        left_sibling = self.children[index - 1] if index >=1 else None
        right_sibling = self.children[index + 1] if index < children_length - 1 else None

        # try and transfer from the siblings
        if left_sibling and left_sibling.can_transfer():
            value, keys = left_sibling.right_value()
            child.add_leaf_entry(value, keys)
            left_sibling.delete_leaf_entry(value)
            self.list_values[index - 1] = left_sibling.right_value()[0]
        elif right_sibling and right_sibling.can_transfer():
            value, keys = right_sibling.left_value()
            child.add_leaf_entry(value, keys)
            right_sibling.delete_leaf_entry(value)
            self.list_values[index] = value
        # past this point its becuase we can't transfer, so we merge, trying for a left sibling first
        elif left_sibling:
            left_sibling.merge_node(child)
            left_sibling.next = child.next
            self.list_values.pop(index - 1)
            self.children.pop(index)
        elif right_sibling:
            right_sibling.merge_node(child)
            self.list_values.pop(index)
            self.children.pop(index)
        # after we merge, we need to make sure the parent node (ie self) is balanced
        # this is similarly solved either by transferring or merging

    def left_sibling(self):
        '''
        Get the left sibling of this inner node
        '''
        return self.parent.children[self.parent.children.index(self) - 1] if self.parent.children.index(self) > 0 else None

    def right_sibling(self):
        '''
        Get the right sibling of this inner node
        '''
        return self.parent.children[self.parent.children.index(self) + 1] if self.parent.children.index(self) < len(self.parent.children) - 1 else None

    def balance_self(self):
        '''
        Balance this node if it is in an underflow state
        '''
        # Check if either sibling can transfer





