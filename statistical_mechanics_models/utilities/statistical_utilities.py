# -*- coding: utf-8 -*-

class StatisticalUtilities:
    
    
    #Maybe sort the 
    def NumberOfValuesInListLargerThanX(LIST,X, strictlyLarger = True ):
        counter = 0;
        if strictlyLarger:
            for itr in range(len(LIST)):
                if LIST[itr] > X:
                    counter += 1
        else:
            for itr in range(len(LIST)):
                if LIST[itr] >= X:
                    counter += 1
                    
        return counter
                    
            
    
    #Maybe sort the 
    def EmpericalEdgeWeightDistribution(path):
        pass
    