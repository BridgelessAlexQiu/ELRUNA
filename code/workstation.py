import numpy as np
import networkx as nx
import random
import utility as uti
from collections import defaultdict
import cProfile
import math
import timeit

# ----------------------------------- #
#           Read the Network          #
# ----------------------------------- #
"""
Dataset: High Energy Physics - Theory collaboration network
Link: https://snap.stanford.edu/data/ca-HepTh.html
Nodes in largest CC: 8638
Edges in largest CC: 24827
"""

"""
Dataset: General Relativity and Quantum Cosmology collaboration network
Link: https://snap.stanford.edu/data/ca-GrQc.html
Nodes in largest CC: 4158
Edges in largest CC: 13428
"""

"""
	Dataset: Coauthorship network of scientists working on network theory and experiment
	Link: http://www-personal.umich.edu/~mejn/netdata/
	Nodes in largest CC: 379
	Edges in largest CC: 914
"""
g1 = nx.read_gml("dataset/newman_netscience.gml")

# ------------------------------------- #
#         Extract the Largest CC        #
# ------------------------------------- #
largest_cc = max(nx.connected_components(g1), key=len)
g1 = g1.subgraph(largest_cc)

# -------------------------------------------------------- #
#      Relabel the Network with Consecutive Integers       #
# -------------------------------------------------------- #
g1 = nx.convert_node_labels_to_integers(g1)

# --------------------------------------------- #
#                  Remove Loops                 #
# --------------------------------------------- #
g1.remove_edges_from(g1.selfloop_edges())

# ---------------------------------------------- #
#       Construct the Ground Truth Mapping       #
# ---------------------------------------------- #
g1_node_list = np.asarray(g1.nodes())
g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

# Construct the ground truth mapping
gt_mapping = dict()
for i in range(len(g1_node_list)):
        gt_mapping[g1_node_list[i]] = g2_node_list[i]

# Construct the ground truth inverse mapping
gt_inverse_mapping = dict()
for i in range(len(g2_node_list)):
    gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

# ------------------------------------------------- #
#          Construct the Isomorphic Network         #
# ------------------------------------------------- #
g2 = nx.relabel_nodes(g1, gt_mapping)

# -----------------------------------#
#         Adjacency Matrices         #
# -----------------------------------#
C = nx.to_numpy_matrix(g1, dtype = np.int64)
D = nx.to_numpy_matrix(g2, nodelist = g1_node_list, dtype = np.int64)

# ----------------------------------- #
#         Sizes of Two Networks       #
# ----------------------------------- #
g1_size = len(g1)
g2_size = len(g2)

# --------------------------- #
#        Max Iteration        #
# --------------------------- #
max_iter = nx.diameter(g1) - 1

# -------------------------------------- #
#             Degree Sequence            #
# -------------------------------------- #
g1_degree_sequence = [None] * g1_size
g2_degree_sequence = [None] * g2_size

for node in g1.nodes():
	g1_degree_sequence[node] = g1.degree(node)

for node in g2.nodes():
	g2_degree_sequence[node] = g2.degree(node)


# ------------------------------------------ #
#             Neighrbor Sequence             #
# ------------------------------------------ #
g1_neighbor_sequence = [None] * g1_size
g2_neighbor_sequence = [None] * g2_size

for node in g1.nodes():
	g1_neighbor_sequence[node] = list(g1.neighbors(node))

for node in g2.nodes():
	g2_neighbor_sequence[node] = list(g2.neighbors(node))


# ######################################################################### #
#                                   MAIN                                    #
# ######################################################################### #

# ----------------------------- # 
#   Initial Similarity Matrix   #
# ----------------------------- #
S_ini = [[min(g1_degree_sequence[i], g2_degree_sequence[u]) / max(g1_degree_sequence[i], g2_degree_sequence[u]) for u in range(g2_size)] for i in range(g1_size)]

# ----------------------------- # 
#     Initial Greedy Vector     #
# ----------------------------- #
b_g1_ini = [None] * (g1_size)
b_g2_ini = [None] * (g2_size)

for i in range(g1_size):
	b_g1_ini[i] = max(S_ini[i])
for u in range(g2_size):
	maxi = -2
	for i in range(g1_size):
		if S_ini[i][u] > maxi:
			maxi = S_ini[i][u]
	b_g2_ini[u] = maxi

# --------------------------- #
#     Start the Profiler      #
# --------------------------- #
pr = cProfile.Profile()
pr.enable()

# --------------- #
#  Funciton Call  #
# --------------- #

S = uti.initial_solution_enhanced(S_ini, b_g1_ini, b_g2_ini, g1, g2, g1_neighbor_sequence, g2_neighbor_sequence, g1_degree_sequence, g2_degree_sequence, g1_size, g2_size, max_iter)

# --------------------------- #
#      End the Profiler       #
# --------------------------- #
pr.disable()
pr.print_stats(sort='time')

# --------------------------------------- #
#       Extract the Mapping (Greedy)      #
# --------------------------------------- #

# The initial mapping
mapping = dict()
# Determine if an 
selected = [0] * (g2_size)

for i in range(g1_size):
	maxi = -2
	max_index = 0
	for u in range(g2_size):
		if S[i][u] > maxi and not selected[u]:
			maxi = S[i][u]
			max_index = u
	mapping[i] = max_index
	selected[max_index] = 1


# ------------------------------------ #
#      Initial Mapping Percentage      #
# ------------------------------------ #
matched_node = 0
for i in range(g1_size):
	if gt_mapping[i] == mapping[i]:
		matched_node += 1
print("Initial mapping percentage: {} (A percentage less than 1.0 does not necessarily indicate incorrect mappings)".format(matched_node / g1_size))

# --------------------------- #
#      Edge Correctness       #
# --------------------------- #
count = 0
s = set()       
for i1 in range(len(g1)):
	i2 = mapping[i1]
	for j1 in range(len(g1)):
		j2 = mapping[j1]
		if C[i1, j1] == 1:
			if D[i2, j2] == 0:
				count += 1
				s.add(i1)
				s.add(j1)
		if C[i1, j1] == 0:
			if D[i2, j2] == 1:
				count += 1
				s.add(i1)
				s.add(j1)
                
print("Initial violations: {} (0 violation indicates isomorphic mappings)".format(count/2))
