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


