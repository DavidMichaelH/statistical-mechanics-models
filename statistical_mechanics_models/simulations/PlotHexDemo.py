from graphs.triangular_lattice import TriangularLattice
from first_passage_percolation.fpp import FPP
import random
import math
from plot.plot_hexagonal_grid import HexPlot
from datetime import datetime
from timeit import default_timer as timer

start = timer()



#Define the lattice, in this case we will use the square lattice
height = 100
width = 100
myTriangularLattice = TriangularLattice()
myTriangularLattice.create_lattice(height, width)
#So far a graph has been defined but has zero vertex/edge weights and 
#and only contains topological data  

def Bernoulli():
    return random.randrange(2)

def BernPareto():
    return random.randrange(2)*(random.paretovariate(1))

def Exp():
    return random.expovariate(5)

def Pareto():
    return random.paretovariate(1)


def ExpOverT():
    return random.randrange(2)/math.log(1/(random.uniform(0,1)))*random.randrange(2)

def MyVertexWeight():
    return Bernoulli()


## here we define the model by setting edge weights to simulate and i.i.d.
# edge weight assignment being careful to note that the graph maintains 
# a directed set of edges and so both directions should record equal value 

# Initialize vertices
for w in range(0, width):
    for h in range(0, height):
        myTriangularLattice.set_vertex_weight((w, h), MyVertexWeight())
        
for w in range(0, width):
    for h in range(0, height):
        myTriangularLattice.set_vertex_weight((w, h), MyVertexWeight())
        

# Setting all weight on the Vertical Boundaries to zero
for h in range(0,height-1):
    myTriangularLattice.set_vertex_weight((width - 1, h), 0)
    myTriangularLattice.set_vertex_weight((0, h), 0)

        
        
#Create a Triangular Lattice 

START_NODE = (0,height//2)
#START_NODE = (width//2,height//2)

myFppModel = FPP(myTriangularLattice,start_node = START_NODE)
shortest_path_field = myFppModel.compute_distance_field()

#passageTime , TARGET_NODE = myFppModel.passage_time_to_boundary()
#print("Passage time = " + str(passageTime))
TARGET_NODE = (width-1,height//2)

#passageTimeToBoundary , TARGET_NODE = myFppModel.passage_time_to_boundary()

Geodesic = myFppModel.compute_geodesic(TARGET_NODE)

 
hexPlot = HexPlot()
hexPlot.plot_hexagonal_grid(shortest_path_field, continuousColor="seismic")
hexPlot.PlotPath(Geodesic,pathColor="green",linewidth = 0.8,markersize=0.8)
now = datetime.now()
plotName =  "CoolPlot_" +   now.strftime("%H_%M_%S") + ".pdf"
directory = "C:/"
#hexPlot.SaveFigure(directory + plotName) #uncomment if you want to save
hexPlot.show()

end = timer()

duration = round(end - start)
print(f"Computation took {duration} seconds" )
