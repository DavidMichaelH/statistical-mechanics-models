
from graphs.planar_weighted_lattice import PlanarWeightedLattice


class TriangularLattice(PlanarWeightedLattice):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.directed_lattice = False


    # generates the neighbors of a node in a square lattice
    def generate_neighbors(self, w, h):
        """
        Generates the neighbors of a node in a square lattice.

        :param w: The x-coordinate of the node.
        :param h: The y-coordinate of the node.
        :return: A list of tuples representing the neighboring nodes.
        """
            
        neighbors_list = []

        # add the top and bottom neighbors if they exist
        if h < self.height-1:
            neighbors_list.append((w, h+1))
        
        if h > 0:
            neighbors_list.append((w, h-1))

        # add the lower left and right neighbors if they exist
        if w < self.width-1:
            neighbors_list.append((w+1, h))
            
        if w > 0:
            neighbors_list.append((w-1, h))

        # add the upper left and right neighbors if they exist
        if w % 2 == 0:
            if w > 0 and h > 0:
                neighbors_list.append((w-1, h-1))
            if w < self.width-1 and h > 1:
                neighbors_list.append((w+1, h-1))
        else:
            if w > 0 and h < self.height-1:
                neighbors_list.append((w-1, h+1))
            if w < self.width-1 and h < self.height-1:
                neighbors_list.append((w+1, h+1))
            
        return neighbors_list

 
