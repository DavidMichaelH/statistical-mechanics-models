from abc import ABC, abstractmethod
import random


class MetropolisHastings(ABC):

    def AcceptReject(self, x_curr, x_next):
        return random.uniform(0.0, 1.0) < self.AcceptProb(x_curr, x_next)

    def NextValue(self, current_val):
        proposed_val = self.Propose(current_val)
        if self.AcceptReject(current_val, proposed_val):
            return proposed_val
        else:
            return current_val

    @abstractmethod
    def AcceptProb(self, x_curr, x_next):
        raise NotImplementedError('Method not yet implemented')

    @abstractmethod
    def Propose(self, x):
        raise NotImplementedError('Method not yet implemented')
