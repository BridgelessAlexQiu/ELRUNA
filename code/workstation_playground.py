import numpy as np
import networkx as nx
import random
import utility as uti
import cProfile
import timeit
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import itertools
import copy
import numba
from numba import jit
# ------------------------------------------- Initial Solution -----------------------------------------------#

probability = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35, 0.37, 0.39, 0.41, 0.43, 0.45]
# probability = [0.09]
graph_type = "newman_netscience"
network_type = 'real_networks'

print('Graph Type: {}'.format(graph_type))
y = []
for p in probability:
	print("Probability: {}".format(p))
	g1_file_name = "networks/" + network_type + "/" + graph_type + "/edgelist/" + graph_type + "_g1.edgelist"
	g2_file_name = "networks/" + network_type + "/" + graph_type + "/edgelist/" + graph_type + "_" + str(p) +"_g2.edgelist"
	
	# ------------------------------------------------ #
	#                 Read in G1 and G2                #
	# ------------------------------------------------ #
	g1 = nx.read_edgelist(g1_file_name, nodetype = int)
	g2 = nx.read_edgelist(g2_file_name, nodetype = int)

	# ------------------------------------------ #
	#      Add additional edges on top of g2     #
	# ------------------------------------------ #
	# additional_edges = 100
	# for u in g2.nodes():
	# 	for v in g2.nodes():
	# 		random_number = random.uniform(1, 1000)
	# 		if (u != v) and (int(random_number) <= 1000 * p) and (not g2.has_edge(u, v)) and (additional_edges != 0):
	# 			g2.add_edge(u,v)
	# 			print(u, v)
	# 			additional_edges -= 1
	# 		elif additional_edges == 0:
	# 			break
	# 	if additional_edges == 0:
	# 		break

	print(nx.info(g1))
	print(nx.info(g2))

	g1_node_list = np.asarray(g1.nodes())
	g2_node_list = np.asarray(g2.nodes())

	# # ---------------------------------------------- #
	# #       Construct the Ground Truth Mapping       #
	# # ---------------------------------------------- #
	gt_file_name = "networks/" + network_type + "/" + graph_type + "/edgelist/" + graph_type + "_gt_mapping.txt"
	gt_mapping_file = open(gt_file_name, 'r')

	# Construct the ground truth mapping
	gt_mapping = dict()
	for line in gt_mapping_file:
		i = line.split(' ')[0]
		u = line.split(' ')[1][:-1]
		gt_mapping[int(i)] = int(u)

	# Construct the ground truth inverse mapping
	gt_inverse_mapping = dict()
	for i, u in gt_mapping.items():
		gt_inverse_mapping[u] = i

	gt_mapping_file.close()

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
	S = uti.initial_solution_enhanced_testing(S_ini, b_g1_ini, b_g2_ini, g1_neighbor_sequence, g2_neighbor_sequence, g1_degree_sequence, g2_degree_sequence, g1_size, g2_size, max_iter, g1_node_coverage_percentage, g2_node_coverage_percentage)

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

	# ! THIS IS TEMPORARY
	for i in range(g1_size):
		for u in range(g1_size):
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

	ini_ec = mapped_edges / total_edges
	print("Initial Edge Correctnes: {}".format(ini_ec))
	print("Initial Objective: {}".format(objective))
	y.append(ini_ec)
print(y)
#[0.9934354485776805, 0.9912472647702407, 0.9879649890590809, 0.986870897155361, 0.9879649890590809, 0.9934354485776805, 0.9857768052516411, 0.9803063457330415, 0.9846827133479212, 0.9857768052516411, 0.936542669584245, 0.9573304157549234, 0.9332603938730853, 0.9485776805251641, 0.8840262582056893, 0.9266958424507659, 0.8468271334792122, 0.811816192560175, 0.7844638949671773, 0.7024070021881839, 0.7166301969365426, 0.6695842450765864, 0.6039387308533917, 0.6083150984682714]