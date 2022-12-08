from graphs.planar_weighted_lattice import PlanarWeightedLattice


class SquareLattice(PlanarWeightedLattice):

    def __init__(self, width, height):
        super().__init__(width, height)

    # generates the neighbors of a node in a square lattice
    def generate_neighbors(self, w, h):
        """
        Generates the neighbors of a node in a square lattice.

        :param w: The x-coordinate of the node.
        :param h: The y-coordinate of the node.
        :return: A list of tuples representing the neighboring nodes.
        """
        neighbors_list = []
        
        if h < self.height-1:
            neighbors_list.append((w, h+1))
        
        if h > 0:
            neighbors_list.append((w, h-1))
            
        if w < self.width-1:
            neighbors_list.append((w+1, h))
            
        if w > 0:
            neighbors_list.append((w-1, h))
            
        return neighbors_list
