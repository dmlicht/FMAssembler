class Node(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.outgoing = {}

    def add_outgoing_edge(self, edge, child):
        self.outgoing[edge.label[:1]] = edge

class Edge(object):
    def __init__(self, parent, child, label):
        self.parent = parent
        self.child = child
        self.label = label

    def append_label(self, s):
        self.label = self.label + s

class Ukkonen(object):
    """Test implementation of Ukkonen's algorithm for 
    linear time suffix sorting of the text."""
    def __init__(self, t):
        self.t = t
        self.implicit_suffix_tree_root = Node()

        for i in xrange(1, len(t)):
            t_i = t[0:i]
            for j in xrange(len(t_i)):
                self.extend(self.implicit_suffix_tree_root, t_i[j:])

    def extend(self, new_s):
        """traverse current implicit suffix tree adding nodes where new string diverges"""
        current_node = self.implicit_suffix_tree_root
        current_new_s_segment = new_s
        #oe - outgoing edge

        while len(current_new_s_segment) > 0:
            oe = current_node.outgoing.get(current_new_s_segment[:1])
            if oe == None:
                new_edge = Edge(current_node, Node(current_node), current_new_s_segment)
                current_node.add_outgoing_edge(new_edge)
                current_new_s_segment = ""
            elif current_new_s_segment.startswith(oe.label):
                current_new_s_segment = current_new_s_segment[len(oe.label):]
                current_node = oe.child
            elif oe.label.startswith(current_new_s_segment):
                current_new_s_segment = ""
            #they diverge in the middle of the string
            else:
                i = 0
                while oe.label[i] == current_new_s_segment[i]:
                    i += 1
                new_edge = Edge(current_node, Node(current_node), current_new_s_segment[i:])
                current_new_s_segment = ""

        


    # def construct_implicit_st(self, s_i, implicit_st_i_minus_one):
    #     """constructs the implicit suffix tree for the substring ranging from 0:i
    #     of the text t
    #     s_i is substring of text t from 0:i
    #     implicit_st_i_minus_one is the implicit suffix tree for the substring 0:i-1"""
        
    #     #base case
    #     if len(s_i) == 1:
    #         