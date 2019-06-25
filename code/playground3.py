import numpy as np
import networkx as nx
import random
import utility as uti
from collections import defaultdict
from docplex.mp.constants import ComparisonType
from docplex.mp.model import Model
import math


# the large constant
beta = 1000
d_replace = 2
max_iter = 4000
sample_size = 5
network_size = 100

wrong = False

# g1 = nx.read_edgelist("test1.edgelist", nodetype = int)
# g2 = nx.read_edgelist("test2.edgelist", nodetype = int)

# g1_node_list = list(g1.nodes()) 
# g2_node_list = list(g2.nodes())


#-------------------------------------------
#              EXAMPLE GRAPHS             -
#-------------------------------------------
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

# relabel the graph
g2 = nx.relabel_nodes(g1, gt_mapping)


C = nx.to_numpy_matrix(g1, dtype = np.int64)
D = nx.to_numpy_matrix(g2, g1_node_list, dtype = np.int64)

for i in range(len(g2)):
    for j in range(len(g2)):
        if D[i, j] == 0:
            D[i, j] = d_replace

# the initial mapping (quite arbitrary )
# mapping = {1 : 2, 0 : 4, 3 : 1, 4 : 3, 2 : 0, 5: 5, 6 : 6, 7 : 7, 8 : 8}
# mapping = {5: 0, 3: 6, 0: 2, 8 : 8, 4 : 1, 7 : 7, 1 : 4, 2 : 3, 6 : 5}

# ----------------------------------------------------------------------
#                        INITIAL SOLUTION                              -
# ----------------------------------------------------------------------

# initial Permutation matrix
pi = uti.initial_solution(g1, g2, g1_node_list, 0.2, n = network_size) # the last parameter is the pertubation probability

# initial mapping, format (dict): {vertex in g1 : vertx in g2}
mapping = dict()
for i in range(len(g1)):
    for j in range(len(g2)):
        if pi[i, j] == 1:
            mapping[i] = j

# Compute the initial mapping percentage
matched_node = 0
for i in range(len(g1)):
    if gt_mapping[i] == mapping[i]:
        matched_node += 1
print("Initial mapping percentage: {}".format(matched_node / len(g1))) #0.6333333333333333

# ------------------------------------------------------------------------------
#                             INITIAL OBJECTIVE                                -
# ------------------------------------------------------------------------------
# Cost matrix and Distance matrix
C = nx.to_numpy_matrix(g1, dtype = np.int64)
D = nx.to_numpy_matrix(g2, g1_node_list, dtype = np.int64) # the rows and columns are ordered according to the nodes in g1

# To make g2 complete, we connect pairs of vertices that are not adjacent with edges of weight 2
for i in range(len(g2)):
    for j in range(len(g2)):
        if D[i, j] == 0:
            D[i, j] = d_replace # could be the reason?


# initial objective value
objective = 0
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
		objective += C[i1, j1] * D[i2, j2]

print("The initial objective value: {}".format(objective))
print("Initial violations: {}".format(count))


inverse_mapping = {}
for k, v in mapping.items():
	inverse_mapping[v] = k


vio_per_vertex = defaultdict(lambda : 0)

for i1 in range(len(g1)):
	i2 = mapping[i1]
	for neighbor in g1.neighbor(i1):
		f		