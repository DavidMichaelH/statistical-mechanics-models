 
#nodes_dict => dictionary {node : weight of node}
#adj_dict => {node : [node1,node2,...,nodek]}  "Node is key and neighbors are value"
 
class GraphSite(object):
    def __init__(self, nodes_dict = {}, adj_dict= {}):
        self.nodes_dict = nodes_dict
        self.adj_dict = adj_dict
 
        
    def get_nodes(self):
        "Returns the nodes of the graph."
        return list(self.nodes_dict.keys())
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) is not False:
                connections.append(out_node)
        return connections
    
    def value(self, node):
        "Returns the value of a vertex."
        return self.nodes_dict[node]
    
    
    def getNeighbors(self,node):
        return self.adj_dict[node]

    
    