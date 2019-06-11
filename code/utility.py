import networkx as nx
import numpy as np
import operator
import random

#----------------------------degree seqeunce------------------------------------
# Return the degree sequence, format (dict): {node1: degree, node2: degree, ...}
def degree_sequence(G):
    sequence = dict()
    for node, degree in G.degree():
        sequence[node] = degree
    return sequence

#---------------------------random graph generator--------------------------
# Return a particular random graph
def construct_random_graph(type = "barabasi_c", n = 300, p = 40, m = 0.4):
    if type == "barabasi_c":
        return nx.powerlaw_cluster_graph(n, p, m)
    elif type == "barabasi":
        return nx.barabasi_albert_graph(n, p)
    elif type == "erdos":
        return nx.fast_gnp_random_graph(n, 0.3)
    else:
        raise ValueError('Unknown graph type!')


#-----------------------------Initial permuation matrix---------------------------

# Construct the initial similarity matrix
def initial_solution(g1, g2, node_list, r : "the perturbation probability"):
    dim = (len(g1), len(g2)) # dimeonsion of the permutation matrix
    pi = np.zeros(dim, np.int8) # the permutation matrix, initial entries are 0

    # Sort nodes by degrees in descending order. format : list of tuples with size 2
    sorted_ds_g1 = sorted(g1.degree(), key=operator.itemgetter(1), reverse=True)
    sorted_ds_g2 = sorted(g2.degree(), key=operator.itemgetter(1), reverse=True)

    # Adjacency matrix of two networks
    A1 = nx.to_numpy_matrix(g1, dtype = np.int8)
    A2 = nx.to_numpy_matrix(g2, node_list, dtype = np.int8) # the rows and columns are ordered according to the nodes in g1

    # Initial solution, the while loop is necessary here because we want to skip w.s.p
    i = 0
    while i < len(g1):
        # vertices with ith degree ranking in two graphs
        u1 = int(sorted_ds_g1[i][0])
        u2 = int(sorted_ds_g2[i][0])

        # Modified Big-Align Approach
        rand = random.uniform(0, 1)
        if rand >= r or i == 299:
            pi[u1, u2] = 1
        else:
            i += 1
            v1 = int(sorted_ds_g1[i][0])
            v2 = int(sorted_ds_g2[i][0])
            pi[u1, v2] = 1
            pi[v1, u2] = 1

        i += 1
    return pi
