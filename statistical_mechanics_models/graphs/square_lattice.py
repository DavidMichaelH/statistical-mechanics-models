from graph import Graph


class SquareLattice(Graph):

    #This sort of method could be generic weighted graph
    def CreateSquareLattice(self,height,width):
    
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
                
                
    #This could be overridden from some generic class 
    def GetNeighbors(self,x,y):
        NeighborsList = []
        
        if y < self.width-1:
            NeighborsList.append((x,y+1))
        
        if y > 0:
            NeighborsList.append((x,y-1))
            
        if x < self.height-1:
            NeighborsList.append((x+1,y))
            
        if x > 0:
            NeighborsList.append((x-1,y))
            
        return NeighborsList
    
    
    def SetVertexWeight(self,node, weight):
        self.nodes_dict[node] = weight
        
        
    def SetEdgeWeight(self, node1, node2, weight):
        self.adj_dict[node1][node2] = weight
        
         