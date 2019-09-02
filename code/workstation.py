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

# --------------------------------------------- Initial Solution -------------------------------------------------#

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
File: dataset/CA-GrQc.txt
"""

"""
Dataset: Coauthorship network of scientists working on network theory and experiment
Link: http://www-personal.umich.edu/~mejn/netdata/
Nodes in largest CC: 379
Edges in largest CC: 914
File: newman_netscience.gml
"""

# g1 = nx.read_gml("dataset/newman_netscience.gml")
# g1 = nx.read_edgelist("dataset/CA-GrQc.txt")

# ------------------------------------- #
#         Extract the Largest CC        #
# ------------------------------------- #
# largest_cc = max(nx.connected_components(g1), key=len)
# g1 = g1.subgraph(largest_cc)

# -------------------------------------------------------- #
#      Relabel the Network with Consecutive Integers       #
# -------------------------------------------------------- #
# g1 = nx.convert_node_labels_to_integers(g1)

# --------------------------------------------- #
#                  Remove Loops                 #
# --------------------------------------------- #
# g1.remove_edges_from(g1.selfloop_edges())

# # ---------------------------------------------- #
# #       Construct the Ground Truth Mapping       #
# # ---------------------------------------------- #
# # g1_node_list = np.asarray(g1.nodes())
# # g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

# # Construct the ground truth mapping
# gt_mapping = dict()
# for i in range(len(g1_node_list)):
#         gt_mapping[g1_node_list[i]] = g2_node_list[i]

# # Construct the ground truth inverse mapping
# gt_inverse_mapping = dict()
# for i in range(len(g2_node_list)):
#     gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

# ------------------------------------------------- #
#          Construct the Isomorphic Network         #
# ------------------------------------------------- #
# g2 = nx.relabel_nodes(g1, gt_mapping)


# nx.write_edgelist(g1, "g1_network.edgelist", data = False)
# nx.write_edgelist(g2, "g2_original_network.edgelist", data = False)

# gt_mapping_file = open("gt_mapping.txt", 'w')
# for i, u in gt_mapping.items():
# 	gt_mapping_file.write(str(i) + ' ' + str(u) + '\n')


# D_orignal = nx.to_numpy_matrix(g2, nodelist = g1_node_list, dtype = np.int64)


# # -------------------------------------------------- #
# #               Perturbation of g2                   #
# # -------------------------------------------------- #
# perturbation_prob = 0.002
# total_number_of_added_edges = 0
# for i in g2.nodes():
# 	for j in g2.nodes():
# 		if i != j:
# 			random_number = random.uniform(1, 1000)
# 			if (random_number <= 1000 * perturbation_prob) and (not g2.has_edge(i, j)):
# 				total_number_of_added_edges += 1
# 				g2.add_edge(i,j)
# print("{} edges were added".format(total_number_of_added_edges))

# nx.write_edgelist(g2, "g2_perturbated_network.edgelist", data = False)

# # ------------------------------------------------ #
# #                 Read in G1 and G2                #
# # ------------------------------------------------ #
# g1 = nx.read_edgelist("g1_network.edgelist", nodetype = int)
# g2 = nx.read_edgelist('g2_perturbated_network.edgelist', nodetype = int)
# g2_origianl = nx.read_edgelist('g2_original_network.edgelist', nodetype = int)

# g1_node_list = np.asarray(g1.nodes())
# g2_node_list = np.asarray(g2.nodes())

# # ---------------------------------------------- #
# #       Construct the Ground Truth Mapping       #
# # ---------------------------------------------- #
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

# # ----------------------------------- #
# #         Sizes of Two Networks       #
# # ----------------------------------- #
# g1_size = len(g1)
# g2_size = len(g2)

# # -----------------------------------#
# #         Adjacency Matrices         #
# # -----------------------------------#
# ordered_list = [i for i in range(g1_size)]

# C = nx.to_numpy_matrix(g1, nodelist = ordered_list, dtype = np.int64)
# D = nx.to_numpy_matrix(g2, nodelist = ordered_list, dtype = np.int64)


# # ------------------- #
# #      Update D       #
# # ------------------- #
# d_replace = 2
# D = np.where(D==0, d_replace, D)

# # --------------------------- #
# #        Max Iteration        #
# # --------------------------- #
# diameter = nx.diameter(g1) #17
# max_iter = diameter + 1

# # -------------------------------------- #
# #             Degree Sequence            #
# # -------------------------------------- #
# g1_degree_sequence = [None] * g1_size
# g2_degree_sequence = [None] * g2_size

# for node in g1.nodes():
# 	g1_degree_sequence[node] = g1.degree(node)

# for node in g2.nodes():
# 	g2_degree_sequence[node] = g2.degree(node)

# # ------------------------------------------ #
# #             Neighrbor Sequence             #
# # ------------------------------------------ #
# g1_neighbor_sequence = [None] * g1_size
# g2_neighbor_sequence = [None] * g2_size

# for node in g1.nodes():
# 	g1_neighbor_sequence[node] = list(g1.neighbors(node))

# for node in g2.nodes():
# 	g2_neighbor_sequence[node] = list(g2.neighbors(node))


# # ######################################################################### #
# #                                   MAIN                                    #
# # ######################################################################### #

# # ----------------------------- # 
# #   Initial Similarity Matrix   #
# # ----------------------------- #
# S_ini = [[min(g1_degree_sequence[i], g2_degree_sequence[u]) / max(g1_degree_sequence[i], g2_degree_sequence[u]) for u in range(g2_size)] for i in range(g1_size)]

# # ----------------------------- # 
# #     Initial Greedy Vector     #
# # ----------------------------- #
# b_g1_ini = [None] * (g1_size)
# b_g2_ini = [None] * (g2_size)

# for i in range(g1_size):
# 	b_g1_ini[i] = max(S_ini[i])
# for u in range(g2_size):
# 	maxi = -2
# 	for i in range(g1_size):
# 		if S_ini[i][u] > maxi:
# 			maxi = S_ini[i][u]
# 	b_g2_ini[u] = maxi

# print("Preprocessing Finished")

# # --------------------------- #
# #     Start the Profiler      #
# # --------------------------- #
# pr = cProfile.Profile()
# pr.enable()

# # --------------- #
# #  Funciton Call  #
# # --------------- #

# S = uti.initial_solution_enhanced(S_ini, b_g1_ini, b_g2_ini, g1, g2, g1_neighbor_sequence, g2_neighbor_sequence, g1_degree_sequence, g2_degree_sequence, g1_size, g2_size, max_iter)

# # --------------------------- #
# #      End the Profiler       #
# # --------------------------- #
# pr.disable()
# pr.print_stats(sort='time')

# # ------------------------------------------ #
# #      New Extract the Mapping (Greedy)      #
# # ------------------------------------------ #
# # The initial mapping
# mapping = dict()
# # Determine if a vertex is mapped
# g1_selected = [0] * (g1_size)
# g2_selected = [0] * (g2_size)

# maxi_of_each_vertex = dict() # record the maxi of each vertex
# edge_weight_pairs = [] # format: [((i,u), weight)]

# for i in g1.nodes():
# 	for u in g2.nodes():
# 		edge_weight_pairs.append(((i,u), S[i][u])) 

# sorted_edge_weight_pairs = sorted(edge_weight_pairs, key=lambda x: x[1], reverse = True)

# for pair in sorted_edge_weight_pairs:
# 	i = pair[0][0]
# 	u = pair[0][1]
# 	if (not g1_selected[i]) and (not g2_selected[u]):
# 		mapping[i] = u
# 		g1_selected[i] = 1
# 		g2_selected[u] = 1

# # initial inverse mapping
# inverse_mapping = {}
# for k, v in mapping.items():
# 	inverse_mapping[v] = k

# # ------------------------------------- #
# #      Record the actural mapping       #
# # ------------------------------------- #
# actual_mapping = open("actual_pertubated_mapping.txt", 'w')
# for i, u in mapping.items():
# 	actual_mapping.write("{} ({}) - {} ({}) \n".format(i, g1_degree_sequence[i], u, g2_degree_sequence[u]))
# actual_mapping.close()

# # ------------------------------------ #
# #      Initial Mapping Percentage      #
# # ------------------------------------ #
# matched_node = 0
# for i in range(g1_size):
# 	if gt_mapping[i] == mapping[i]:
# 		matched_node += 1
# print("Initial mapping percentage: {} (A percentage less than 1.0 does not necessarily indicate incorrect mappings)".format(matched_node / g1_size))

# # ------------ #
# #      EC      #
# # ------------ #
# mapped_edges = 0
# total_edges = 0
# objective = 0
# for i in range(len(g1)):
# 	u = mapping[i]
# 	for j in range(len(g1)):
# 		v = mapping[j]
# 		objective += C[i,j] * D[u,v] # compute the objective
# 		if C[i, j] == 1:
# 			total_edges += 1
# 			if D[u, v] == 1:
# 				mapped_edges += 1

# ec = mapped_edges / total_edges
# print("Initial Edge Correctnes: {}".format(ec))
# print("Initial Objective: {}".format(objective))

# # --------------------------------------------- End of Initial Solution --------------------------------------#


# # ------------------------------------------- Quantify the Degree of Mismatching -------------------------------#

# # ----------------------------------------------- #
# #       Construct the new adjacency matrix        #
# # ----------------------------------------------- #

# # The size of the new graph
# graph_size = C.shape[0] + D.shape[0]

# E = np.zeros((graph_size, graph_size), np.int64)

# # Fill up the initial blocks
# for i in range(C.shape[0]):
# 	for j in range(C.shape[0]):
# 		if C[i, j] == 1:
# 			E[i, j] = 1
# for i in range(D.shape[0]):
# 	for j in range(D.shape[0]):
# 		if D[i, j] == 1:
# 			i_prime = i + C.shape[0]
# 			j_prime = j + C.shape[0]
# 			E[i_prime, j_prime] = 1

# # Fill up the cross section
# for i, j in mapping.items():
# 	j_prime = j + C.shape[0]
# 	E[i, j_prime] = 1
# 	E[j_prime, i] = 1

# g3 = nx.from_numpy_matrix(E)
# g3_node_list = np.asarray(g3.nodes()) # list of node ids, starts from 0

# # ------------------------------------------------------ #
# #             Compute the initial violation              #
# # ------------------------------------------------------ #

# # formate: {node_id : violations}
# violation_dict = defaultdict(lambda : 0)

# # vertices in g1
# for i in g1.nodes():
# 	num_conserved_edges = 0
# 	for j in g1.neighbors(i):
# 		u = mapping[i]
# 		v = mapping[j]
# 		if D[u, v] == 1: # D[u,v] == 2 if u and v are not adjacent
# 			num_conserved_edges += 1
# 			violation_dict[i] = (g1_degree_sequence[i] - num_conserved_edges) / g1_degree_sequence[i]

# # vertices in g2
# for u in g2.nodes():
# 	num_conserved_edges = 0
# 	for v in g2.neighbors(u):
# 		i = inverse_mapping[u]
# 		j = inverse_mapping[v]
# 		num_conserved_edges += C[i, j]
# 		violation_dict[u + C.shape[0]] = (g2_degree_sequence[u] - num_conserved_edges) / g2_degree_sequence[u]

# # ------------------- #
# #      Iteration      #
# # ------------------- #
# """
# Networkx PageRank Parameters:
# 1. G (graph) – Undirected graphs will be converted to a directed graph with two directed edges for each undirected edge.
# 2. alpha = 0.85
# 3. personalization (dict, optional) - A dictionary with a key for every graph node and nonzero personalization value for each node. 
# 									  By default, a uniform distribution is used.
# 4. max_iter (integer, optional)  = 100
# 5. tol (float, optional) = 1e-06 Error tolerance used to check convergence in power method solver
# 6. nstart (dictionary, optional) - Starting value of PageRank iteration for each node.
# 7. weight (key, optional) - Edge data key to use as weight. If None weights are set to 1.
# 8. 

