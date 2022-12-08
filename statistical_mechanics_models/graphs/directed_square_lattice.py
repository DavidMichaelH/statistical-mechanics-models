from graphs.planar_weighted_lattice import PlanarWeightedLattice
from typing import List, Tuple

class DirectedSquareLattice(PlanarWeightedLattice):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.directed_lattice = True

    # generates the neighbors of a node in a directed square lattice
    def generate_neighbors(self, w: int, h: int) -> List[Tuple[int, int]]:
        """
        Generates the neighbors of a node in a square lattice.

        :param w: The x-coordinate of the node.
        :param h: The y-coordinate of the node.
        :return: A list of tuples representing the neighboring nodes.
        """
        neighbors_list = []

        if h < self.height - 1:
            neighbors_list.append((w, h + 1))

        if w < self.width - 1:
            neighbors_list.append((w + 1, h))


        return neighbors_list
