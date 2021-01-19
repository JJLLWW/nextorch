"""
nextorch.utils

Utility functions for Bayesian Optimization
"""

import numpy as np
import copy
import torch
from torch import Tensor 

from typing import Optional, TypeVar, Union, Tuple
# NEED TO EXPLAIN THESE IN DOCS
# Create a type variable for 1D arrays from numpy, np.ndarray
Array = TypeVar('Array')
# Create a type variable for 2D arrays from numpy, np.ndarray, and call it as a matrix
Matrix = TypeVar('Matrix')

# Create a type variable which is array like (1D) including list, array, 1d tensor
ArrayLike1d = Union[list, Array, Tensor]
# Create a type variable which is matrix like (2D) including matrix, tensor
MatrixLike2d = Union[Matrix, Tensor]

# use a GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
dtype = torch.float

#%% Scaling helper functions 
def unitscale_xv(xv: ArrayLike1d, xi_range: ArrayLike1d) -> ArrayLike1d:
    """
    Takes in an x array in a real scale
    and converts it to a unit scale

    Parameters
    ----------
    xv : ArrayLike1d
        original x array
    xi_range : ArrayLike1d
        range of x, [left bound, right bound]

    Returns
    -------
    xunit: ArrayLike1d, same type as xv
        normalized x in a unit scale
    """    
    xunit = copy.deepcopy(xv)
    lb = xi_range[0] #the left bound
    rb = xi_range[1] #the right bound
    xunit = (xv - lb)/(rb - lb)
    
    return xunit

def unitscale_X(
    X: MatrixLike2d,  
    X_range: Optional[ArrayLike1d] = [], 
    log_flags: Optional[list] = [], 
    decimals: Optional[int] = None
) -> Matrix:
    """Takes in a matrix in a real scale
    and converts it into a unit scale

    Parameters
    ----------
    X : MatrixLike2d
        original matrix in a real scale
    X_range : Optional[array_like_1d], optional
        list of x ranges, by default []
    log_flags : Optional[list], optional
        list of boolean flags
        True: use the log scale on this dimensional
        False: use the normal scale 
        by default []
    decimals : Optional[int], optional
        Number of decimal places to keep
        by default None, i.e. no rounding up 

    Returns
    -------
    Xunit: numpy matrix
        matrix scaled to a unit scale
    """
     #If 1D, make it 2D a matrix
    if len(X.shape)<2:
        X = copy.deepcopy(X)
        X = np.array([X])
        
    dim = X.shape[1] #the number of column in X
    
    if X_range == []: X_range = [[0,1]] * dim
    else: X_range = np.transpose(X_range)
    
    if log_flags == []: log_flags = [False] * dim
    
    # Initialize with a zero matrix
    Xunit = np.zeros((X.shape[0], X.shape[1]))
    for i, xi in enumerate(np.transpose(X)):
        if log_flags[i]:
            Xunit[:,i] =  np.log10(unitscale_xv(xi, X_range[i]))
        else:
            Xunit[:,i] =  unitscale_xv(xi, X_range[i])
    
    # Round up if necessary
    if not decimals == None:
        Xunit = np.around(Xunit, decimals = decimals)  
    
    return Xunit


def inverse_unitscale_xv(xv: ArrayLike1d, xi_range: ArrayLike1d) -> ArrayLike1d:    
    """
    Takes in an x array in a unit scale
    and converts it to a real scale

    Parameters
    ----------
    xv : ArrayLike1d
        x array in a unit scale
    xi_range : ArrayLike1d
        range of x, [left bound, right bound]

    Returns
    -------
    xv: ArrayLike1d, same type as xv
        x in a real scale
    """ 
    xreal = copy.deepcopy(xv)
    lb = xi_range[0] #the left bound
    rb = xi_range[1] #the right bound
    xreal = lb + (rb-lb)*xv
    
    return xreal


def inverse_unitscale_X(
    X: MatrixLike2d, 
    X_range: Optional[ArrayLike1d]= [], 
    log_flags: Optional[list] = [], 
    decimals: Optional[int] = None
) -> Matrix:
    """Takes in a matrix in a unit scale
    and converts it into a real scale

    Parameters
    ----------
    X : MatrixLike2d
        original matrix in a unit scale
    X_range : Optional[array_like_1d], optional
        list of x ranges, by default []
    log_flags : Optional[list], optional
        list of boolean flags
        True: use the log scale on this dimensional
        False: use the normal scale 
        by default []
    decimals : Optional[int], optional
        Number of decimal places to keep
        by default None, i.e. no rounding up 

    Returns
    -------
    Xunit: numpy matrix
        matrix scaled to a real scale
    """
    if len(X.shape)<2:
        X = copy.deepcopy(X)
        X = np.array([X]) #If 1D, make it 2D array
    
    dim = X.shape[1]  #the number of column in X
    
    if X_range == []: X_range = [[0,1]] * dim
    else: X_range = np.transpose(X_range)
    
    if log_flags == []: log_flags = [False] * dim
    
    Xreal = np.zeros((X.shape[0], X.shape[1]))
    for i, xi in enumerate(np.transpose(X)):
        if log_flags[i]:
            Xreal[:,i] =  10**(inverse_unitscale_xv(xi, X_range[i]))
        else:
            Xreal[:,i] =  inverse_unitscale_xv(xi, X_range[i])

    # Round up if necessary
    if not decimals == None:
        Xreal = np.around(Xreal, decimals = decimals)  
    
    return Xreal