# Return:  Dictionary of nodes with PageRank as value
# """

# dict_ranking = nx.pagerank(g3, alpha = 0.5, personalization = violation_dict)

# # format: list of tuples sorted based on the rankings: [(node_id : ranking)]
# sorted_tuple_ranking = uti.sort_dict(dict_ranking)

# # vertices in g1 order by ranking in descending order
# g1_sorted_ranking = []
# for tup in sorted_tuple_ranking:
# 	if tup[0] < g1_size:
# 		g1_sorted_ranking.append(tup[0])

# # ----------------------------------------------- Refinement -------------------------------------------- #

# # --------------------- #
# #       Parameters      #
# # --------------------- #
# beta = 1000 # Force the constraint
# max_iter = 4000
# sample_size = 5
# wrong = False

# # ---------------------------------------------- #
# #                  Local Search                  #
# # ---------------------------------------------- #

# # ------------------------- #
# #      Get ready to plot    #
# # ------------------------- #
# # x = []
# # y = []

# # pre_violation = 0 # objective from the previous iteration
# improved = True
# unchanged_count = 0 # the number of iterations that the objective has remain unchanged, gets reset if we move the window
# window = 10 # window size
# stuck  = 0 

# # ------------------------ #
# #      Main Iteration      #
# # ------------------------ #
# for iter in range(max_iter):
# 	# If the number of violation is not improving
# 	if not improved:
# 		unchanged_count += 1
# 		stuck += 1
# 	else: # If improves
# 		stuck = 0
# 		unchanged_count = 0

