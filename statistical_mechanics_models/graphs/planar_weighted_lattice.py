from graphs.graph import Graph

class PlanarWeightedLattice(Graph):
     
    def CreateLattice(self,height,width):
    
        self.width = width
        self.height = height
    
        # Initialize vertices
        for w in range(0, self.width):
            for h in range(0, self.height):
                self.nodes_dict[(w, h)] = 0
    
        # Initialize edges
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.adj_dict[(x, y)] = {x : 0 for x in self.GetNeighbors(x, y)}
                
                
    def SetVertexWeight(self,node, weight):
        self.nodes_dict[node] = weight
        
        
    def SetEdgeWeight(self, node1, node2, weight):
        self.adj_dict[node1][node2] = weight
        
        
    def GetNeighbors(self,x,y):
        pass