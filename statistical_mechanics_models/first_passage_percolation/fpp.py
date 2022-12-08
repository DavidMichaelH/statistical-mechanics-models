
import sys
import heapq as heap

class FPP:

    def __init__(self, graph, start_node=None):
        self.graph = graph
        self.start_node = start_node
        self.previous_nodes = None
        self.distance_map = None
        self.distance_field_list = None

    def SetGraphAndStartNode(self, graph, start_node):
        self.graph = graph
        self.start_node = start_node

    def ComputeDistanceField(self):
        
        self.Dijkstra()
        self.DistanceFieldToMultiDimList()

        return self.distance_field_list
 
    
    
    # dijsktra with Priority Queue

    def Dijkstra(self):
        visited = set()
        pQueue = []
        heap.heappush(pQueue, (self.graph.get_vertex_value(self.start_node), self.start_node))
        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        self.distance_map = {}
        graph_distance = {}  
        # We'll use this dict to save the shortest known path to a node found so far
        self.previous_nodes = {}
        
 
        max_value = float("inf")
        for node in list(self.graph.get_nodes()):
            self.distance_map[node] = max_value
            graph_distance[node] = max_value   
        self.distance_map[self.start_node] = self.graph.get_vertex_value(self.start_node)
        graph_distance[self.start_node] = 0 #  
        
        while pQueue:

            
            #Over all minimums in the queue find the one with shortest graph distance 
            
            value, node = heap.heappop(pQueue)
 
            current_min_node = node
            current_min_node_value = value
            PossibleMinimums =[]

            #compares the minimum values in this list to the current minimum value,
            # and selects the minimum value with the shortest graph distance
            while pQueue: 
                
                value, node = heap.heappop(pQueue)
                
                if value > current_min_node_value:
                    heap.heappush(pQueue,(value,node))
                    break;
                    
                if graph_distance[node] < graph_distance[current_min_node]:
                    PossibleMinimums.append((current_min_node_value,current_min_node))
                    current_min_node = node
                    current_min_node_value = value
                
                    
                else:
                    PossibleMinimums.append((value,node))
                
        
            #Put them all back except for the one you selected and then exit 
            #the loop
            for vk in PossibleMinimums:
                heap.heappush(pQueue,vk)
                  
            
            visited.add(current_min_node)
                    
                    
            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = self.graph.get_neighbors(current_min_node)

            for neighbor in neighbors:
                
                if neighbor in visited:
                    continue
                
                tentative_value = self.distance_map[current_min_node] + self.graph.get_vertex_value(
                    neighbor) + self.graph.get_edge_weight(current_min_node, neighbor)

                if tentative_value < self.distance_map[neighbor]:
                    self.distance_map[neighbor] = tentative_value
                    # We also update the best path to the current node
                    self.previous_nodes[neighbor] = current_min_node
                    
                    
                    graph_distance[neighbor] = graph_distance[current_min_node] + 1
                    heap.heappush(pQueue, (tentative_value, neighbor))
                 
                elif tentative_value == self.distance_map[neighbor]:
                    if graph_distance[neighbor] > graph_distance[current_min_node] + 1:   
                         
                        self.previous_nodes[neighbor] = current_min_node
                         
                        graph_distance[neighbor] = graph_distance[current_min_node] + 1
 
 
    def DistanceFieldToMultiDimList(self):
        # creates a list of lists that is the same size as the graph.
        self.distance_field_list = [
            [0] * self.graph.width for i in range(self.graph.height)]
        for node in self.distance_map.keys():
            self.distance_field_list[node[1]][node[0]
                                              ] = self.distance_map[node]

    def ComputeGeodesic(self, target_node):
        x_path = []
        y_path = []
        edge_weights = []
        vertex_weights = []
        
        node = target_node
          
        #add the weight of the target node 
        
        vertex_weights.insert(0, self.graph.get_vertex_value(node))
        
        x_path.insert(0, node[0])
        y_path.insert(0, node[1])
 
        while node != self.start_node:
            next_node = self.previous_nodes[node]
              
            edge_weights.insert(0, self.graph.get_edge_weight(next_node, node))
 
            node = next_node

            x_path.append(node[0])
            y_path.append(node[1])
            vertex_weights.append(self.graph.get_vertex_value(node))

        x_path.reverse()
        y_path.reverse()
        vertex_weights.reverse()

        return (x_path, y_path, edge_weights,vertex_weights)
    
    
    

    
    
    
    #Returns passage time from self.startnode 
    #to the boundary
    def PassageTimeToBoundary(self):
        passageTimeToBoundary = sys.maxsize
        minCoordinates = (0,0)
        for w in range(self.graph.width):
            if passageTimeToBoundary > self.distance_field_list[0][w]:
                passageTimeToBoundary = self.distance_field_list[0][w]
                minCoordinates = (w,0)
            
            if passageTimeToBoundary > self.distance_field_list[self.graph.height - 1][w]:
                passageTimeToBoundary = self.distance_field_list[self.graph.height - 1][w]
                minCoordinates = (w,self.graph.height-1)
        for h in range(self.graph.height):
            if passageTimeToBoundary > self.distance_field_list[h][0]:
                passageTimeToBoundary = self.distance_field_list[h][0]
                minCoordinates = (0,h)
            if passageTimeToBoundary > self.distance_field_list[h][self.graph.width - 1]:
                passageTimeToBoundary = self.distance_field_list[h][self.graph.width - 1]
                minCoordinates = (self.graph.width-1,h)
                 
        return passageTimeToBoundary , minCoordinates
        
             
            
            
            
            
        
