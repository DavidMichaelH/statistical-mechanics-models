
import sys
import heapq as heap


class FPP:

    def __init__(self, graph, start_node=None):
        self.graph = graph
        self.start_node = start_node
        self.previous_nodes = None
        self.distance_field = None
        self.distance_field_LIST = None

    def SetGraphAndStartNode(self, graph, start_node):
        self.graph = graph
        self.start_node = start_node

    def ComputeDistanceField(self):
        
        self.dijkstra()
        self.DistanceFieldToMultiDimList()

        return self.distance_field_LIST
 
    
    
    # dijsktra with Priority Queue

    def dijkstra(self):
        visited = set()
        pQueue = []
        heap.heappush(pQueue,(self.graph.value(self.start_node), self.start_node))
        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        self.distance_field = {}
        graph_distance = {}  
        # We'll use this dict to save the shortest known path to a node found so far
        self.previous_nodes = {}
        
 
        max_value = sys.maxsize
        for node in list(self.graph.get_nodes()):
            self.distance_field[node] = max_value
            graph_distance[node] = max_value   
        self.distance_field[self.start_node] = self.graph.value(
            self.start_node)
        graph_distance[self.start_node] = 0  #  
        
        while pQueue:

            value, node = heap.heappop(pQueue)
 
            current_min_node = node
            current_min_node_value = value
            PossibleMinimums =[]

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
            neighbors = self.graph.getNeighbors(current_min_node)

            for neighbor in neighbors:
                
                if neighbor in visited:
                    continue
                
                tentative_value = self.distance_field[current_min_node] + self.graph.value(
                    neighbor)

                if tentative_value < self.distance_field[neighbor]:
                    self.distance_field[neighbor] = tentative_value
                    # We also update the best path to the current node
                    self.previous_nodes[neighbor] = current_min_node
                    
                    
                    graph_distance[neighbor] = graph_distance[current_min_node] + 1
                    heap.heappush(pQueue, (tentative_value, neighbor))
                 
                elif tentative_value == self.distance_field[neighbor]:
                    if graph_distance[neighbor] > graph_distance[current_min_node] + 1:   
                         
                        self.previous_nodes[neighbor] = current_min_node
                         
                        graph_distance[neighbor] = graph_distance[current_min_node] + 1
 
 
    def DistanceFieldToMultiDimList(self):
        self.distance_field_LIST = [
            [0] * self.graph.width for i in range(self.graph.height)]
        for node in self.distance_field.keys():
            self.distance_field_LIST[node[1]][node[0]
                                              ] = self.distance_field[node]

    def ComputeGeodesic(self, target_node):
        Xpath = []
        Ypath = []
        node = target_node
        Xpath.insert(0, node[0])
        Ypath.insert(0, node[1])
        XNonzeroSites = []
        YNonzeroSites = []

        while node != self.start_node:
            next_node = self.previous_nodes[node]

            if self.graph.value(node) > 0:
                XNonzeroSites.insert(0, node[0])
                YNonzeroSites.insert(0, node[1])

            node = next_node
            Xpath.insert(0, node[0])
            Ypath.insert(0, node[1])

        Xpath.insert(0, self.start_node[0])
        Ypath.insert(0, self.start_node[1])

        return (Xpath, Ypath), (XNonzeroSites, YNonzeroSites)
    
    
    #Returns passage time from self.startnode 
    #to the boundary
    def PassageTimeToBoundary(self):
        passageTimeToBoundary = sys.maxsize
        minCoordinates = (0,0)
        for w in range(self.graph.width):
            if passageTimeToBoundary > self.distance_field_LIST[0][w]:
                passageTimeToBoundary = self.distance_field_LIST[0][w]
                minCoordinates = (w,0)
            
            if passageTimeToBoundary > self.distance_field_LIST[self.graph.height-1][w]:
                passageTimeToBoundary = self.distance_field_LIST[self.graph.height-1][w]
                minCoordinates = (w,self.graph.height-1)
        for h in range(self.graph.height):
            if passageTimeToBoundary > self.distance_field_LIST[h][0]:
                passageTimeToBoundary = self.distance_field_LIST[h][0]
                minCoordinates = (0,h)
            if passageTimeToBoundary > self.distance_field_LIST[h][self.graph.width-1]:
                passageTimeToBoundary = self.distance_field_LIST[h][self.graph.width-1]
                minCoordinates = (self.graph.width-1,h)
                 
        return passageTimeToBoundary , minCoordinates
        
             
            
            
            
            
        
