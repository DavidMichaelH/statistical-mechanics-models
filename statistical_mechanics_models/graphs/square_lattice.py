from graphs.planar_weighted_lattice import PlanarWeightedLattice


class SquareLattice(PlanarWeightedLattice):
    
 
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
    
    
    
        
         