# 	# If we have been stucked for some iterations, move one element forward
# 	if unchanged_count == 3:
# 		window += 1
# 		unchanged_count = 0
 
# 	# Sample n nodes based on the violation
# 	V_1 = []
# 	V_1.append(g1_sorted_ranking[window - 10])
# 	n = sample_size
# 	num_of_sampled_vertices = 1

# 	while num_of_sampled_vertices < n:
# 		rand = random.uniform(window - 9, window)
# 		if g1_sorted_ranking[int(rand)] not in V_1:
# 			V_1.append(g1_sorted_ranking[int(rand)])
# 			num_of_sampled_vertices += 1

# 	# construct the corresponding mapped nodes in g2
# 	V_2 = []
# 	for i in V_1:
# 		V_2.append(mapping[i])

# 	#-------------------------------- Construct matrix H (Beginning) -----------------------------

# 	# M_1 = \beta \times I_{n_1 \times n_1} \otimes Oi(I_{n_2 \times n_2} ), here n_1 = n_2 = n
# 	M_1 = beta * np.kron(
# 		np.identity(n, np.int64),
# 		uti.Oi(np.identity(n, np.int64))
# 		)

# 	# M_2 = \beta \times Oi(I_{n_1 \times n_1}) \otimes I_{n_2 \times n_2}, here n_1 = n_2 = n
# 	M_2 = beta * np.kron(
# 		uti.Oi(np.identity(n, np.int64)),
# 		np.identity(n, np.int64)
# 		)

