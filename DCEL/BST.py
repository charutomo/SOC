from Geometry.Parabola import Parabola

class BinarySeachTree():
    def __init__(self):
        self.root = None

class Node():
    def __init__(self, content):
        self.content = content
        self.left_child = None
        self.right_child = None

    def __eq__(self, o):
        return id(self) == id(o)

class BeachLine():
    def __init__(self):
        self.root = None

    def append(self, arc, directrix):
        if self.root is None:
            self.root = BeachLineLeafNode(arc.site)
        else:
            parent, closest_arc = self.find_closest_arc(arc.site, directrix)
            if closest_arc is not None:
                new_internal_node = None
                if closest_arc.site.x < arc.site.x:
                    new_internal_node = BeachLineInternalNode(closest_arc.site, arc.site)
                    new_internal_node.left_child = BeachLineLeafNode(closest_arc.site)
                    new_internal_node.right_child = BeachLineLeafNode(arc.site)
                elif closest_arc.site.x > arc.site.x:
                    new_internal_node = BeachLineInternalNode(arc.site, closest_arc.site)
                    new_internal_node.left_child = BeachLineLeafNode(arc.site)
                    new_internal_node.right_child = BeachLineLeafNode(closest_arc.site)

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

            if current_node.left_child is not BeachLineInternalNode \
            and current_node.right_child is not BeachLineInternalNode:
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
    def find_closest_arc(self, site, directrix):
        def find_closest_arc(current_node, site, directrix):
            if current_node is BeachLineInternalNode:
                current_breakpoint = current_node.get_breakpoint(directrix)
                if site.x < current_breakpoint.x:
                    if current_node.left_child is BeachLineLeafNode:
                        return current_node, current_node.left_child
                    elif current_node.left_child is BeachLineInternalNode:
                        return find_closest_arc(current_node.left_child, site, directrix)
                if site.x > current_breakpoint.x:
                    if current_node.right_child is BeachLineLeafNode:
                        return current_node, current_node.right_child
                    elif current_node.right_child is BeachLineInternalNode:
                        return find_closest_arc(current_node, site, directrix)
            elif current_node is BeachLineLeafNode:
                return None, current_node
            else:
                return None, None

        return find_closest_arc(self.root, site, directrix)

class BeachLineInternalNode(Node):
    def __init__(self, left_site, right_site):
        Node.__init__(self, (left_site, right_site))

    @left_child.setter
    def left_child(self, new_child):
        self.left_child = new_child
        self.content[0] = new_child

    @right_child.setter
    def right_child(self, new_child):
        self.right_child = new_child
        self.content[1] = new_child

    def get_breakpoint(self, directrix):
        return Parabola.GetBreakpoint(self.content[0], self.content[1], directrix)

class BeachLineLeafNode(Node):
    def __init__(self, arc_site):
        Node.__init__(self, arc_site)
