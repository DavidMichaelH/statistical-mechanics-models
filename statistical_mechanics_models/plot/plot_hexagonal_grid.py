import matplotlib.pyplot as plt
import math
import matplotlib as mpl
import matplotlib.cm as cm
import sys


class HexPlot:

    def __init__(self):
        self.plt = plt

    def gen_hex_corners(self, center=(0, 0)):
        X = []
        Y = []
        for k in range(0, 6):
            X.append(center[0] + math.cos(k * math.pi / 3) / (2 * math.cos(math.pi / 6)))
            Y.append(center[1] + math.sin(k * math.pi / 3) / (2 * math.cos(math.pi / 6)))

        return X, Y

    def plot_hexagon(self, center=(0, 0), hexagon_face_color='lightsalmon', edgecolor=None):
        if edgecolor is None:
            edgecolor = hexagon_face_color
        X, Y = self.gen_hex_corners(center)
        self.plt.fill(X, Y, facecolor=hexagon_face_color, edgecolor=edgecolor, linewidth=0.1)

    def show(self):
        self.plt.axis('equal')
        self.plt.show()

    def plot_hexagonal_grid(self, field, use_binary_color=False, color_thresh=0, binaryColors=["blue", "red"],
                            continuousColor="hot"):

        if use_binary_color:
            color_field = self.compute_binary_color_field(field, colorThresh=color_thresh, colors=binaryColors)
        else:
            color_field = self.compute_color_field(field, color_map=continuousColor)

        wDim = len(color_field[0])
        hDim = len(color_field)

        if max(wDim, hDim) < 125:
            edgecolor = 'blue'
        else:
            edgecolor = None

        for x in range(wDim):
            for y in range(hDim):
                # Compute the correct centers
                center = self.compute_center_of_hexagon(x, y)
                self.plot_hexagon(center=(center[0][0], center[1][0]), hexagon_face_color=color_field[y][x],
                                  edgecolor=edgecolor)

    def compute_center_of_hexagon(self, X, Y):

        hex_center_x = []
        hex_center_y = []
        if type(X) is not list:
            w = X * math.cos(math.pi / 6)
            h = Y if X % 2 == 0 else Y + math.sin(math.pi / 6)
            hex_center_x.append(w)
            hex_center_y.append(h)
            return hex_center_x, hex_center_y

        for i in range(len(X)):
            w = X[i] * math.cos(math.pi / 6)
            h = Y[i] if X[i] % 2 == 0 else Y[i] + math.sin(math.pi / 6)
            hex_center_x.append(w)
            hex_center_y.append(h)

        return hex_center_x, hex_center_y

    def compute_color_field(self, field, color_map="hot"):

        width = len(field[0])
        height = len(field)

        max_val = -sys.maxsize
        min_val = sys.maxsize

        # First scan to find min and max
        for x in range(width):
            for y in range(height):
                if max_val < field[y][x]:
                    max_val = field[y][x]
                if min_val > field[y][x]:
                    min_val = field[y][x]

        norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val)

        try:
            cmap = cm.get_cmap(color_map)
        except:
            cmap = cm.hot

        m = cm.ScalarMappable(norm=norm, cmap=cmap)

        color_field = [[(0, 0, 0, 0)] * width for i in range(height)]

        # First scan to find min an max
        for x in range(width):
            for y in range(height):
                color_field[y][x] = m.to_rgba(field[y][x])

        return color_field

    def compute_binary_color_field(self, field, colors=["blue", "red"], colorThresh=0):

        width = len(field[0])
        height = len(field)

        color_field = [[colors[0]] * width for i in range(height)]

        # First scan to find min an max
        for x in range(width):
            for y in range(height):
                color_field[y][x] = colors[0] if field[y][x] <= colorThresh else colors[1]

        return color_field

    def PlotPath(self, XY, distinguished_sites=None, linewidth=1, markersize=2, pathColor="green",
                 distinguishedColor="blue"):

        hex_xy = self.compute_center_of_hexagon(XY[0], XY[1])

        self.plt.plot(hex_xy[0], hex_xy[1], color=pathColor, linewidth=linewidth,
                      marker='o', markerfacecolor=pathColor, markersize=markersize)

        if distinguished_sites is not None:
            hexDist = self.compute_center_of_hexagon(distinguished_sites[0], distinguished_sites[1])

            for i in range(len(hexDist[0])):
                self.plt.plot(hexDist[0][i], hexDist[1][i], color=distinguishedColor, linewidth=2 * linewidth,
                              marker='o', markerfacecolor=distinguishedColor, markersize=2 * markersize)

    def PlotCircle(self, center=(0, 0), facecolor='lightsalmon', edgecolor='orangered'):
        self.plt.plot(center[0], center[1], markersize=1, marker='o', color=facecolor)

    def SaveFigure(self, directory_and_filename):
        # , bbox_inches='tight'
        self.plt.savefig(directory_and_filename)
