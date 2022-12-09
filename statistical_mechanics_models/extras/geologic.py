from graphs.square_lattice import SquareLattice
from first_passage_percolation.fpp import FPP
import numpy as np
import math
from PIL import Image
import requests
from io import BytesIO
from numpy import asarray
import matplotlib.pyplot as plt


class GeoLogicPane:

    def __init__(self, nw_corner):

        self.terrain_img = None

        self.terrain_increment_distance = 0.0005
        self.terrain_res = self.terrain_increment_distance
        self.terrain_heightmap = None

        self.nw_corner = nw_corner
        self.se_corner = (nw_corner[0] - 1, nw_corner[1] + 1)

        self.get_srtm_terrain_map_from_usgs(self.nw_corner)

    def rgb_2_gray(self, rgb):
        return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

    def display_terrain(self):
        plt.imshow(self.terrain_img)

    def subsample_terrain(self, sample_interval):
        self.terrain_heightmap = self.terrain_img[::sample_interval, ::sample_interval]

    def get_terrain_shape(self):
        return self.terrain_heightmap.shape

    def get_srtm_terrain_map_from_usgs(self, nw_corner):

        lat = abs(nw_corner[1])

        long_str = str(nw_corner[0] - 1)

        if lat < 100:
            lat_str = "0" + str(lat)
        else:
            lat_str = str(lat)

        url_ending = lat_str + "/n" + long_str + "_w" + lat_str + "_1arc_v3.jpg"

        url = f"https://ims.cr.usgs.gov/browse/srtm_v3/1arc/w" + url_ending

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        self.terrain_img = asarray(img) / 256.0


class GeoLogic:

    def __init__(self, nw_corner):

        self.geoLogicPane = GeoLogicPane(nw_corner)

        self.point_a = None
        self.point_b = None

        self.weight_map = None  # square lattice
        self.geoLogicFpp = None
        self.shortest_path_field = None
        self.geodesic = None

    def check_points_in_same_chunk(self, p, q):
        long = math.ceil(p[0])
        lat = math.floor(p[1])

        c1 = self.geoLogicPane.nw_corner == (long, lat)
        c2 = (int(p[0]) == int(q[0]))
        c3 = (int(p[1]) == int(q[1]))
        return c1 and c2 and c3

    def compute_geodesic_between_coordinates(self, p, q):

        if not self.check_points_in_same_chunk(p, q):
            print("The given points are invalid")
            return

        self.point_a = p
        self.point_b = q

        self.compute_weight_map()
        self.compute_distance_map()
        self.compute_geodesic()

    def display_terrain(self):

        plt.imshow(self.geoLogicPane.terrain_heightmap, 'magma')

        point = self.geocoordinate_to_indices(self.point_a)
        plt.scatter(point[0], point[1], s=20, c='r', marker='o')

        point = self.geocoordinate_to_indices(self.point_b)
        plt.scatter(point[0], point[1], s=20, c='b', marker='o')

    def geocoordinate_to_index(self, coordinate, start_coordinate, end_coordinate, int_length):
        frac = (coordinate - start_coordinate) / (end_coordinate - start_coordinate)
        index = int(frac * int_length)
        return index

    def index_to_geocoordinate(self, index, start_coordinate, end_coordinate, int_length):
        coordinate = start_coordinate + (end_coordinate - start_coordinate) * (index / int_length)
        return coordinate

    def geocoordinate_to_indices(self, point):

        terrain_shape = self.geoLogicPane.get_terrain_shape()

        # x corresponds to lattitude
        point_a = self.geoLogicPane.nw_corner[1]
        point_b = self.geoLogicPane.se_corner[1]
        length = terrain_shape[0]
        index_x = self.geocoordinate_to_index(point[1], point_a, point_b, length)

        # y corresponds to longitude

        point_a = self.geoLogicPane.nw_corner[0]
        point_b = self.geoLogicPane.se_corner[0]
        length = terrain_shape[1]
        index_y = self.geocoordinate_to_index(point[0], point_a, point_b, length)

        return (index_x, index_y)

    def indices_to_geocoordinate(self, indices):

        terrain_shape = self.geoLogicPane.get_terrain_shape()

        # x corresponds to lattitude
        point_a = self.geoLogicPane.nw_corner[1]
        point_b = self.geoLogicPane.se_corner[1]
        length = terrain_shape[0]
        geocoord_x = self.index_to_geocoordinate(indices[1], point_a, point_b, length)

        # y corresponds to longitude

        point_a = self.geoLogicPane.nw_corner[0]
        point_b = self.geoLogicPane.se_corner[0]
        length = terrain_shape[1]
        geocoord_y = self.index_to_geocoordinate(indices[0], point_a, point_b, length)

        return (geocoord_y, geocoord_x)

    def get_geodesic_as_geocoordinates(self):
        geocoordinates = []

        itr = 0

        while itr < len(self.geodesic[1]):
            i = self.geodesic[0][itr]
            j = self.geodesic[1][itr]
            geocoordinate = self.indices_to_geocoordinate((i, j))
            geocoordinates.append(geocoordinate)

            itr += 1
        return geocoordinates

    """"
    we might choose to use different subsampling methods which do things like 
    maxpool or take averages. 
    """

    def subsample_terrain(self, sample_interval):
        self.geoLogicPane.subsample_terrain(sample_interval)

    def get_terrain_shape(self):
        return self.geoLogicPane.get_terrain_shape()

    def compute_weight_map(self):

        height = self.geoLogicPane.terrain_heightmap.shape[0]
        width = self.geoLogicPane.terrain_heightmap.shape[1]

        self.weight_map = SquareLattice(height, width)

        for w in range(0, width):
            for h in range(0, height):
                node = (w, h)
                node_w = (w + 1, h)
                node_h = (w, h + 1)

                if w + 1 < width:
                    weight_w = self.compute_edge_weight(node, node_w)
                    self.weight_map.set_edge_weight(node, node_w, weight_w, directed_edge=False)

                if h + 1 < height:
                    weight_h = self.compute_edge_weight(node, node_h)
                    self.weight_map.set_edge_weight(node, node_h, weight_h, directed_edge=False)

    def compute_edge_weight(self, node1, node2):
        edge_weight = math.sqrt(self.geoLogicPane.terrain_res ** 2 + (
                    self.geoLogicPane.terrain_heightmap[node1] - self.geoLogicPane.terrain_heightmap[node2]) ** 2)
        return edge_weight

    def compute_distance_map(self):

        x = self.geocoordinate_to_indices(self.point_a)
        start_node = (x[1], x[0])

        self.geoLogicFpp = FPP(self.weight_map, start_node=start_node)
        self.shortest_path_field = self.geoLogicFpp.compute_distance_field()

    def show_distance_map(self):
        plt.imshow(self.shortest_path_field, 'magma')

    def compute_geodesic(self):

        x = self.geocoordinate_to_indices(self.point_b)
        end_node = (x[1], x[0])

        self.geodesic = self.geoLogicFpp.compute_geodesic(end_node)

    def show_geodesic(self):
        plt.plot(self.geodesic[1], self.geodesic[0], "-r")
