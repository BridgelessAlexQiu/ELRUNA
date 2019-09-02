import numpy as np
import networkx as nx
import random
import utility as uti
import cProfile
import timeit
import math
from docplex.mp.constants import ComparisonType
from docplex.mp.model import Model
from collections import defaultdict
import matplotlib.pyplot as plt
import itertools

# --------------------------------------------- Initial Solution -------------------------------------------------#

# ------------------------------------------------ #
#                 Read in G1 and G2                #
# ------------------------------------------------ #
g1 = nx.read_edgelist("networks/random_networks/barabasi/edgelist/barabasi_g1.edgelist", nodetype = int)
g2 = nx.read_edgelist('networks/random_networks/barabasi/edgelist/barabasi_0.009_g2.edgelist', nodetype = int)
# g2_original_network = nx.read_edgelist('g2_original_network.edgelist', nodetype = int)


g1_node_list = np.asarray(g1.nodes())
g2_node_list = np.asarray(g2.nodes())

# ---------------------------------------------- #
#       Construct the Ground Truth Mapping       #
# ---------------------------------------------- #
# gt_mapping_file = open("gt_mapping.txt", 'r')

# # Construct the ground truth mapping
# gt_mapping = dict()
# for line in gt_mapping_file:
# 	i = line.split(' ')[0]
# 	u = line.split(' '	)[1][:-1]
# 	gt_mapping[int(i)] = int(u)

# # Construct the ground truth inverse mapping
# gt_inverse_mapping = dict()
# for i, u in gt_mapping.items():
# 	gt_inverse_mapping[u] = i

# gt_mapping_file.close()

# ----------------------------------- #
#         Sizes of Two Networks       #
# ----------------------------------- #
g1_size = len(g1)
g2_size = len(g2)

# -----------------------------------#
#         Adjacency Matrices         #
# -----------------------------------#
ordered_list = [i for i in range(g1_size)]

C = nx.to_numpy_matrix(g1, nodelist = ordered_list, dtype = np.int64)
D = nx.to_numpy_matrix(g2, nodelist = ordered_list, dtype = np.int64)

# --------------------------- #
#        Max Iteration        #
# --------------------------- #
diameter = nx.diameter(g1)
max_iter = diameter + 1

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

# ------------------------------------------------------- #
#         Compute the percentage of node coverage         #
# ------------------------------------------------------- #
# [[0.005277044854881266, 0.018469656992084433, ..., 1.0, 1.0], [...], [...], [...] ... [...]]
g1_node_coverage_percentage = [[] for i in range(g1_size)]
for node in g1.nodes():
	discovered = [0] * g1_size # 0 : not discovered, 1 : discovered
	discovered[node] = 1
	num_of_discovred_node = 1
	frontier = [node]

	for iter_num in range(max_iter):
		new_frontier = []
		for n in frontier:
			for nei in g1.neighbors(n):
				if not discovered[nei]:	
					num_of_discovred_node += 1
					new_frontier.append(nei)
					discovered[nei] = 1
		cov_percentage = num_of_discovred_node / g1_size
		g1_node_coverage_percentage[node].append(cov_percentage)
		frontier = new_frontier

g2_node_coverage_percentage = [[] for i in range(g2_size)]
for node in g2.nodes():
	discovered = [0] * g2_size # 0 : not discovered, 1 : discovered
	discovered[node] = 1
	num_of_discovred_node = 1
	frontier = [node]

	for iter_num in range(max_iter):
		new_frontier = []
		for n in frontier:
			for nei in g2.neighbors(n):
				if not discovered[nei]:	
					num_of_discovred_node += 1
					new_frontier.append(nei)
					discovered[nei] = 1
		cov_percentage = num_of_discovred_node / g2_size
		g2_node_coverage_percentage[node].append(cov_percentage)
		frontier = new_frontier

#########################################################################
#                                 MAIN                                  #
#########################################################################

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

print("Preprocessing Finished")

# --------------------------- #
#     Start the Profiler      #
# --------------------------- #
pr = cProfile.Profile()
pr.enable()

# --------------- #
#  Funciton Call  #
# --------------- #

