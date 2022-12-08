from typing import Callable, List
from graphs.graph import Graph


class PlanarWeightedLattice(Graph):

    def __init__(self, width: int, height: int, directed_lattice: bool = False):
        super().__init__()
        self.width = width
        self.height = height
        self.directed_lattice = directed_lattice
        self.create_lattice()

    def create_lattice(self):
        """Set up the lattice with the given height and width."""

        # Initialize nodes
        for w in range(0, self.width):
            for h in range(0, self.height):
                self.add_node((w, h))

        # Initialize edges
        for x in range(0, self.width):
            for y in range(0, self.height):
                neighbors = self.generate_neighbors(x, y)
                for neighbor in neighbors:
                    self.add_edge((x, y), neighbor, directed_edge=self.directed_lattice)

    def get_edge_weights_on_path(self, xpath: List[int], ypath: List[int]) -> List[int]:
        edge_weights = [];

        for itr in range(len(xpath) - 1):
            edge_weights.append(self.get_edge_weight((xpath[itr], ypath[itr]), (xpath[itr + 1], ypath[itr + 1])))

        return edge_weights

    def generate_neighbors(self, x: int, y: int):
        pass

    def set_vertex_weights(self, vertex_weight: Callable[[int], float]):
        """
        Sets the weight of a node in the graph.

        :param vertex_weight: A function that takes a node's ID as input and returns its weight.
        :type vertex_weight: Callable[[int], float]
        """
        for node in self.get_nodes():
            self.set_vertex_weight(node, vertex_weight(node))

    def set_edge_weights(self, edge_weight: Callable[[int], float]):
        """
        Sets the weight of each edge in the graph.

        :param edge_weight: A function that takes the node's ID for a given edge as input and returns its weight.
        :type edge_weight: Callable[[int], float]
        """
        for edge in self.get_edges():
            self.set_edge_weight(edge[0], edge[1], edge_weight(edge))