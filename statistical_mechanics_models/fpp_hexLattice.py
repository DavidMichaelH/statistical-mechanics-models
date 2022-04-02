from graphs.triangularLattice import TriangularLattice
from first_passage_percolation.fpp import FPP
import random
import math
from plot.PlotHexagonalGrid import HexPlot

#Define the lattice, in this case we will use the square lattice
height = 100
width = 100
myTriangularLattice = TriangularLattice()
myTriangularLattice.CreateLattice(height, width)
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
    return random.randrange(2)/math.log(1/(random.uniform(0,1)))

def MyVertexWeight():
    return Bernoulli()


## here we define the model by setting edge weights to simulate and i.i.d.
# edge weight assignment being careful to note that the graph maintains 
# a directed set of edges and so both directions should record equal value 

# Initialize vertices
for w in range(0, width):
    for h in range(0, height):
        myTriangularLattice.SetVertexWeight((w, h), MyVertexWeight())
        
        
        
#Create a Triangular Lattice 
START_NODE = (width//2,height//2)

myFppModel = FPP(myTriangularLattice,start_node = START_NODE)
shortest_path_field = myFppModel.ComputeDistanceField()

passageTime , TARGET_NODE = myFppModel.PassageTimeToBoundary()
print("Passage time = " + str(passageTime))
   
Geodesic = myFppModel.ComputeGeodesic(TARGET_NODE)

 
hexPlot = HexPlot()
hexPlot.PlotHexagonalGrid(shortest_path_field,continuousColor="RdBu") 
hexPlot.PlotPath(Geodesic,pathColor="green",linewidth = 0.8,markersize=0.8)
hexPlot.Show()   
   