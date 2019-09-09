import utility as uti
import numpy as np
import networkx as nx
import math
import random
from collections import defaultdict
from docplex.mp.constants import ComparisonType
from docplex.mp.model import Model

# ------------------------------------------- Quantify the Degree of Mismatching -------------------------------#

# 	if ini_ec != 1.0:
# 		# ----------------------------------------------- #
# 		#       Construct the new adjacency matrix        #
# 		# ----------------------------------------------- #

# 		# mapping = {}
# 		# inverse_mapping = {}
# 		# file = open("actual_pertubated_mapping.txt", 'r')

# 		# for line in file:
# 		# 	i = int(line.split(' ')[0])
# 		# 	u = int(line.split(' ')[1][:-1])
# 		# 	mapping[i] = u
# 		# 	inverse_mapping[u] = i
# 		# file.close()

# 		# The size of the new graph
# 		graph_size = C.shape[0] + D.shape[0]

# 		E = np.zeros((graph_size, graph_size), np.int64)

# 		# Fill up the initial blocks
# 		for i in range(C.shape[0]):
# 			for j in range(C.shape[0]):
# 				if C[i, j] == 1:
# 					E[i, j] = 1
# 		for i in range(D.shape[0]):
# 			for j in range(D.shape[0]):
# 				if D[i, j] == 1:
# 					i_prime = i + C.shape[0]
# 					j_prime = j + C.shape[0]
# 					E[i_prime, j_prime] = 1

# 		# Fill up the cross section
# 		for i, j in mapping.items():
# 			j_prime = j + C.shape[0]
# 			E[i, j_prime] = 1
# 			E[j_prime, i] = 1

# 		g3 = nx.from_numpy_matrix(E)
# 		g3_node_list = np.asarray(g3.nodes()) # list of node ids, starts from 0

# 		# ------------------------------------------------------ #
# 		#             Compute the initial violation              #
# 		# ------------------------------------------------------ #

# 		# formate: {node_id : violations}
# 		violation_dict = defaultdict(lambda : 0)

# 		# vertices in g1
# 		for i in g1.nodes():
# 			num_conserved_edges = 0
# 			for j in g1.neighbors(i):
# 				u = mapping[i]
# 				v = mapping[j]
# 				if D[u, v] == 1: # D[u,v] == 2 if u and v are not adjacent
# 					num_conserved_edges += 1
# 					violation_dict[i] = (g1_degree_sequence[i] - num_conserved_edges) / g1_degree_sequence[i]

# 		# vertices in g2
# 		for u in g2.nodes():
# 			num_conserved_edges = 0
# 			for v in g2.neighbors(u):
# 				i = inverse_mapping[u]
# 				j = inverse_mapping[v]
# 				num_conserved_edges += C[i, j]
# 				violation_dict[u + C.shape[0]] = (g2_degree_sequence[u] - num_conserved_edges) / g2_degree_sequence[u]

# 		# ------------------- #
# 		#      Iteration      #
# 		# ------------------- #
# 		"""
# 		Networkx PageRank Parameters:
# 		1. G (graph) – Undirected graphs will be converted to a directed graph with two directed edges for each undirected edge.
# 		2. alpha = 0.85
# 		3. personalization (dict, optional) - A dictionary with a key for every graph node and nonzero personalization value for each node. 
# 											By default, a uniform distribution is used.
# 		4. max_iter (integer, optional)  = 100
# 		5. tol (float, optional) = 1e-06 Error tolerance used to check convergence in power method solver
# 		6. nstart (dictionary, optional) - Starting value of PageRank iteration for each node.
# 		7. weight (key, optional) - Edge data key to use as weight. If None weights are set to 1.
# 		8. 

# 		Return:  Dictionary of nodes with PageRank as value
# 		"""

# 		dict_ranking = nx.pagerank(g3, alpha = 0.5, personalization = violation_dict)

# 		# format: list of tuples sorted based on the rankings: [(node_id : ranking)]
# 		sorted_tuple_ranking = uti.sort_dict(dict_ranking)

# 		# vertices in g1 order by ranking in descending order
# 		g1_sorted_ranking = []
# 		for tup in sorted_tuple_ranking:
# 			if tup[0] < g1_size:
# 				g1_sorted_ranking.append(tup[0])


# 		# ------------------------------------------------------ #
# 		#                     Local Search                       #
# 		# ------------------------------------------------------ #
# 		local_search_max_iter = 5000 # the maximu number of iterations of local searrch
# 		front_index = 0 # the starting index of the window
# 		window_size = 30
# 		improved = True # does the objective gets improved by the currrent iteration?
# 		unchanged_count = 0 # num of iterations that the objective has remain unchanged at the current window, gets reset if we move the window
# 		stuck  = 0  # The total num of iterations that the objective has remain unchanged
# 		n = 5 # subset size

# 		for iter in range(local_search_max_iter):
# 			# If the number of violation is not improving
# 			if not improved:
# 				unchanged_count += 1
# 				stuck += 1
# 			else: # If improves
# 				stuck = 0
# 				unchanged_count = 0

# 			# If we have been stucked at the current window for some iterations, move one element forward
# 			if unchanged_count == 1000:
# 				front_index += 1
# 				unchanged_count = 0

# 			# Random sampling
# 			num_of_sampled_vertices = 0
# 			v1 = []
# 			v2 = []
# 			while num_of_sampled_vertices < n:
# 				rand = random.uniform(front_index, front_index + window_size)
# 				if g1_sorted_ranking[int(rand)] not in v1:
# 					v1.append(g1_sorted_ranking[int(rand)])
# 					num_of_sampled_vertices += 1
# 			for i in v1:
# 				v2.append(mapping[i])

# 			best_objective = 0
# 			for i in v1:
# 				u = mapping[i]
# 				for j in g1_neighbor_sequence[i]:
# 					v = mapping[j]
# 					best_objective += C[i,j] * D[u,v]

# 			improved = False

# 			all_possible_alignments = list(itertools.permutations(v2))
# 			for align in all_possible_alignments:
# 				local_mapping = dict()
# 				for index in range(len(v1)):
# 					local_mapping[v1[index]] = align[index]
# 				new_local_objective = 0
# 				for i, u in local_mapping.items():
# 					for j in g1_neighbor_sequence[i]:
# 						if j in v1:
# 							v = local_mapping[j]
# 						else:
# 							v = mapping[j]
# 						new_local_objective += C[i,j] * D[u,v]
# 				if new_local_objective > best_objective:
# 					for i, u in local_mapping.items():
# 						mapping[i] = u
# 					best_objective = new_local_objective
# 					improved = True

# 			if stuck > 2000:
# 					print("Number of iterations: {}".format(iter))
# 					break

# 	# ------------------ #
# 	#      Final EC      #
# 	# ------------------ #
# 	mapped_edges = 0
# 	total_edges = 0
# 	objective = 0
# 	for i in range(len(g1)):
# 		u = mapping[i]
# 		for j in range(len(g1)):
# 			v = mapping[j]
# 			objective += C[i,j] * D[u,v] # compute the objective
# 			if C[i, j] == 1:
# 				total_edges += 1
# 				if D[u, v] == 1:
# 					mapped_edges += 1

# 	final_ec = mapped_edges / total_edges
# 	print("Final Edge Correctnes: {}".format(final_ec))
# 	print("Final objective: {}".format(objective))

# 	y_with_local_search.append(final_ec)

# 	print(" ---------------------------------------------- ")

# print(y_without_local_search)
# print(y_with_local_search)

