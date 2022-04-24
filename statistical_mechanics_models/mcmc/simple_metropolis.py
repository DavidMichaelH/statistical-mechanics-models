from abc import abstractmethod 
from metropolis_hastings import MetropolisHastings
 
class SimpleMetropolis(MetropolisHastings):
    
 
    #MCMC Acceptance Probability 
    def AcceptProb(self,x_curr,x_next):
        if (x_curr==x_next):
            return 1;
        
        temp = self.TargetDist(x_next)/self.TargetDist(x_curr)
        temp = temp*self.MarkovKernel(x_next,x_curr)
        temp = temp/self.MarkovKernel(x_curr,x_next)
        temp = min(1,temp)
        return temp
        
        
    @abstractmethod
    def MarkovKernel(self,x_curr,x_next):
        raise NotImplementedError('Method not yet implemented')
        
        
    @abstractmethod
    def TargetDist(self,x):
        raise NotImplementedError('Method not yet implemented')