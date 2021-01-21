import numpy as np # Matrix operations
import numpy.linalg as la # Get principal components
import pandas as pd # Open .csv files
import os # Path tools

dir = os.getcwd() + "\\data\\"

"""
get_cov
-------
Returns the covariance matrix for a folder .csv files

Parameters:
    - folder: The name (not the whole file path!) of the child folder of games to process.
    
Preconditions:
    - All .csv files in folder are 19x19 matrices
    - The first row and column of all .csv files contain the numbers 0-18 in order 
"""
def get_cov(folder):
    full_dir = dir + folder
    cov = np.zeros((361,361)) # Accumulator for covariance matrix

    files = os.listdir(full_dir)
    N = len(files)

    for i in range(N):
        fname = files[i]
        try:
            game = pd.read_csv(full_dir+"\\"+fname).values[:,1:] # Import board, remove first column
            game = np.reshape(game, (361,1))
            cov += game @ np.transpose(game) # Covariance in current file
        except pd.errors.EmptyDataError: # Delete empty matrices
            os.remove(full_dir+"\\"+fname)
    return cov / N

"""
cov_to_cor
----------
Returns the correlation matrix associated with a covariance matrix

Parameters:
    - cov: A 361x361 real matrix with positive diagonal entries
"""
def cov_to_cor(cov):
    cor = np.zeros((361,361))
    for i in range(361):
        for j in range(i+1):
            cor_ij = cov[i,j] / ((cov[i,i] * cov[j,j]) ** 0.5) # Divide by product of standard deviations
            cor[i,j] = cor_ij
            cor[j,i] = cor_ij
    return cor

"""
principal_components
--------------------
Returns the principal components of a covariance matrix
"""
def principal_components(cov):
    return la.eig(cov)[1]

generate_cov = False # Whether to compute covariance matrix anew or load from save

if generate_cov:
    cov_9d = get_cov("9d_csv_norm")
    cov_18k = get_cov("18k_csv_norm")

    frame_9d = pd.DataFrame(cov_9d)
    frame_18k = pd.DataFrame(cov_18k)

    frame_9d.to_csv(dir + "9d_cov_all_norm.csv")
    frame_18k.to_csv(dir + "18k_cov_all_norm.csv")
else:
    cov_9d = pd.read_csv(dir+"9d_cov_all_norm.csv").values[:,1:]
    cov_18k = pd.read_csv(dir+"18k_cov_all_norm.csv").values[:,1:]

cor_18k = cov_to_cor(cov_18k) # Correlation matrix of 18k dataset
cor_9d = cov_to_cor(cov_9d) # Correlation matrix of 9d dataset