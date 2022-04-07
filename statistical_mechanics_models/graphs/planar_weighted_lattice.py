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
                self.adj_dict[(x, y)] = {x : 0 for x in self.GenerateNeighbors(x, y)}
                
                
    def GetEdgeWeightsOnPath(self,Xpath,Ypath):
        edgeWeights = [];
        
        for itr in range(len(Xpath)-1):
            edgeWeights.append(self.GetEdgeWeight((Xpath[itr],Ypath[itr]),(Xpath[itr+1],Ypath[itr+1])))
            
        return edgeWeights   
    
    
    def GenerateNeighbors(self,x,y):
        pass
    
    
     
    