# 	# M_3 = -2\beta \times I_{n_1n_2 \times n_1n_2}
# 	M_3 =  -2 * beta * np.identity(n**2)

# 	# Extract submatrix of C for which only contains the selected nodes in V_1
# 	partial_C = np.zeros((n, n), np.int64)
# 	for i in range(n):
# 		for j in range(n):
# 			partial_C[i, j] = C[V_1[i], V_1[j]]

# 	# Extract submatrix for D for which only contains the selected nodes in V_2
# 	partial_D = np.zeros((n, n), np.int64)
# 	for i in range(n):
# 		for j in range(n):
# 			partial_D[i, j] = D[V_2[i], V_2[j]]

# 	# Finally, matrix H
# 	H = np.kron(partial_C, partial_D) + M_1 + M_2 + M_3

# 	#---------------------------------Construct matrix H (Ending) -----------------------------

# 	#------------------------------Construct bias vector J (beginning)-------------------------

# 	# J1
# 	J_1 = [0] * n**2
# 	for i1 in range(n):
# 		i = V_1[i1]
# 		nei = set(g1.neighbors(i))
# 		nei = list(nei - set(V_1))
# 		for i2 in range(n):
# 			u = V_2[i2]
# 			s = 0
# 			index = 0
# 			for k in nei:
# 				psi_k = mapping[k]
# 				s += C[i, k] * D[u, psi_k]
# 				index = n * (i1) + i2 # Here we use i1 insteand of i1 - 1 because list are zero indexed
# 			J_1[index] = s

