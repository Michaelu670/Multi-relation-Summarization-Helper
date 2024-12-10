import numpy as np
from itertools import product


def calculate_cost(U, W, r_edges, total_edges):
    """
    Calculate the cost of a supernode pair (U, W) for a relation r.
    Args:
        U: Supernode U (list of node indices in U).
        W: Supernode W (list of node indices in W).
        r_edges: Set of edges present for relation r in the graph.
        total_edges: Total possible edges between U and W.

    Returns:
        Cost of the supernode pair for relation r.
    """
    actual_edges = r_edges.intersection(total_edges)
    possible_edges_count = len(total_edges)
    actual_edges_count = len(actual_edges)
    return min(possible_edges_count - actual_edges_count + 1, actual_edges_count)


def calculate_total_cost(U, relations):
    """
    Calculate the total cost of maintaining a supernode U across all relations.
    Args:
        U: Supernode U (list of node indices in U).
        adj_matrix: Adjacency matrix of the graph.
        relations: List of adjacency matrices for each relation.

    Returns:
        Total cost of the supernode.
    """
    total_cost = 0
    for r_idx, r_matrix in enumerate(relations):
        for neighbor_idx in range(len(r_matrix)):
            if any(r_matrix[u][neighbor_idx] > 0 for u in U):  # Check for edges in relation r
                total_edges = set(product(U, [neighbor_idx]))  # All possible edges between U and neighbor
                actual_edges = set((u, neighbor_idx) for u in U if r_matrix[u][neighbor_idx] > 0)
                total_cost += calculate_cost(U, [neighbor_idx], actual_edges, total_edges)
    return total_cost


def greedy_plus_algorithm(relations, supernodes, k):
    """
    Implement the Greedy+ algorithm.
    Args:
        adj_matrix: Adjacency matrix of the graph.
        relations: List of adjacency matrices for each relation.
        supernodes: Initial supernode partition (list of lists of node indices).

    Returns:
        Reduced set of supernodes after merging using the Greedy+ algorithm.
    """
    while True:
        best_merge = None
        best_cost_reduction = -1000000000

        # Iterate through all pairs of supernodes
        for i, U in enumerate(supernodes):
            for j, W in enumerate(supernodes):
                if i >= j:  # Avoid duplicate pairs and self-comparison
                    continue

                # Merge supernodes U and W
                H = U + W

                # Calculate cost reduction
                C_U = calculate_total_cost(U, relations)
                C_W = calculate_total_cost(W, relations)
                C_H = calculate_total_cost(H, relations)
                
                denominator = C_U + C_W
                if denominator != 0:
                    cost_reduction = (C_U + C_W - C_H) / denominator
                else:
                    cost_reduction = 0  # If the denominator is zero, no cost reduction
                
                
                # Update the best merge if cost reduction is better
                if cost_reduction > best_cost_reduction:
                    best_merge = (i, j)
                    best_cost_reduction = cost_reduction

        # Perform the best merge
        i, j = best_merge
        supernodes[i] += supernodes[j]  # Merge supernodes
        del supernodes[j]  # Remove the merged supernode

        if len(supernodes) == k:
            break

    return supernodes


# Example input
from dsurollback_cfg import adj_matrix as cfg
from dsurollback_pdg import adj_matrix as pdg
relations = [cfg, pdg]  
supernodes = [[i] for i in range(len(cfg))]  # Start with each node as its own supernode
k = 10

# Run the algorithm
result = greedy_plus_algorithm(relations, supernodes, k)

# Prettier print (1-indexing and sort)
result_1index = sorted([
    sorted([
        x+1 for x in y
    ]) 
    for y in result
])

print("Final supernodes:", result_1index)
