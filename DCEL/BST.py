from Geometry.Parabola import Parabola

class Node():
    def __init__(self, content):
        self.content = content
        self._left_child = None
        self._right_child = None

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, new_child):
        self._left_child = new_child

    @left_child.deleter
    def left_child(self):
        del self._left_child

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, new_child):
        self._right_child = new_child

    @right_child.deleter
    def right_child(self):
        del self._right_child

    def __eq__(self, o):
        return id(self) == id(o)

    def display(self):
        pass

class BeachLine():
    def __init__(self):
        self.root = None

    def append(self, arc, directrix):
        if self.root is None:
            self.root = BeachLineLeafNode(arc.focus)
        else:
            parent, closest_arc = self.find_closest_arc(arc.focus, directrix)
            if closest_arc is not None:
                new_internal_node = None
                if closest_arc.content.x < arc.focus.x:
                    new_internal_node = BeachLineInternalNode(closest_arc.content, arc.focus)
                    new_internal_node.left_child = BeachLineLeafNode(closest_arc.content)
                    new_internal_node.right_child = BeachLineLeafNode(arc.focus)
                elif closest_arc.content.x > arc.focus.x:
                    new_internal_node = BeachLineInternalNode(arc.focus, closest_arc.content)
                    new_internal_node.left_child = BeachLineLeafNode(arc.focus)
                    new_internal_node.right_child = BeachLineLeafNode(closest_arc.content)

                # Replace closestArc
                if parent is not None:
                    if parent.left_child is closest_arc:
                        parent.left_child = new_internal_node
                    elif parent.right_child is closest_arc:
                        parent.right_child = new_internal_node
                else:
                    # Parent being none implies that this is the root node
                    self.root = new_internal_node
            else:
                print("Closest Arc not Found.")

    def remove_leaf_node(self, leaf_node):
        def remove_leaf_node(current_node, leaf_node):
            if current_node is None:
                return

            if current_node.left_child == leaf_node:
                current_node.left_child = None
                return
            elif current_node.right_child == leaf_node:
                current_node.right_child = None
                return
            else:
                remove_leaf_node(current_node.left_child, leaf_node)
                remove_leaf_node(current_node.right_child, leaf_node)

        remove_leaf_node(self.root, leaf_node)
        self.validate_tree()

    def validate_tree(self):
        def validate_tree(parent_node, current_node):
            if current_node is None:
                return
            validate_tree(current_node, current_node.left_child)
            validate_tree(current_node, current_node.right_child)

            if not isinstance(current_node.left_child, BeachLineInternalNode) \
            and not isinstance(current_node.right_child, BeachLineInternalNode):
                if current_node.left_child is None or current_node.right_child is None:
                    if parent_node.left_child == current_node:
                        parent_node.left_child = current_node
                    elif parent_node.right_child == current_node:
                        parent_node.right_child = current_node
                elif current_node.left_child == current_node.right_child:
                    if parent_node.left_child == current_node:
                        parent_node.left_child = current_node.left_child
                    elif parent_node.right_child == current_node:
                        parent_node.right_child = current_node.left_child

    # Always returns an arc and its parent
    def find_closest_arc(self, focus, directrix):
        def find_closest_arc(current_node, focus, directrix):
            if isinstance(current_node, BeachLineInternalNode):
                current_breakpoint = current_node.get_breakpoint(directrix)
                if focus.x < current_breakpoint.x:
                    if isinstance(current_node.left_child, BeachLineLeafNode):
                        return current_node, current_node.left_child
                    elif isinstance(current_node.left_child, BeachLineInternalNode):
                        return find_closest_arc(current_node.left_child, focus, directrix)
                if focus.x > current_breakpoint.x:
                    if isinstance(current_node.right_child, BeachLineLeafNode):
                        return current_node, current_node.right_child
                    elif isinstance(current_node.right_child, BeachLineInternalNode):
                        return find_closest_arc(current_node.right_child, focus, directrix)
            elif isinstance(current_node, BeachLineLeafNode):
                return None, current_node
            else:
                return None, None

        return find_closest_arc(self.root, focus, directrix)
    
    def display(self):
        self.root.display()

class BeachLineInternalNode(Node):
    def __init__(self, left_site, right_site):
        Node.__init__(self, [left_site, right_site])

    @Node.left_child.setter
    def left_child(self, new_child):
        self._left_child = new_child
        right_most_child_in_left_tree = new_child
        while not isinstance(right_most_child_in_left_tree, BeachLineLeafNode):
            right_most_child_in_left_tree = right_most_child_in_left_tree.right_child
            
        self.content[0] = right_most_child_in_left_tree.content

    @Node.right_child.setter
    def right_child(self, new_child):
        self._right_child = new_child
        left_most_child_in_right_tree = new_child
        while not isinstance(left_most_child_in_right_tree, BeachLineLeafNode):
            left_most_child_in_right_tree = left_most_child_in_right_tree.left_child
            
        self.content[1] = left_most_child_in_right_tree.content

    def get_breakpoint(self, directrix):
        left_arc = self.left_child     # The right most arc in the subtree of the left child
        while not isinstance(left_arc, BeachLineLeafNode):
            left_arc = left_arc.right_child

            if left_arc is None:
                print("Left Arc is None")
                return

        right_arc = self.right_child
        while not isinstance(right_arc, BeachLineLeafNode):
            right_arc = right_arc.left_child

            if right_arc is None:
                print("Right Arc is None")
                return

        return Parabola.get_breakpoint(left_arc.content, right_arc.content, directrix)
    
    def display(self):
        print("Internal (", self.content[0].ToString(), self.content[1].ToString(), ")")
        self.left_child.display()
        self.right_child.display()

class BeachLineLeafNode(Node):
    def __init__(self, arc_site):
        Node.__init__(self, arc_site)

    def display(self):
        self.content.Print()