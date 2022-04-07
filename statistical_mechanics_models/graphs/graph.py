#nodes_dict => dictionary {node : weight of node}
#adj_dict => {node : {node1 : weight of edge (node,node1),...,nodek : weight of edge (node,nodek)} }   
 
class Graph:
    def __init__(self):
        self.nodes_dict = {}
        self.adj_dict = {}
 
        
    def GetNodes(self):
        return list(self.nodes_dict.keys())
    
    
    def GetVertexValue(self, node):
        return self.nodes_dict[node]
    
    def GetNeighbors(self,node):
        return self.adj_dict[node].keys()
    
    def GetEdgeWeight(self,nodeA,nodeB):
        return self.adj_dict[nodeA][nodeB]
        
    
    def SetVertexWeight(self,node, weight):
        self.nodes_dict[node] = weight
        
        
    def SetEdgeWeight(self, node1, node2, weight, directedEdge = True):
        self.adj_dict[node1][node2] = weight
        if not directedEdge:
            self.adj_dict[node2][node1] = weight
        
        
    
    
    