
from graphs.planar_weighted_lattice import PlanarWeightedLattice


class TriangularLattice(PlanarWeightedLattice):
 
        
 
    def generate_neighbors(self, x, y):
        NeighborsList = []
        
        if y < self.height-1:
            NeighborsList.append((x,y+1))
        
        if y > 0:
            NeighborsList.append((x,y-1))
            
        if x < self.width-1:
            NeighborsList.append((x+1,y))
            
        if x > 0:
            NeighborsList.append((x-1,y))
            
        if x%2 == 0:
            if x>0 and y > 0:
                NeighborsList.append((x-1,y-1))
            if x < self.width-1 and y > 1:
                NeighborsList.append((x+1,y-1))
        else:
            if x>0 and y <self.height-1:
                NeighborsList.append((x-1,y+1))
            if x < self.width-1 and y <self.height-1:
                NeighborsList.append((x+1,y+1))
            
        return NeighborsList
         
          
         
        
 
