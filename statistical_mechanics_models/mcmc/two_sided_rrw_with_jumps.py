# -*- coding: utf-8 -*-
from special_mixed_density import SpecialMixedDensity
import random 
from abc import abstractmethod 
#RRW = Reflecting Random Walk Model with Jumps
class TwoSidedRrwWithJumps(SpecialMixedDensity):

    
    def __init__(self,interval = (1 , 2) ):
        super().__init__()
        self.RelativeStepSize = 0.1
        self.interval = interval 

        self.alphaA = 0.25
        self.alphaB = 0.15
        
    @property
    def interval(self):
        return self._interval
       
    @interval.setter
    def interval(self,value):
        self._interval = value 
        self.u = self.RelativeStepSize*(self._interval[1] -self._interval[0])
        

            
        
    def Propose(self,x):
        return self.UpdateProcess(x)
        
     
    def Gstar(self,x_curr,x_next):
        #First we need to see how close we are to the boundary 
        
        if x_next < self.interval[0] or x_next > self.interval[1]:
            return 0.0
        
        #Interior Case 
        if x_curr > self.interval[0] + self.u and x_curr < self.interval[1] - self.u:
            if x_next > x_curr - self.u and x_next < x_curr + self.u:
                return 0.5/self.u
            else:
                return 0.0 
            
        #Bottom Boundary Case 
        if x_curr -self.u < self.interval[0]:
            if x_next < 2*self.interval[0] + self.u - x_curr:
                return 1/self.u
            else:
                return 0.5/self.u
            
        #Top Boundary Case 
        if x_curr + self.u > self.interval[1]:
            if x_next < 2*self.interval[1] - self.u - x_curr:
                return 0.5/self.u
            else:
                return 1/self.u
            
    def Alpha(self,x):

        val = (self.alphaB - self.alphaA)*(x - self.interval[0])/(self.interval[1]-self.interval[0]) + self.alphaA 
        return val
        
         
    
    def ReturnDist(self,x):
        if x >= self.interval[0]and x <= self.interval[1]:
            return 1/(self.interval[1]-self.interval[0])
        return 0
    
    
    
    @abstractmethod
    def TargetCntsPart(self,x):
        raise NotImplementedError('Method not yet implemented')
    
     
  
    #Process information
     
    
    def ReturnDistribution(self):
        return random.uniform(self.interval[0],self.interval[1])
    
    
    #This is the update rule for g* 
    def UpdatePositivePart(self,x):
        y = x+ random.uniform(-self.u,self.u)
        
        #Check if you are in bounds 
        if y <= self.interval[1] and y > self.interval[0]:
            return y
        
        #If we you went over top boundary reflect down
        if y > self.interval[1]:
            return 2*self.interval[1] - y
        
        
        #If we you went below the boundary reflect up
        if y < self.interval[0]:
            return 2*self.interval[0]- y
        
     
    
    
    
    def UpdateProcess(self,val):
        
        #If val == 0
        if val == 0:
            if random.uniform(0, 1) < self.Beta:
                return 0 
            else:
                return self.ReturnDistribution()
            
        #If you are here then val > 0 
        if random.uniform(0, 1) < self.Alpha(val):
            return 0 
        else:
            return self.UpdatePositivePart(val)
             
        
