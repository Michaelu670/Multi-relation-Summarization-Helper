import numpy as np
import random
from pyclustering.cluster.kmedians import kmedians
from pyclustering.utils.metric import distance_metric, type_metric


def get_random_initial_medians(matrix, k):
    """
    Selects k random rows from the adjacency matrix as initial medians.
    
    Args:
        matrix (np.ndarray): The adjacency matrix.
        k (int): The number of initial medians to select.
        
    Returns:
        list: A list of k rows from the matrix representing the initial medians.
    """
    if k > len(matrix):
        raise ValueError("k cannot be greater than the number of rows in the matrix.")
    
    # Randomly choose k distinct row indices
    selected_indices = random.sample(range(len(matrix)), k)
    
    # Extract the selected rows
    initial_medians = [matrix[idx] for idx in selected_indices]
    
    return initial_medians


def one_kmedian(matrix, k):
    initial_medians = get_random_initial_medians(matrix, k)

    # Create a kmedians instance with L1/L2 distance
    metric = distance_metric(type_metric.EUCLIDEAN)
    kmedians_instance = kmedians(matrix.tolist(), initial_medians, metric=metric)

    # Perform clustering
    kmedians_instance.process()

    return kmedians_instance

    

def multiple_kmedian(matrix, k, rep=10):
    best_run = one_kmedian(matrix, k)
    
    for i in range(rep-1):
        run = one_kmedian(matrix, k)
        if run.get_total_wce() < best_run.get_total_wce():
            best_run = run

    clusters = best_run.get_clusters()
    medians = best_run.get_medians()
    score = best_run.get_total_wce()

    # Prettier print (1-indexing and sort)
    clusters_1index = sorted([
        sorted([
            x+1 for x in y
        ]) 
        for y in clusters
    ])

    # Print results
    print("Clusters:", clusters_1index)
    print("Medians:", medians)
    print("Score:", score)


#CHANGEME
from dsurollback import adj_matrix 
k = 3
run = 100

multiple_kmedian(adj_matrix, k, run)