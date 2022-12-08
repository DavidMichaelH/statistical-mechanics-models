# nodes_dict => dictionary {node : weight of node}
# adj_dict => {node : {node1 : weight of edge (node,node1),...,nodek : weight of edge (node,nodek)} }

class Graph:
    def __init__(self):
        """
        Initializes the graph.
        """
        self.nodes_dict = {}
        self.adj_dict = {}

    def get_nodes(self):
        """
        Returns a list of the nodes in the graph.
        :return: A list of the nodes in the graph.
        """
        return self.nodes_dict.keys()

    def get_vertex_value(self, node):
        """
        Returns the value of a node.
        :param node: The node.
        :return: The value of the node.
        """
        return self.nodes_dict[node]

    def get_neighbors(self, node):
        """
        Returns a list of the neighbors of a node.
        :param node: The node.
        :return: A list of the neighbors of the node.
        """
        return self.adj_dict[node].keys()

    def get_edge_weight(self, node_a, node_b):
        """
        Returns the weight of an edge.
        :param node_a: The first node.
        :param node_b: The second node.
        :return: The weight of the edge.
        """
        return self.adj_dict[node_a][node_b]

    def set_vertex_weight(self, node, weight):
        """
        Sets the weight of a node.
        :param node:  The node.
        :param weight: The weight of the node
        """
        self.nodes_dict[node] = weight

    def set_edge_weight(self, node1, node2, weight, directed_edge=True):
        """
        Sets the weight of an edge.
        :param node1: The first node.
        :param node2: The second node.
        :param weight: The weight of the edge (default is 0).
        :param directed_edge: If True, the edge is directed (default is True).
        """
        self.adj_dict[node1][node2] = weight
        if not directed_edge:
            self.adj_dict[node2][node1] = weight

    def add_node(self, node, weight=0):
        """
        Adds a new node to the graph.
        :param node: The node to add to the graph.
        :param weight: The weight of the node (default is 0).
        """
        # Add the node to the nodes_dict dictionary
        self.nodes_dict[node] = weight

        # If the node is not already in the adj_dict dictionary,
        # add an empty dictionary to represent the node's neighbors
        if node not in self.adj_dict:
            self.adj_dict[node] = {}

    def add_edge(self, node1, node2, weight=0, directed_edge=True):
        """
        Adds a new edge to the graph.
        :param node1: The first node.
        :param node2: The second node.
        :param weight: The weight of the edge (default is 0).
        :param directed_edge: If True, the edge is directed (default is True).
        """

        if node1 not in self.nodes_dict or node2 not in self.nodes_dict:
            return

        # Add the edge to the adj_dict dictionary
        self.adj_dict[node1][node2] = weight

        # If the edge is not directed, add the edge in the opposite direction
        if not directed_edge:
            self.adj_dict[node2][node1] = weight

    def remove_node(self, node):
        """
        Removes a node from the graph.
        :param node: The node to remove.
        """

        if node not in self.adj_dict:
            return

        # Remove the node from the nodes_dict dictionary
        del self.nodes_dict[node]

        # Remove the node from the adj_dict dictionary
        del self.adj_dict[node]

        # Remove the node from the adj_dict dictionaries of all other nodes
        for other_node in self.adj_dict:
            if node in self.adj_dict[other_node]:
                del self.adj_dict[other_node][node]

    def remove_edge(self, node1, node2, directed_edge=True):
        """
        Removes an edge from the graph.
        :param node1: The first node.
        :param node2: The second node.
        :param directed_edge: If True, the edge is directed (default is True).
        """
        # Remove the edge from the adj_dict dictionary
        del self.adj_dict[node1][node2]

        # If the edge is not directed, remove the edge in the opposite direction
        if not directed_edge:
            del self.adj_dict[node2][node1]


    def has_node(self, node):
        """
        Returns True if the graph contains the node.
        :param node: The node.
        :return: True if the graph contains the node.
        """
        return node in self.nodes_dict

    def has_edge(self, node1, node2):
        """
        Returns True if the graph contains the edge.
        :param node1: The first node.
        :param node2: The second node.
        :return: True if the graph contains the edge.
        """
        return node2 in self.adj_dict[node1]




