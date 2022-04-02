#nodes_dict => dictionary {node : weight of node}
#adj_dict => {node : {node1 : weight of edge (node,node1),...,nodek : weight of edge (node,nodek)} }   
 
class Graph(object):
    def __init__(self, nodes_dict = {}, adj_dict= {}):
        self.nodes_dict = nodes_dict
        self.adj_dict = adj_dict
 
        
    def get_nodes(self):
        "Returns the nodes of the graph."
        return list(self.nodes_dict.keys())
    

    
    def vertexValue(self, node):
        "Returns the value of a vertex."
        return self.nodes_dict[node]
    
    def getNeighbors(self,node):
        return self.adj_dict[node].keys()
    
    def getEdgeWeight(self,nodeA,nodeB):
        return self.adj_dict[nodeA][nodeB]
        