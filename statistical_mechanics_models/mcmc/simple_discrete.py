from abc import abstractmethod 
from metropolis_hastings import MetropolisHastings
 
class SimpleDiscrete(MetropolisHastings):
    
    def __init__(self):
        self.Beta = 0.5
        self.ZeroProb = 0.5
        
    #MCMC Acceptance Probability 
    def AcceptProb(self,x_curr,x_next):
        if (x_curr==x_next):
            return 1;
        
    
        temp = self.TargetPMF(x_next)/self.TargetPMF(x_curr)
        temp = temp*self.MarkovKernel(x_next,x_curr)
        temp = temp/self.MarkovKernel(x_curr,x_next)
        temp = min(1,temp)
        return temp
        
        
    @abstractmethod
    def MarkovKernel(self,x_curr,x_next):
        raise NotImplementedError('Method not yet implemented')
        
        
    @abstractmethod
    def TargetPMF(self,x):
        raise NotImplementedError('Method not yet implemented')