def standardize_X(
    X: MatrixLike2d, 
    X_mean: Optional[ArrayLike1d] = None, 
    X_std: Optional[ArrayLike1d] = None
) -> MatrixLike2d:
    """Takes in an array/matrix X 
    and returns the standardized data with zero mean and a unit variance

    Parameters
    ----------
    X : MatrixLike2d
        the original matrix or array
    X_mean : Optional[ArrayLike1d], optional
        same type as X
        mean of each column in X, 
        by default None, it will be computed here
    X_std : ArrayLike1d, optional
        same type as X
        stand deviation of each column in X, 
        by default None, it will be computed here

    Returns
    -------
    X_standard: MatrixLike2d, same type as X
        Standardized X matrix
    """    
    # Compute the mean and std if not provided
    if X_mean is None:
        X_mean = X.mean(axis = 0)
        X_std = X.std(axis = 0)
        
    return (X - X_mean) / X_std



def inverse_standardize_X(
    X: MatrixLike2d, 
    X_mean: ArrayLike1d, 
    X_std: ArrayLike1d
) -> MatrixLike2d:
    """Takes in an arrary/matrix/tensor X 
    and returns the data in the real scale

    Parameters
    ----------
    X : MatrixLike2d
        the original matrix or array
    X_mean : Optional[ArrayLike1d], optional
        same type as X
        mean of each column in X, 
        by default None, it will be computed here
    X_std : ArrayLike1d, optional
        same type as X
        stand deviation of each column in X, 
        by default None, it will be computed here

    Returns
    -------
    X_real: MatrixLike2d, same type as X
        in real scale
    """
    
    if isinstance(X, torch.Tensor):
        X_real = X * X_std +  X_mean
    else:
        X_real = np.multiply(X, X_std) +  X_mean # element by element multiplication
    
    return X_real
    
#%% 2-dimensional system specific functions
def create_2D_mesh(mesh_size = 41) -> Tuple[Matrix, Matrix, Matrix]:   
    """Create 2D mesh for testing

    Parameters
    ----------
    mesh_size : int, optional
        mesh size, by default 41

    Returns
    -------
    X_test, X1, X2: Tuple[Matrix, Matrix, Matrix]
        X1 and X2 used for for-loops
    """
    nx1, nx2 = (mesh_size, mesh_size)
    x1 = np.linspace(0, 1, nx1)
    x2 = np.linspace(0, 1, nx2)
    # Use Cartesian indexing, the matrix indexing is wrong
    X1, X2 = np.meshgrid(x1, x2,  indexing='xy') 
    
    X_test = []
    for i in range(nx1):
        for j in range(nx2):
            X_test.append([X1[i,j], X2[i,j]])
    
    X_test = np.array(X_test)
    
    return X_test, X1, X2

def transform_plot2D_X(X1: Matrix, X2: Matrix, X_range: Matrix
) -> Tuple[Matrix, Matrix]:
    """Transform X1 and X2 in unit scale to real scales for plotting

    Parameters
    ----------
    X1 : Matrix
        X for variable 1
    X2 : Matrix
        X for variable 2
    X_range : Matrix
        the ranges of two variables 

    Returns
    -------
    X1, X2: Tuple[Matrix, Matrix]
        X1, X2 in real units 
    """
    X_range = np.array(X_range).T
    X1 = inverse_unitscale_xv(X1, X_range[0])
    X2 = inverse_unitscale_xv(X2, X_range[1])
    
    return X1, X2
  
def transform_plot2D_Y(X: Tensor, X_mean: ArrayLike1d, X_std: ArrayLike1d, mesh_size: int
) -> Matrix:
    """takes in 1 column of tensor 
    convert to real units and return a 2D numpy array 

    Parameters
    ----------
    X : Tensor
        1d tensor
    X_mean : ArrayLike1d
        means 
    X_std : ArrayLike1d
        standard deviations
    mesh_size : int
        mesh size

    Returns
    -------
    X_plot2D: numpy matrix
        in real units for plotting
        
    """
    X = X.clone()
    # Inverse the standardization
    X_real = inverse_standardize_X(X, X_mean, X_std)

    # Convert to numpy for plotting
    X_plot2D = np.reshape(X_real.detach().numpy(), (mesh_size, mesh_size))
    
    return X_plot2D
    




