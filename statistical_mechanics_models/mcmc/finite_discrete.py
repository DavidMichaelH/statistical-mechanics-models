from simple_metropolis import SimpleMetropolis
import random


class FiniteDiscrete(SimpleMetropolis):

    def __init__(self, _vals=[], _probs=[]):
        self.probOfChange = 0.25
        self.probabilities = _probs
        self.values = _vals

    def MarkovKernel(self, x_curr, x_next):
        x_curr_index = self.values.index(x_curr)
        if 0 < x_curr_index < len(self.probabilities) - 1:
            if x_curr == x_next:
                return 1 - self.probOfChange
            else:
                return self.probOfChange / 2.0

        if x_curr == x_next:
            return 1 - self.probOfChange / 2.0
        else:
            return self.probOfChange / 2.0

    def TargetDist(self, x):
        x_index = self.values.index(x)
        return self.probabilities[x_index]

    def UpdateProcess(self, val):
        x_index = self.values.index(val)
        if random.uniform(0, 1) < self.probOfChange:
            x_index += 1 if random.uniform(0, 1) < 0.5 else -1
            x_index = max(x_index, 0)
            x_index = min(x_index, len(self.probabilities) - 1)
            return self.values[x_index]
        else:
            return val

    def Propose(self, x):
        return self.UpdateProcess(x)