S = uti.initial_solution_enhanced_testing(S_ini, b_g1_ini, b_g2_ini, g1, g2, g1_neighbor_sequence, g2_neighbor_sequence, g1_degree_sequence, g2_degree_sequence, g1_size, g2_size, max_iter, g1_node_coverage_percentage, g2_node_coverage_percentage, cut_off = 2)

# --------------------------- #
#      End the Profiler       #
# --------------------------- #
pr.disable()
pr.print_stats(sort='time')

# ------------------------------------------ #
#      New Extract the Mapping (Greedy)      #
# ------------------------------------------ #
# The initial mapping
mapping = dict()
# Determine if a vertex is mapped
g1_selected = [0] * (g1_size)
g2_selected = [0] * (g2_size)

maxi_of_each_vertex = dict() # record the maxi of each vertex
edge_weight_pairs = [] # format: [((i,u), weight)]

for i in g1.nodes():
	for u in g2.nodes():
		edge_weight_pairs.append(((i,u), S[i][u]))

sorted_edge_weight_pairs = sorted(edge_weight_pairs, key=lambda x: x[1], reverse = True)

for pair in sorted_edge_weight_pairs:
	i = pair[0][0]
	u = pair[0][1]
	if (not g1_selected[i]) and (not g2_selected[u]):
		mapping[i] = u
		g1_selected[i] = 1
		g2_selected[u] = 1

# initial inverse mapping
inverse_mapping = {}
for k, v in mapping.items():
	inverse_mapping[v] = k

# # ------------------------------------ #
# #      Initial Mapping Percentage      #
# # ------------------------------------ #
# matched_node = 0
# for i in range(g1_size):
# 	if gt_mapping[i] == mapping[i]:
# 		matched_node += 1
# print("Initial mapping percentage: {} (A percentage less than 1.0 does not necessarily indicate incorrect mappings)".format(matched_node / g1_size))

# ------------------- #
#     Initial EC      #
# ------------------- #
mapped_edges = 0
total_edges = 0
objective = 0
for i in range(len(g1)):
	u = mapping[i]
	for j in range(len(g1)):
		v = mapping[j]
		objective += C[i,j] * D[u,v] # compute the objective
		if C[i, j] == 1:
			total_edges += 1
			if D[u, v] == 1:
				mapped_edges += 1

ec = mapped_edges / total_edges
print("Initial Edge Correctnes: {}".format(ec))
print("Initial Objective: {}".format(objective))

# ------------------------------------------- Quantify the Degree of Mismatching -------------------------------#

# ----------------------------------------------- #
#       Construct the new adjacency matrix        #
# ----------------------------------------------- #

# mapping = {}
# inverse_mapping = {}
# file = open("actual_pertubated_mapping.txt", 'r')

# for line in file:
# 	i = int(line.split(' ')[0])
# 	u = int(line.split(' ')[1][:-1])
# 	mapping[i] = u
# 	inverse_mapping[u] = i
# file.close()

# The size of the new graph
graph_size = C.shape[0] + D.shape[0]

E = np.zeros((graph_size, graph_size), np.int64)

# Fill up the initial blocks
for i in range(C.shape[0]):
	for j in range(C.shape[0]):
		if C[i, j] == 1:
			E[i, j] = 1
for i in range(D.shape[0]):
	for j in range(D.shape[0]):
		if D[i, j] == 1:
			i_prime = i + C.shape[0]
			j_prime = j + C.shape[0]
			E[i_prime, j_prime] = 1

# Fill up the cross section
for i, j in mapping.items():
	j_prime = j + C.shape[0]
	E[i, j_prime] = 1
	E[j_prime, i] = 1

g3 = nx.from_numpy_matrix(E)
g3_node_list = np.asarray(g3.nodes()) # list of node ids, starts from 0

# ------------------------------------------------------ #
#             Compute the initial violation              #
# ------------------------------------------------------ #

# formate: {node_id : violations}
violation_dict = defaultdict(lambda : 0)

# vertices in g1
for i in g1.nodes():
	num_conserved_edges = 0
	for j in g1.neighbors(i):
		u = mapping[i]
		v = mapping[j]
		if D[u, v] == 1: # D[u,v] == 2 if u and v are not adjacent
			num_conserved_edges += 1
			violation_dict[i] = (g1_degree_sequence[i] - num_conserved_edges) / g1_degree_sequence[i]

