import matplotlib.pyplot as plt
import math
import matplotlib as mpl
import matplotlib.cm as cm
import sys
 
class HexPlot:
    
    def __init__(self):
        self.plt = plt 
        
        
        
     
    def GenHexCorners(self, center = (0,0)):
        X = []
        Y = []
        for k in range(0,6):
            X.append(center[0]+math.cos(k*math.pi/3)/(2*math.cos(math.pi/6)))
            Y.append(center[1]+math.sin(k*math.pi/3)/(2*math.cos(math.pi/6)))
            
        return X,Y 
  
    
    def PlotHexagon(self,center = (0,0),facecolor='lightsalmon', edgecolor=None):
        if edgecolor is None:
            edgecolor = facecolor
        X,Y = self.GenHexCorners(center)
        self.plt.fill(X, Y,facecolor = facecolor, edgecolor = edgecolor, linewidth=0.1)
        #plt.fill(X, Y,facecolor='blue', edgecolor='purple', linewidth=3)
        
    def Show(self):
        self.plt.axis('equal')
        self.plt.show()
        
    
    
    def PlotHexagonalGrid(self,field,useBinaryColor = False,colorThresh = 0, binaryColors = ["blue","red"],continuousColor = "hot"):
    
         
        if useBinaryColor:
            COLOR_FIELD = self.ComputeBinaryColorField(field,colorThresh = colorThresh,colors = binaryColors)
        else:
            COLOR_FIELD = self.ComputeColorField(field,colorMap=continuousColor)
            

        wDim = len(COLOR_FIELD[:][0])
        hDim = len(COLOR_FIELD[0]) 
  
        if max(wDim,hDim) < 125:
            edgecolor='blue'
        else:
            edgecolor=None
        
        
        for x in range(wDim):
            for y in range(hDim):
                #Compute the correct centers
                center = self.ComputeCenterOfHexagon(x,y)
                self.PlotHexagon(center = (center[0][0],center[1][0]),facecolor=COLOR_FIELD[y][x], edgecolor=edgecolor)

        
        
    def ComputeCenterOfHexagon(self,X,Y):

        hexCenterX = []
        hexCenterY = []
        if type(X) is not list:
            w = X*math.cos(math.pi/6)
            h = Y if X%2==0 else Y + math.sin(math.pi/6)
            hexCenterX.append(w)
            hexCenterY.append(h)
            return (hexCenterX,hexCenterY)
        
        
        for i in range(len(X)):
            w = X[i]*math.cos(math.pi/6)
            h = Y[i] if X[i]%2==0 else Y[i] + math.sin(math.pi/6)
            hexCenterX.append(w)
            hexCenterY.append(h)
            
        return (hexCenterX,hexCenterY)
    
    def ComputeColorField(self,field,colorMap = "hot"):
        
   
        
        width = len(field[:][0])
        height = len(field[0]) 
        
        
        MAX_VAL = -sys.maxsize
        MIN_VAL = sys.maxsize
        
             
        # First scan to find min an max
        for x in range(width):
            for y in range(height):
             if MAX_VAL < field[y][x] :
                 MAX_VAL = field[y][x] 
             if MIN_VAL > field[y][x] :
                 MIN_VAL = field[y][x] 
 
        norm = mpl.colors.Normalize(vmin=MIN_VAL, vmax=MAX_VAL)
        
        
        
        if colorMap == "RdBu":
            cmap = cm.RdBu
        elif colorMap == "coolwarm":
            cmap = cm.coolwarm
        elif colorMap == "viridis":
            cmap = cm.viridis
        elif colorMap == "cool":
            cmap = cm.cool
        elif colorMap == "copper":
            cmap = cm.copper
        else:
            cmap = cm.hot
        
        
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        
        COLOR_FIELD = [[(0,0,0,0)]* width for i in range(height)]
             
        # First scan to find min an max
        for x in range(width):
            for y in range(height):
             COLOR_FIELD[y][x] = m.to_rgba(field[y][x])
            
            
        
        
        return COLOR_FIELD
    
    
    def ComputeBinaryColorField(self,field, colors = ["blue","red"] , colorThresh = 0):
         
  
        width = len(field[:][0])
        height = len(field[0]) 
        
 
        COLOR_FIELD = [[colors[0]]* width for i in range(height)]
             
        # First scan to find min an max
        for x in range(width):
            for y in range(height):
             COLOR_FIELD[y][x] = colors[0] if field[y][x] <= colorThresh else colors[1]
        
        return COLOR_FIELD
    
    def PlotPath(self,XY,DistinguishedSites = None,linewidth = 1,markersize=2,pathColor="green",distinguishedColor ="blue"):
                
        hexXY = self.ComputeCenterOfHexagon(XY[0],XY[1])
         
        self.plt.plot(hexXY[0], hexXY[1],color=pathColor, linewidth = linewidth,
             marker='o', markerfacecolor=pathColor, markersize=markersize)
        
        if DistinguishedSites is not None:
            hexDist = self.ComputeCenterOfHexagon(DistinguishedSites[0],DistinguishedSites[1])
            
            for i in range(len(hexDist[0])):
                self.plt.plot(hexDist[0][i], hexDist[1][i],color=distinguishedColor, linewidth = 2*linewidth,
                          marker='o', markerfacecolor=distinguishedColor, markersize=2*markersize)
        
    def PlotCircle(self,center = (0,0),facecolor='lightsalmon', edgecolor='orangered'):
        self.plt.plot(center[0],center[1], markersize = 1,marker='o', color=facecolor)
         


        