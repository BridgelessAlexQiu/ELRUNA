import numpy as np
import networkx as nx
import random
import utility as uti
from collections import defaultdict
import math
import matplotlib.pyplot as plt


beta = 1000 # Force the constraint
d_replace = 2
max_iter = 4000
sample_size = 5
network_size = 100

wrong = False

#------------------------------------------------------
#                  EXAMPLE GRAPH                      -
# -----------------------------------------------------

# g1 = nx.read_edgelist("test1.edgelist", nodetype = int)
# g2 = nx.read_edgelist("test2.edgelist", nodetype = int)

# g1_node_list = list(g1.nodes()) 
# g2_node_list = list(g2.nodes())

# the initial mapping (quite arbitrary )
# mapping = {1 : 2, 0 : 4, 3 : 1, 4 : 3, 2 : 0, 5: 5, 6 : 6, 7 : 7, 8 : 8}
# mapping = {5: 0, 3: 6, 0: 2, 8 : 8, 4 : 1, 7 : 7, 1 : 4, 2 : 3, 6 : 5}

#-------------------------------------------------
#              EXAMPLE RANDOM GRAPHS             -
#-------------------------------------------------

g1 = uti.construct_random_graph("barabasi_c", n = network_size)

# ------------------------------------------------------------
#             CONSTRUCT THE GROUND TRUTH MAPPING             -
# ------------------------------------------------------------

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

# Construct the second graph by relabeling the first graph
g2 = nx.relabel_nodes(g1, gt_mapping)

# Adjacency matrices
C = nx.to_numpy_matrix(g1, dtype = np.int64)
D = nx.to_numpy_matrix(g2, g1_node_list, dtype = np.int64)

for i in range(len(g2)):
    for j in range(len(g2)):
        if D[i, j] == 0:
            D[i, j] = d_replace

# --------------------------------------------------------------------- #
#                           INITIAL SOLUTION                            #
# --------------------------------------------------------------------- #

# initial Permutation matrix
pi = uti.initial_solution(g1, g2, g1_node_list, 0.2, n = network_size) # the second last parameter is the purtabation probability

# initial mapping, format (dict): {vertex in g1 : vertx in g2}
mapping = dict()
for i in range(len(g1)):
    for j in range(len(g2)):
        if pi[i, j] == 1:
            mapping[i] = j

# initial inverse mapping
inverse_mapping = {}
for k, v in mapping.items():
	inverse_mapping[v] = k

# Initial mapping percentage
matched_node = 0
for i in range(len(g1)):
    if gt_mapping[i] == mapping[i]:
        matched_node += 1
print("Initial mapping percentage: {}".format(matched_node / len(g1))) #0.6333333333333333

# initial objective value
objective = 0
count = 0
for i1 in range(len(g1)):
	for j1 in range(len(g1)):
		i2 = mapping[i1]
		j2 = mapping[j1]
		if C[i1, j1] == 1: # adjacency to nonadjacency
			if D[i2, j2] == d_replace:
				count += 1
		if C[i1, j1] == 0: # nonadjacency to adjacency
			if D[i2, j2] == 1:
				count += 1
		objective += C[i1, j1] * D[i2, j2]

print("The initial objective value: {}".format(objective))
print("Initial violations: {}".format(count))


# ----------------------------------------------- #
#       Construct the new adjacency matrix        #
# ----------------------------------------------- #

# The size of the new graph
graph_size = C.shape[0] + D.shape[0]

E = np.zeros((graph_size, graph_size), np.int64)

# Fill up the initial blocks
for i in range(C.shape[0]):
	for j in range(C.shape[0]):
		if C[i, j] == 1:
			E[i,j] = 1
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
violation = defaultdict(lambda : 0)

# vertices in g1
for i in g1.nodes():
	num_conserved_edges = 0
	for j in g1.neighbors(i):
		u = mapping[i]
		v = mapping[j]
		if D[u, v] == 1: # D[u,v] == 2 if u and v are not adjacent
			num_conserved_edges += 1
	violation[i] = (g1.degree(i) - num_conserved_edges) / g1.degree(i)

# vertices in g2
for u in g2.nodes():
	num_conserved_edges = 0
	for v in g2.neighbors(u):
		i = inverse_mapping[u]
		j = inverse_mapping[v]
		num_conserved_edges += C[i, j]
	violation[u + C.shape[0]] = (g2.degree(u) - num_conserved_edges) / g2.degree(u)

#-------------------- #
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

dict_ranking = nx.pagerank(g3, alpha = 0.45, personalization = violation)

# format: list of tuples sorted based on the rankings: [(node_id : ranking)]
sorted_tuple_ranking = uti.sort_dict(dict_ranking)

g1_sorted_ranking = []
for tup in sorted_tuple_ranking:
	if tup[0] <= 99:
		g1_sorted_ranking.append(tup[0])



# for i, tup in enumerate(sorted_tuple_ranking):
# 	vertex = tup[0]
# 	if vertex <= 99: # in the first network
# 		print(
# 			"Vertex {} in g1 ranked {}, it is mapped to vertex {} in g2. The degree of {} is {}; The degree of {} is {}".format(
# 				vertex,
# 				i,
# 				mapping[vertex],
# 				vertex,
# 				g1.degree(vertex),
# 				mapping[vertex],
# 				g2.degree(mapping[vertex])
# 			)
# 		)
# 	elif vertex > 99: # in the second network
# 		print(
# 			"Vertex {} in g2 ranked {}, it is mapped to vertex {} in g1. The degree of {} is {}; The degree of {} is {}".format(
# 				vertex-100,
# 				i,
# 				inverse_mapping[vertex-100],
# 				vertex-100,
# 				g2.degree(vertex-100),
# 				inverse_mapping[vertex-100],
# 				g1.degree(inverse_mapping[vertex-100])
# 			)
# 		)

for i, tup in enumerate(sorted_tuple_ranking):
	vertex = tup[0]
	if vertex <= 99:
		print("Based on the algorithm, g1 - {} : g2 - {}".format(vertex, mapping[vertex]))
		print("Violation: {}".format(violation[vertex]))
		print("Ground Truth: {} : {}".format(vertex, gt_mapping[vertex]))
		print("-------------")
	elif vertex > 99:
		vertex = vertex - 100
		print("Based on the algorithm, g2 - {} : g1 - {}".format(vertex, inverse_mapping[vertex]))
		print("Violation: {}".format(violation[vertex + 100]))
		print("Ground Truth: {} : {}".format(vertex, gt_inverse_mapping[vertex]))
		print("-------------")

x = []
y = []

for i, tup in enumerate(sorted_tuple_ranking):
	vertex = tup[0]
	if vertex <= 99:
		x.append(violation[vertex])
		if mapping[vertex] == gt_mapping[vertex]:
			y.append(1)
		else:
			y.append(0)
	elif vertex > 99:
		vertex = vertex - 100
		x.append(violation[vertex + 100])
		if inverse_mapping[vertex] == gt_inverse_mapping[vertex]:
			y.append(1)
		else:
			y.append(0)

plt.scatter(x, y)
plt.show()

x = []
y = []

for i, tup in enumerate(sorted_tuple_ranking):
	vertex = tup[0]
	x.append(i+1)
	if vertex <= 99:
		if mapping[vertex] == gt_mapping[vertex]:
			y.append(1)
		else:
			y.append(0)
	elif vertex > 99:
		vertex = vertex - 100
		if inverse_mapping[vertex] == gt_inverse_mapping[vertex]:
			y.append(1)
		else:
			y.append(0)

plt.scatter(x, y)
plt.show()