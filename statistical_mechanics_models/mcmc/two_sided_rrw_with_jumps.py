# -*- coding: utf-8 -*-
from special_mixed_density import SpecialMixedDensity
import random 
from abc import abstractmethod 
#RRW = Reflecting Random Walk Model with Jumps
class TwoSidedRrwWithJumps(SpecialMixedDensity):

    
    def __init__(self,a = 1, b = 2):
        super().__init__()
        self.RelativeStepSize = 0.1
        self.A = a
        self.B = b
        self.alphaA = 0.25
        self.alphaB = 0.15
        
        
    @property
    def A(self):
        return self._A
       

    @A.setter
    def A(self,value):
        self._A = value 
        self.u = self.RelativeStepSize*(self.B -self.A)
        
    @property
    def B(self):
        return self._A
       

    @B.setter
    def B(self,value):
        self._B = value 
        self.u = self.RelativeStepSize*(self.B -self.A)
        
            
        
    def Propose(self,x):
        return self.UpdateProcess(x)
        
     
    def Gstar(self,x_curr,x_next):
        #First we need to see how close we are to the boundary 
        
        if x_next < self.A or x_next > self.B:
            return 0.0
        
        #Interior Case 
        if x_curr > self.A + self.u and x_curr < self.B - self.u:
            if x_next > x_curr - self.u and x_next < x_curr + self.u:
                return 0.5/self.u
            else:
                return 0.0 
            
        #Bottom Boundary Case 
        if x_curr -self.u < self.A:
            if x_next < 2*self.A + self.u - x_curr:
                return 1/self.u
            else:
                return 0.5/self.u
            
        #Top Boundary Case 
        if x_curr + self.u > self.B:
            if x_next < 2*self.B - self.u - x_curr:
                return 0.5/self.u
            else:
                return 1/self.u
            
    def Alpha(self,x):
        if self.B == self.A:
            return self.alphaA 
        val = (self.alphaB - self.alphaA)*(x - self.A)/(self.B-self.A) + self.alphaA 
        return val
        
         
    
    def ReturnDist(self,x):
        if x >= self.A and x <= self.B:
            return 1/(self.B-self.A)
        return 0
    
    
    
    @abstractmethod
    def TargetCntsPart(self,x):
        raise NotImplementedError('Method not yet implemented')
    
     
  
    #Process information
     
    
    def ReturnDistribution(self):
        return random.uniform(self.A,self.B)
    
    
    #This is the update rule for g* 
    def UpdatePositivePart(self,x):
        y = x+ random.uniform(-self.u,self.u)
        
        #Check if you are in bounds 
        if y <= self.B and y > self.A :
            return y
        
        #If we you went over top boundary reflect down
        if y > self.B:
            return 2*self.B - y
        
        
        #If we you went below the boundary reflect up
        if y < self.A:
            return 2*self.A - y
        
     
    
    
    
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
             
        
