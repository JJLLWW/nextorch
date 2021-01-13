import pyDOE2 as DOE 
import numpy as np
import utils as ut

def factorial(levels, DOE_function = DOE.fullfact):
    '''
    levels - a list of integers, design levels
    DOE_function - pyDOE function, general full-factorial by default
    Return normalized sampling plan given a DOE function
    '''
    X_real = DOE_function(levels)
    #Normailize X_real
    X_ranges = np.transpose([[0, i-1] for i in levels]) #-1 for python index
    X_norm = ut.norm_X(X_real, X_range = X_ranges)
    
    return X_norm

def lhs(dim, n_points):
    """[summary]

    Parameters
    ----------
    dim : [type]
        [description]
    n_points : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    Xlhc = DOE.lhs(dim, samples = n_points)
    return Xlhc


def random():

    pass

def random_distribution():
    pass




'''
Other designs such as:
- Fractional-Factorial
- Plackett-Burman
- Box-Behnken designs
- Central composite designs
can be generated by pyDOE2 and hence used by nextorch
'''

