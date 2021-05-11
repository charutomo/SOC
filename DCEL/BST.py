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

    def get_largest_child(self):
        pass

    def get_smallest_child(self):
        pass

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

    def find_arc(self, arc):

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
    
    def get_adjacent_arcs(self, arc):
        def get_adjacent_arcs(current_node, arc):
            adjacent_arcs = []
            if isinstance(current_node.right_child, BeachLineLeafNode):
                if current_node.right_child.content == arc.focus:
                    adjacent_arcs.append(current_node.left_child.get_largest_child())
            else:
                adjacent_arcs.extend(get_adjacent_arcs(current_node.right_child, arc))
            if isinstance(current_node.left_child, BeachLineLeafNode):
                if current_node.left_child.content == arc.focus:
                    adjacent_arcs.append(current_node.right_child.get_smallest_child())
            else:
                adjacent_arcs.extend(get_adjacent_arcs(current_node.left_child, arc))

            return adjacent_arcs
        return get_adjacent_arcs(self.root, arc)

    def display(self):
        self.root.display()

class BeachLineInternalNode(Node):
    def __init__(self, left_site, right_site):
        Node.__init__(self, [left_site, right_site])

    @Node.left_child.setter
    def left_child(self, new_child):
        self._left_child = new_child
        self.content[0] = new_child.get_largest_child()

    @Node.right_child.setter
    def right_child(self, new_child):
        self._right_child = new_child
        self.content[1] = new_child.get_smallest_child()

    def get_breakpoint(self, directrix):
        left_arc = self.get_largest_child()
        right_arc = self.get_smallest_child()

        return Parabola.get_breakpoint(left_arc.content, right_arc.content, directrix)

    def get_largest_child(self):
        current_node = self
        while not isinstance(current_node, BeachLineLeafNode):
            current_node = current_node.right_child

            if current_node is None:
                print("Largest node is None")
                return

        return current_node

    def get_smallest_child(self):
        current_node = self
        while not isinstance(current_node, BeachLineLeafNode):
            current_node = current_node.left_child

            if current_node is None:
                print("Smallest node is None")
                return

        return current_node

    def display(self):
        print("Internal (", self.content[0].ToString(), self.content[1].ToString(), ")")
        self.left_child.display()
        self.right_child.display()

class BeachLineLeafNode(Node):
    def __init__(self, arc_site):
        Node.__init__(self, arc_site)

    def get_largest_child(self):
        return self

    def get_smallest_child(self):
        return self

    def display(self):
        self.content.Print()