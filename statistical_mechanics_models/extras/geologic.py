from graphs.square_lattice import SquareLattice
from first_passage_percolation.fpp import FPP
import random
import math
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.pyplot import figure
import matplotlib.image as mpimg


class GeoLogicPane:

    
    def __init__(self,file_path,nw_corner,se_corner):
        
        self.terrain_img = None
        
        self.terrain_increment_distance = 0.0005
        self.terrain_res = self.terrain_increment_distance
        self.terrain_heightmap = None 

        self.terrain_img_file_path = file_path 
        self.nw_corner = nw_corner
        self.se_corner = se_corner
        
        
        self.cartographic = None 
        self.cartographic_downsample = None 
        
        self.import_terrain_file(self.terrain_img_file_path)
        
                
        
    def rgb2gray(self,rgb):
        return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


    """
        Appears to have issues reading in jpg so we need 
        to convert to png using gimp or something
    """
    def import_terrain_file(self,file_path):
        self.terrain_img = mpimg.imread(file_path)  
        
        if len(self.terrain_img.shape) > 2:
            print(self.terrain_img)
            self.terrain_img = self.rgb2gray(self.terrain_img)    
        
        self.terrain_heightmap = self.terrain_img
        
        
    def display_terrain(self):
        plt.imshow(self.terrain_img)
        #plt.show()
        
        
    def subsample_terrain(self,sample_interval):
        self.terrain_heightmap = self.terrain_img[::sample_interval,::sample_interval]
        self.cartographic_downsample = self.cartographic[::sample_interval,::sample_interval,:]
        
    def get_terrain_shape(self):
        return self.terrain_heightmap.shape 
        
    
    def assign_cartographic(self,file_path):
        self.cartographic = mpimg.imread(file_path)  
        print(self.cartographic.shape)
    
    
        
class GeoLogic:

    
    def __init__(self,file_path,nw_corner,se_corner):
        
        self.geoLogicPane = GeoLogicPane(file_path,nw_corner,se_corner)
        
        self.pointA = None
        self.pointB = None
         
        
        self.distance_map = None 
        self.weight_map = None #square lattice 
        self.geoLogicFpp = None
        self.shortest_path_field = None 
        self.geodesic = None 
         
    def display_terrain(self):
        
        plt.imshow(self.geoLogicPane.terrain_heightmap,'magma')
               
        point = self.corrdinate_to_array(self.pointA)
        plt.scatter(point[0],point[1], s=20, c='r', marker='o')
        
        point = self.corrdinate_to_array(self.pointB)
        plt.scatter(point[0],point[1], s=20, c='b', marker='o')
        
 
    def geocorrdinate_to_index(self,cordinate,start_corrdinate,end_corrdinate,int_length):
        frac = (cordinate-start_corrdinate)/(end_corrdinate - start_corrdinate)
        index = int(frac*int_length)
        return index 
        
    def corrdinate_to_array(self,point):
        
        
        terrain_shape = self.geoLogicPane.get_terrain_shape()
        
        #x corresponds to lattitude
        pa = self.geoLogicPane.nw_corner[1]
        pb = self.geoLogicPane.se_corner[1]
        length = terrain_shape[0]
        index_x = self.geocorrdinate_to_index(point[1],pa,pb,length)
                
        #y corresponds to longitude 
                
        pa = self.geoLogicPane.nw_corner[0]
        pb = self.geoLogicPane.se_corner[0]
        length = terrain_shape[1]
        index_y = self.geocorrdinate_to_index(point[0],pa,pb,length)
        
        return (index_x,index_y)
    
    
    
    
    """
    we might choose to use different subsampling methods which do things like 
    maxpool or take averages. 
    """
    def subsample_terrain(self,sample_interval):
        self.geoLogicPane.subsample_terrain(sample_interval)
        
                
    
    def get_terrain_shape(self):
        return self.geoLogicPane.get_terrain_shape()
        
    def compute_weight_map(self):
        
        
        
        height = self.geoLogicPane.terrain_heightmap.shape[0]
        width = self.geoLogicPane.terrain_heightmap.shape[1] 
        
        self.weight_map = SquareLattice()
        self.weight_map.CreateLattice(height, width)
        
        
        for w in range(0, width):
            for h in range(0, height):
                node = (w, h)
                node_w = (w+1, h)
                node_h = (w, h+1)           
                
                if w+1 < width:
                    weight_w = self.compute_edge_weight(node,node_w)
                    self.weight_map.SetEdgeWeight(node,node_w, weight_w,directedEdge = False)
                
                if h+1 < height:
                    weight_h = self.compute_edge_weight(node,node_h)
                    self.weight_map.SetEdgeWeight(node,node_h, weight_h,directedEdge = False)
                    
                        
    
    def compute_edge_weight(self,node1,node2):
        edgeWeight = math.sqrt(self.geoLogicPane.terrain_res**2 + (self.geoLogicPane.terrain_heightmap[node1] - self.geoLogicPane.terrain_heightmap[node2])**2)
        return edgeWeight 
    
    
    def compute_distance_map(self):
        
        x = self.corrdinate_to_array(self.pointA)
        start_node = (x[1],x[0])
   
        self.geoLogicFpp = FPP(self.weight_map,start_node = start_node)
        self.shortest_path_field = self.geoLogicFpp.ComputeDistanceField()

        
    def show_distance_map(self):
        plt.imshow(self.shortest_path_field,'magma')
   
    def compute_geodesic(self):
        
        x = self.corrdinate_to_array(self.pointB)
        end_node = (x[1],x[0])

        self.geodesic = self.geoLogicFpp.ComputeGeodesic(end_node)

    def show_geodesic(self):
        plt.plot(self.geodesic[1],self.geodesic[0],"-r")
   
    def assign_cartographic(self,filepath):
        self.geoLogicPane.assign_cartographic(filepath)
        
    def show_cartographic(self):
        plt.imshow(self.geoLogicPane.cartographic_downsample)
