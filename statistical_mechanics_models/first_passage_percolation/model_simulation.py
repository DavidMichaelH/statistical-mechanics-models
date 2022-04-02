# -*- coding: utf-8 -*-
"""
This is where you define the graph and model for the weights
"""

from square_lattice import SquareLattice
from fpp import FPP
import random
import math
import matplotlib.pyplot as plt

#Define the lattice, in this case we will use the square lattice
height = 100
width = 100
mySquareLattice = SquareLattice()
mySquareLattice.CreateSquareLattice(height, width)
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

def MyEdgeWeight():
    return Bernoulli()


## here we define the model by setting edge weights to simulate and i.i.d.
# edge weight assignment being careful to note that the graph maintains 
# a directed set of edges and so both directions should record equal value 

# Non-Boundary (Interior) Case
for w in range(0,width-1):
    for h in range(0,height-1):
        weight = MyEdgeWeight()
        mySquareLattice.SetEdgeWeight((w,h), (w+1,h), weight)
        mySquareLattice.SetEdgeWeight((w+1,h), (w,h), weight)
        
        weight = MyEdgeWeight()
        mySquareLattice.SetEdgeWeight((w,h), (w,h+1), weight)
        mySquareLattice.SetEdgeWeight((w,h+1), (w,h), weight)

# Boundary (horizontal)
for w in range(0,width-1):
    weight = MyEdgeWeight()
    mySquareLattice.SetEdgeWeight((w,height-1), (w+1,height-1), weight)
    mySquareLattice.SetEdgeWeight((w+1,height-1),(w,height-1), weight)
    
    
    
# Boundary (Vertical)
for h in range(0,height-1):
    weight = MyEdgeWeight()
    mySquareLattice.SetEdgeWeight((width-1,h), (width-1,h+1), weight)
    mySquareLattice.SetEdgeWeight((width-1,h+1),(width-1,h), weight)


START_NODE = (width//2,height//2)
myFppModel = FPP(mySquareLattice,start_node = START_NODE)
shortest_path_field = myFppModel.ComputeDistanceField()



passageTime , TARGET_NODE = myFppModel.PassageTimeToBoundary()
print("Passage time = " + str(passageTime))
   
Geodesic = myFppModel.ComputeGeodesic(TARGET_NODE)
  

plt.imshow( shortest_path_field, cmap='hot', interpolation='nearest' )


plt.plot(Geodesic[0], Geodesic[1],color='green', linewidth = 0.5,
             marker='o', markerfacecolor='blue', markersize=1)





