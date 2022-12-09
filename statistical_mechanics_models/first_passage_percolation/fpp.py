
import sys
import heapq as heap
from typing import List, Tuple


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
        
        self.dijkstra()
        self.distance_field_to_multi_dim_list()

        return self.distance_field_list
 

    def dijkstra(self):
        """
        The method uses a modified version of Dijkstra's algorithm to find the shortest path from the
        start node to all other nodes, and it prioritizes paths with the shortest graph distance among geodesics.

        :return: None
        """
        visited = set()
        priority_queue = []
        heap.heappush(priority_queue, (self.graph.get_vertex_value(self.start_node), self.start_node))
        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        self.distance_map = {}
        graph_distance = {}  
        # We'll use this dict to save the shortest known path to a node found so far
        self.previous_nodes = {}

        # Initialize the distance map with the cost of visiting each node to infinity
        max_value = float("inf")
        for node in list(self.graph.get_nodes()):
            self.distance_map[node] = max_value
            graph_distance[node] = max_value

        self.distance_map[self.start_node] = self.graph.get_vertex_value(self.start_node)
        graph_distance[self.start_node] = 0
        
        while priority_queue:

            value, node = heap.heappop(priority_queue)
 
            current_min_node = node
            current_min_node_value = value
            possible_minimums = []

            # Over all minimums in the queue find the one with the shortest graph distance
            while priority_queue:
                
                value, node = heap.heappop(priority_queue)
                
                if value > current_min_node_value:
                    heap.heappush(priority_queue, (value, node))
                    break

                # If the node is a minimum and has a shorter distance than the current minimum node, add the current
                # minimum node to the possible_minimums list and set the current minimum node to the node at
                # the top of the queue.
                if graph_distance[node] < graph_distance[current_min_node]:
                    possible_minimums.append((current_min_node_value, current_min_node))
                    current_min_node = node
                    current_min_node_value = value

                else:
                    possible_minimums.append((value, node))

            # Put them all back except for the one you selected and then exit the loop
            for vk in possible_minimums:
                heap.heappush(priority_queue, vk)

            visited.add(current_min_node)
                    
            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = self.graph.get_neighbors(current_min_node)

            for neighbor in neighbors:
                
                if neighbor in visited:
                    continue

                # Calculate tentative distance to neighbor
                tentative_value = self.distance_map[current_min_node] + self.graph.get_vertex_value(
                    neighbor) + self.graph.get_edge_weight(current_min_node, neighbor)

                # If the tentative distance is better than the current one, update the distance and previous node
                if tentative_value < self.distance_map[neighbor]:
                    self.distance_map[neighbor] = tentative_value
                    # We also update the best path to the current node
                    self.previous_nodes[neighbor] = current_min_node

                    graph_distance[neighbor] = graph_distance[current_min_node] + 1
                    heap.heappush(priority_queue, (tentative_value, neighbor))

                # If the tentative distance is equal to the current one, update the previous node if the path to the
                # current node is shorter
                elif tentative_value == self.distance_map[neighbor]:
                    if graph_distance[neighbor] > graph_distance[current_min_node] + 1:   
                         
                        self.previous_nodes[neighbor] = current_min_node
                         
                        graph_distance[neighbor] = graph_distance[current_min_node] + 1
 

    def distance_field_to_multi_dim_list(self) -> List[List[int]]:
        """
        Converts the distance field stored in a dictionary to a list of lists.

        :return: A list of lists representing the distance field.
        :rtype: list
        """
        # creates a list of lists that is the same size as the graph.
        self.distance_field_list = [
            [0] * self.graph.width for i in range(self.graph.height)]
        for node in self.distance_map.keys():
            self.distance_field_list[node[1]][node[0]] = self.distance_map[node]

    def compute_geodesic(self, target_node: Tuple[int, int]) -> Tuple[List[int], List[int], List[float], List[float]]:
        """
        Computes the geodesic path from the start node to the target node in the graph.

        :param target_node: The end node for the geodesic path.
        :type target_node: Tuple[int, int]
        :return: A tuple containing four lists representing the x-coordinates, y-coordinates, edge weights, and vertex weights of the nodes on the geodesic path.
        :rtype: Tuple[List[int], List[int], List[float], List[float]]
        """
        x_path = []
        y_path = []
        edge_weights = []
        vertex_weights = []
        
        node = target_node
          
        # add the weight of the target node
        vertex_weights.insert(0, self.graph.get_vertex_value(node))

        x_path.append(node[0])
        y_path.append(node[1])

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

        return x_path, y_path, edge_weights, vertex_weights

    #Returns passage time from self.startnode 
    #to the boundary
    def PassageTimeToBoundary(self):
        """
        Compute the passage time from the start node to the boundary, and return the minimum value and coordinates.
        """

        # Initialize the minimum passage time and coordinates
        passage_time_to_boundary = sys.maxsize
        min_coordinates = (0,0)
        for w in range(self.graph.width):
            if passage_time_to_boundary > self.distance_field_list[0][w]:
                passage_time_to_boundary = self.distance_field_list[0][w]
                min_coordinates = (w,0)
            
            if passage_time_to_boundary > self.distance_field_list[self.graph.height - 1][w]:
                passage_time_to_boundary = self.distance_field_list[self.graph.height - 1][w]
                min_coordinates = (w,self.graph.height-1)
        for h in range(self.graph.height):
            if passage_time_to_boundary > self.distance_field_list[h][0]:
                passage_time_to_boundary = self.distance_field_list[h][0]
                min_coordinates = (0,h)
            if passage_time_to_boundary > self.distance_field_list[h][self.graph.width - 1]:
                passage_time_to_boundary = self.distance_field_list[h][self.graph.width - 1]
                min_coordinates = (self.graph.width-1,h)
                 
        return passage_time_to_boundary , min_coordinates
        
             
            
            
            
            
        
