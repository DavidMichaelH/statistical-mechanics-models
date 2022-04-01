


# nodes_dict => dictionary {node : weight of node}
# adj_dict => {node : [node1,node2,...,nodek]}  "Node is key and neighbors are value"


from graph import GraphSite


class TriangularLattice(GraphSite):

   def CreateTriangularLattice(self, field):

        self.width = len(field[:][0])
        self.height = len(field[0])

        # Create the nodes dictionary

        # Initialize vertices
        for w in range(0, self.width):
            for h in range(0, self.height):
                self.nodes_dict[(w, h)] = field[h][w]

        # Initialize edges
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.adj_dict[(x, y)] = self.GetNeighbors(x, y)


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
         
          
         
        
 
