import numpy as np
import networkx as nx
import random
import utility as uti
from collections import defaultdict
import cProfile
import math

# ------------------------
#       Parameteres      -
# ------------------------
d_replace = 2
network_size = 100

# Start the profiler
print("### start the profiler for network creatio ###")
pr = cProfile.Profile()
pr.enable()

#-------------------------------------------------
#              EXAMPLE RANDOM GRAPHS             -
#-------------------------------------------------
g1 = uti.construct_random_graph("barabasi_c", n = network_size)

max_iter = nx.diameter(g1)

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

# The size of two networks will be differnt for real networks
g1_size = g2_size = network_size

# ------------------------------ 
#   Initial Similarity Matrix  -
# ------------------------------
S = np.ones((g1_size, g2_size), np.float64)

# ------------------------------
#     Initial Greedy Vector    -
# ------------------------------
b = np.ones(((g1_size + g2_size), 1), np.float64)

# End the profiler
pr.disable()
pr.print_stats(sort='time')

# Start the profiler
print("### start the profiler for the main iteration ###")
pr = cProfile.Profile()
pr.enable()

#------------------------------------------------------------------------#
#                         Iteration starts here                         #
#------------------------------------------------------------------------#
for _ in range(max_iter):
	# ------------------------
	#       new S and b      -
	# ------------------------
	b_new = -np.ones(((g1_size + g2_size), 1), np.float64)
	S_new = np.zeros((g1_size, g2_size), np.float64) # the only time we use S_new is assignment, therefore, its initial value doesn't matter

	# NOTE: for b and b_new, the index of u is u + g1_size
	for i in g1.nodes():
		for u in g2.nodes():
			# ---------------------------------------
			#    The complete bipartite graph       -
			# ---------------------------------------
			# Instead of constructing the actural graph (which is costly), we create a dictionary B with the format:
			# {(j, v) : weight}
			B = defaultdict(lambda : 0.0)
			neighbors_of_i = {}
			neighbors_of_u = {}
			for j in g1.neighbors(i):
				for v in g2.neighbors(u):
					B[(j, v)] = S[j, v]
					neighbors_of_i[j] = 0
					neighbors_of_u[v] = 0
			
			# format (list of tuples): [ ( (j, v), weight ) ]
			sorted_B = uti.sort_dict(B)

			index_of_the_largest_undeleted_edge = 0
			c = 0 # accumulated similarity values
			total_number_of_edges = len(list(g1.neighbors(i))) *  len(list(g2.neighbors(u)))

			while index_of_the_largest_undeleted_edge != total_number_of_edges:
				# print(index_of_the_largest_undeleted_edge)
				# format: ((j, v), weight)
				largest = sorted_B[index_of_the_largest_undeleted_edge]
				j = largest[0][0]
				v = largest[0][1]
				weight = largest[1]
				if not (weight < b[j,0] and weight < b[v + g1_size, 0]):
					larger = max(b[j,0], b[v + g1_size, 0])
					c += 2 * weight - larger
					neighbors_of_i[j] = 1
					neighbors_of_u[v] = 1

				index_of_the_largest_undeleted_edge += 1

				while (index_of_the_largest_undeleted_edge != total_number_of_edges) and ((neighbors_of_i[sorted_B[index_of_the_largest_undeleted_edge][0][0]]) or (neighbors_of_u[sorted_B[index_of_the_largest_undeleted_edge][0][1]])):
					index_of_the_largest_undeleted_edge += 1
			
			# Compute the updated similarity
			maxi = max(len(list(g1.neighbors(i))), len(list(g2.neighbors(u))))
			S_new[i,u] = c / maxi
			if S_new[i,u] > b_new[i]:
				b_new[i] = S_new[i,u]
			if S_new[i,u] > b_new[u + g1_size]:
				b_new[u + g1_size] = S_new[i,u]
	# Update
	b = b_new
	S = S_new

# End the profiler
pr.disable()
pr.print_stats(sort='time')


# --------------------------------------
#                 MAIN                 -
# --------------------------------------
mapping = dict()
selected = [0] * (g2_size)

# Greedy 
for i in range(S.shape[0]):
	maxi = -1
	max_index = 0
	for u in range(S.shape[1]):
		if S[i,u] > maxi and not selected[u]:
			maxi = S[i, u]
			max_index = u 
	mapping[i] = max_index
	selected[max_index] = 1

matched_node = 0
for i in range(S.shape[0]):
    if gt_mapping[i] == mapping[i]: 
        matched_node += 1
print("Initial mapping percentage: {} (A percentage less than 1.0 does not necessarily indicate incorrect mappings)".format(matched_node / S.shape[0]))

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

