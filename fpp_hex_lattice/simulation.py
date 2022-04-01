

from triangular_lattice import TriangularLattice
from plot_hexagonal_grid import HexPlot 
from fpp import FPP
import random 
                          
  

height = 100
width = 100


field = [[0] * width for i in range(height)]
for x in range(width):
    for y in range(height):
     field[y][x] =  0 if random.uniform(0,1) < 0.5 else 1
     
#Create a Triangular Lattice 
START_NODE = (width//2,height//2)
myTriangularLattice = TriangularLattice()
myTriangularLattice.CreateTriangularLattice(field)
myFppModel = FPP(myTriangularLattice,start_node = START_NODE)
shortest_path_field = myFppModel.ComputeDistanceField()

passageTime , TARGET_NODE = myFppModel.PassageTimeToBoundary()
print("Passage time = " + str(passageTime))
   
Geodesic, NonZeroSite = myFppModel.ComputeGeodesic(TARGET_NODE)

 
hexPlot = HexPlot()
hexPlot.PlotHexagonalGrid(shortest_path_field,continuousColor="RdBu") 
hexPlot.PlotPath(Geodesic,DistinguishedSites=NonZeroSite,pathColor="black",distinguishedColor="green",linewidth = 0.8,markersize=0.8)
hexPlot.Show()   
   