# 	#J2
# 	J_2 = [0] * n**2
# 	for i1 in range(n):
# 		i = V_1[i1]
# 		for i2 in range(n):
# 			u = V_2[i2]
# 			nei = set(g2.neighbors(u))
# 			nei = list(nei - set(V_2))
# 			s = 0
# 			for h in nei:
# 				psi_h_inv = inverse_mapping[h]
# 				s += C[i, psi_h_inv] * D[u, h]
# 				index = n * (i1) + i2 # Here we use i1 insteand of i1 - 1 because list are zero indexed
# 			J_2[index] = -s
	
# 	#J
# 	J = [0] * n**2
# 	for ind in range(n**2):
# 		J[ind] = J_1[ind] + J_2[ind]

# 	#------------------------------QUBO: Construct bias vector J (ending)-------------------------

# 	# ------------------------------------------------------------------
# 	#                       PROPOSED REFINEMENT                        -
# 	# ------------------------------------------------------------------

# 	# The result of the subproblem of size n
# 	result2 = uti.solve_ising(H, J) #RESULTS ARE FLOATS!!!!!
# 	constraint_checker = []
	
# 	improved = False

# 	# Extract the index and upate the mapping
# 	for r in range(len(result2)):
# 		if result2[r] == 1.0:
# 			i = V_1[math.floor(r / n)]
# 			u = V_2[r % n]
# 			if u in constraint_checker:
# 				wrong = True
# 			constraint_checker.append(u)
# 			# Swapping are closed under V_1 and V_2
# 			if mapping[i] != u: # if the objective improves
# 				improved = True
# 			mapping[i] = u
# 			inverse_mapping[u] = i
# 	if stuck > 30:
# 		print("Number of iterations: {}".format(iter))
# 		break

# # ----------------------- #
# #            Plot         #
# # ----------------------- #
# # plt.plot(x, y, '--bo')
# # plt.show()

# # --------------------------------------------- #
# #           Final mapping percentage            #
# # --------------------------------------------- #
# matched_node = 0
# for i in range(len(g1)):
#     if gt_mapping[i] == mapping[i]:
#         matched_node += 1
# print("Final mapping percentage: {}".format(matched_node / len(g1)))

# # ------------ #
# #      EC      #
# # ------------ #
# mapped_edges = 0
# total_edges = 0
# objective = 0
# for i in range(len(g1)):
# 	u = mapping[i]
# 	for j in range(len(g1)):
# 		v = mapping[j]
# 		objective += C[i,j] * D[u,v] # compute the objective
# 		if C[i, j] == 1:
# 			total_edges += 1
# 			if D[u, v] == 1:
# 				mapped_edges += 1

# ec = mapped_edges / total_edges
# print("Final Edge Correctnes: {}".format(ec))
# print("Final Objective: {}".format(objective))

# # --------------------------------------------------- #
# #          Check if the contraint workds fine         #
# # --------------------------------------------------- #    
# if not wrong:
# 	print("The constraint works fine")
# else:
# 	print("The constraint fails")