from graphs.planar_weighted_lattice import PlanarWeightedLattice


class SquareLattice(PlanarWeightedLattice):
    
    #This could be overridden from some generic class 
    def generate_neighbors(self, w, h):
        NeighborsList = []
        
        if h < self.height-1:
            NeighborsList.append((w,h+1))
        
        if h > 0:
            NeighborsList.append((w,h-1))
            
        if w < self.width-1:
            NeighborsList.append((w+1,h))
            
        if w > 0:
            NeighborsList.append((w-1,h))
            
        return NeighborsList
    
    
    
        
         