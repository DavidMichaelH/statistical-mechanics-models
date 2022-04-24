from abc import ABC, abstractmethod
import random


class MetropolisHastings(ABC):
 
          
    #Decided to accept or reject the value
    def AcceptReject(self,x_curr,x_next):
        return random.uniform(0.0, 1.0)<self.AcceptProb(x_curr,x_next)
    
    
        
    #Gets the next value given the current value using previous two methods. 
    def NextValue(self,current_val):
        proposed_val = self.Propose(current_val)
        if self.AcceptReject(current_val,proposed_val):
            return proposed_val
        else:
            return current_val
        
    @abstractmethod
    def AcceptProb(self,x_curr,x_next):
        raise NotImplementedError('Method not yet implemented')
        
        
    @abstractmethod
    def Propose(self,x):
        raise NotImplementedError('Method not yet implemented')
        
    