# vertices in g2
for u in g2.nodes():
	num_conserved_edges = 0
	for v in g2.neighbors(u):
		i = inverse_mapping[u]
		j = inverse_mapping[v]
		num_conserved_edges += C[i, j]
		violation_dict[u + C.shape[0]] = (g2_degree_sequence[u] - num_conserved_edges) / g2_degree_sequence[u]

# ------------------- #
#      Iteration      #
# ------------------- #
"""
Networkx PageRank Parameters:
1. G (graph) – Undirected graphs will be converted to a directed graph with two directed edges for each undirected edge.
2. alpha = 0.85
3. personalization (dict, optional) - A dictionary with a key for every graph node and nonzero personalization value for each node. 
									  By default, a uniform distribution is used.
4. max_iter (integer, optional)  = 100
5. tol (float, optional) = 1e-06 Error tolerance used to check convergence in power method solver
6. nstart (dictionary, optional) - Starting value of PageRank iteration for each node.
7. weight (key, optional) - Edge data key to use as weight. If None weights are set to 1.
8. 

Return:  Dictionary of nodes with PageRank as value
"""

dict_ranking = nx.pagerank(g3, alpha = 0.5, personalization = violation_dict)

# format: list of tuples sorted based on the rankings: [(node_id : ranking)]
sorted_tuple_ranking = uti.sort_dict(dict_ranking)

# vertices in g1 order by ranking in descending order
g1_sorted_ranking = []
for tup in sorted_tuple_ranking:
	if tup[0] < g1_size:
		g1_sorted_ranking.append(tup[0])


# ------------------------------------------------------ #
#                     Local Search                       #
# ------------------------------------------------------ #
local_search_max_iter = 5000 # the maximu number of iterations of local searrch
front_index = 0 # the starting index of the window
window_size = 30
improved = True # does the objective gets improved by the currrent iteration?
unchanged_count = 0 # num of iterations that the objective has remain unchanged at the current window, gets reset if we move the window
stuck  = 0  # The total num of iterations that the objective has remain unchanged
n = 5 # subset size

for iter in range(local_search_max_iter):
	# If the number of violation is not improving
	if not improved:
		unchanged_count += 1
		stuck += 1
	else: # If improves
		stuck = 0
		unchanged_count = 0

	# If we have been stucked at the current window for some iterations, move one element forward
	if unchanged_count == 1000:
		front_index += 1
		unchanged_count = 0

	# Random sampling
	num_of_sampled_vertices = 0
	v1 = []
	v2 = []
	while num_of_sampled_vertices < n:
		rand = random.uniform(front_index, front_index + window_size)
		if g1_sorted_ranking[int(rand)] not in v1:
			v1.append(g1_sorted_ranking[int(rand)])
			num_of_sampled_vertices += 1
	for i in v1:
		v2.append(mapping[i])

	best_objective = 0
	for i in v1:
		u = mapping[i]
		for j in g1_neighbor_sequence[i]:
			v = mapping[j]
			best_objective += C[i,j] * D[u,v]

	improved = False

	all_possible_alignments = list(itertools.permutations(v2))
	for align in all_possible_alignments:
		local_mapping = dict()
		for index in range(len(v1)):
			local_mapping[v1[index]] = align[index]
		new_local_objective = 0
		for i, u in local_mapping.items():
			for j in g1_neighbor_sequence[i]:
				if j in v1:
					v = local_mapping[j]
				else:
					v = mapping[j]
				new_local_objective += C[i,j] * D[u,v]
		if new_local_objective > best_objective:
			for i, u in local_mapping.items():
				mapping[i] = u
			best_objective = new_local_objective
			improved = True

	if stuck > 2000:
			print("Number of iterations: {}".format(iter))
			break


# ------------------ #
#      Final EC      #
# ------------------ #
mapped_edges = 0
total_edges = 0
objective = 0
for i in range(len(g1)):
	u = mapping[i]
	for j in range(len(g1)):
		v = mapping[j]
		objective += C[i,j] * D[u,v] # compute the objective
		if C[i, j] == 1:
			total_edges += 1
			if D[u, v] == 1:
				mapped_edges += 1

ec = mapped_edges / total_edges
print("Final Edge Correctnes: {}".format(ec))
print("Final objective: {}".format(objective))

