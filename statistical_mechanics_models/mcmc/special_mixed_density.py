from abc import abstractmethod
from metropolis_hastings import MetropolisHastings
 
class SpecialMixedDensity(MetropolisHastings):
    
    def __init__(self):
        self.Beta = 0.5
        self.ZeroProb = 0.5
    
    #MCMC Acceptance Probability 
    def AcceptProb(self,x_curr,x_next):
        if (x_curr==x_next):
            return 1;
        
        if not (x_curr==0) and not (x_next==0):

            part1 = self.TargetCntsPart(x_next)/self.TargetCntsPart(x_curr)
            part2 = (1-self.Alpha(x_next))/(1-self.Alpha(x_curr))
            part3 = self.Gstar(x_next,x_curr)/self.Gstar(x_curr,x_next)
            part4= min(1,part1*part2*part3)
            return part4
        
        if not (x_curr==0) and (x_next==0):
            part1 = self.ZeroProb/self.Alpha(x_curr)
            part2 = (1-self.Beta)/(1-self.Beta)
            part3 = self.ReturnDist(x_curr)/self.TargetCntsPart(x_curr)
            part4= min(1,part1*part2*part3)
            return part4
            
        if (x_curr==0) and not (x_next==0):
            part1 = self.Alpha(x_next)/self.ZeroProb
            part2 = (1-self.ZeroProb)/(1-self.Beta)
            part3 = self.TargetCntsPart(x_next)/self.ReturnDist(x_next) 
            part4= min(1,part1*part2*part3)
            return part4
        
        
        
        
        
    @abstractmethod
    def Gstar(self,x_curr,x_next):
        raise NotImplementedError('Method not yet implemented')
        
    @abstractmethod
    def Alpha(self,x):
        raise NotImplementedError('Method not yet implemented')
        
        
    @abstractmethod
    def TargetCntsPart(self,x):
        raise NotImplementedError('Method not yet implemented')
        
        
    @abstractmethod
    def ReturnDist(self,x):
        raise NotImplementedError('Method not yet implemented')