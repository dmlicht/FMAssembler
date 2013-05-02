import Queue

class Edge(object):
    def __init__(self, x, y, xy_label, yx_label):
        self.xy_label = xy_label
        self.yx_label = yx_label
        self.x = x
        self.y = y
        self.weight = 1


class Node(object):
    def __init__(self, string):
        self.string = string
        self.suffix_overlaps = []
        self.prefix_overlaps = []


class OverlapGraph(object):
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_edge(self, from_string, to_string, overlap_len):
        """creates corresponding new edge and adds it to the graph
        if either node in the edge is not present, they will be created
        and added as well"""
        existing_edge = self.edges.get((from_string, to_string), 0)
        if existing_edge:
            existing_edge.weight += 1
            return

        #make sure new nodes are in the graph
        for string in [from_string, to_string]:
            if string not in self.nodes:
                self.add_node(string)

        from_node = self.nodes[from_string]
        to_node = self.nodes[to_string]

        edge = Edge(from_node, to_node, to_string[overlap_len:], from_string[:-1*overlap_len])
        self.edges[(from_string, to_string)] = edge
        #add overlaps to nodes
        from_node.suffix_overlaps.append(edge)
        to_node.prefix_overlaps.append(edge)

    def add_node(self, string):
        """creates and adds node to graph"""
        node = Node(string)
        self.nodes[string] = node

    def get_contigs(self):
        """constructs the contigs implied by the string graph"""
        contigs = []
        start_node_q = Queue.Queue()
        start_node_q.put(self.find_start_node())
        # print self.find_start_node()
        seen_strings = set([])
        while not start_node_q.empty():
            run_start_node = start_node_q.get()
            seen_strings.add(run_start_node.string)
            run_string, branch_nodes = self.get_non_branching_run(run_start_node)
            contigs.append(run_string)
            for branch_node in branch_nodes:
                # print type(branch_node)
                if branch_node.string not in seen_strings:
                    start_node_q.put(branch_node)
        return contigs

    def get_non_branching_run(self, start_node):
        """returns string produced by run of non branching edges
        and outgoing nodes at first branch"""
        run_strings = []
        run_strings.append(start_node.string)
        node = start_node
        while len(node.suffix_overlaps) == 1:
            edge = node.suffix_overlaps[0]
            label = edge.xy_label
            run_strings.append(label)
            node = edge.y

        #if loop exits due to branch
        if len(node.suffix_overlaps) > 1:
            edges = node.suffix_overlaps
            next_nodes = [edge.y for edge in edges]
            return ''.join(run_strings), next_nodes

        #if loop because traversal falls off
        if len(node.suffix_overlaps) == 0:
            return ''.join(run_strings), []

    def find_start_node(self):
        """returns node to start building string from
        this is the node that has the fewest suffix overlaps, which will be
        0 if it is not a repeat"""
        min_incoming = 100000000 #some really high value
        min_incoming_node = ""
        for node in self.nodes.values():
            # print node
            if len(node.prefix_overlaps) < min_incoming:
                min_incoming = len(node.prefix_overlaps)
                min_incoming_node = node
        return min_incoming_node