import numpy as np
import networkx as nx
import random
import utility as uti
from collections import defaultdict
import cProfile
import math

"""
Several notes when two real networks of different sizes are used:
	1. Indexing - node id to index start from 0
	2. Diameter
	3. Should map smaller network to larger network
"""

# -----------------------#
#       Parameteres      #
# -----------------------#
d_replace = 2
network_size = 100

#------------------------------------------------#
#              Example Random Graph              #
#------------------------------------------------#
g1 = uti.construct_random_graph("barabasi_c", n = network_size)

# NOTE: UPDATE NEEDED HERE: For real networks, max_iter should be equal to the larger diameter - 1
max_iter = nx.diameter(g1) - 1

# -----------------------------------------------------------#
#             Construct the Ground Truth Mapping             #
# -----------------------------------------------------------#
g1_node_list = np.asarray(g1.nodes()) # list of node ids, starts from 0
g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

# Construct the ground truth mapping
gt_mapping = dict()
for i in range(len(g1_node_list)):
        gt_mapping[g1_node_list[i]] = g2_node_list[i]

# Construct the ground truth inverse mapping
gt_inverse_mapping = dict()
for i in range(len(g2_node_list)):
    gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

# ------------------------------------- #
#    Construct the Isomorphic Graph     #
# ------------------------------------- #
g2 = nx.relabel_nodes(g1, gt_mapping)

# sizes of two networks
g1_size = len(g1)
g2_size = len(g2)

# -----------------------------------#
#         Adjacency Matrices         #
# -----------------------------------#
C = nx.to_scipy_sparse_matrix(g1, dtype = np.int64)
D = nx.to_scipy_sparse_matrix(g2, nodelist = g1_node_list, dtype = np.int64)

# ######################################################################### #
#                                   MAIN                                    #
# ######################################################################### #

# The initial mapping
mapping = dict()
# Determine if an 
selected = [0] * (g2_size)

# ----------------------------- # 
#   Initial Similarity Matrix   #
# ----------------------------- #
S_ini = [[min(g1.degree(i), g2.degree(u)) / max(g1.degree(i), g2.degree(u)) for u in range(g2_size)] for i in range(g1_size)]

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
S = uti.initial_solution_enhanced(S_ini, b_g1_ini, b_g2_ini, g1, g2, max_iter)
# S = uti.IsoRank(C, D, tol = 0.000005, max_iter = 500, H = None)

# --------------------------- #
#      End the Profiler       #
# --------------------------- #
pr.disable()
pr.print_stats(sort='time')

# --------------------------------------- #
#       Extract the Mapping (Greedy)      #
# --------------------------------------- #
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

# ---------------------------- #
#      Initial Violation       #
# ---------------------------- #
count = 0
for i1 in range(len(g1)):
	for j1 in range(len(g1)):
		i2 = mapping[i1]
		j2 = mapping[j1]
		if C[i1, j1] == 1:
			if D[i2, j2] == d_replace:
				count += 1
		if C[i1, j1] == 0:
			if D[i2, j2] == 1:
				count += 1
print("Initial violations: {} (0 violation indicates isomorphic mappings)".format(count))
