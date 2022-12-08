from graphs.graph import Graph


class PlanarWeightedLattice(Graph):

    def create_lattice(self, height, width):

        self.width = width
        self.height = height

        # Initialize vertices
        for w in range(0, self.width):
            for h in range(0, self.height):
                self.add_node((w, h))

        # Initialize edges
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.adj_dict[(x, y)] = {x: 0 for x in self.generate_neighbors(x, y)}

    def get_edge_weights_on_path(self, xpath, ypath):
        edge_weights = [];

        for itr in range(len(xpath) - 1):
            edge_weights.append(self.get_edge_weight((xpath[itr], ypath[itr]), (xpath[itr + 1], ypath[itr + 1])))

        return edge_weights

    def generate_neighbors(self, x, y):
        pass
