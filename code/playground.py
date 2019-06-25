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

# Construct the second graph by relabeling the first graph
g2 = nx.relabel_nodes(g1, gt_mapping)

# Adjacency matrices
C = nx.to_numpy_matrix(g1, dtype = np.int64)
D = nx.to_numpy_matrix(g2, g1_node_list, dtype = np.int64)

for i in range(len(g2)):
    for j in range(len(g2)):
        if D[i, j] == 0:
            D[i, j] = d_replace

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

# initial inverse mapping
inverse_mapping = {}
for k, v in mapping.items():
	inverse_mapping[v] = k

# Compute the initial mapping percentage
matched_node = 0
for i in range(len(g1)):
    if gt_mapping[i] == mapping[i]:
        matched_node += 1
print("Initial mapping percentage: {}".format(matched_node / len(g1))) #0.6333333333333333

# ------------------------------------------------------------------------------
#                             INITIAL OBJECTIVE                                -
# ------------------------------------------------------------------------------

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


#-------------------------
#      LOCAL SEARCH      -
# ------------------------

# iteration
for iter in range(max_iter):
    # random sample n nodes from the graph
	V_1 = []
	n = sample_size # sample size
	t = 0
	while t < n:
		rand = random.uniform(0, len(g1))
		if g1_node_list[int(rand)] not in V_1:
			V_1.append(g1_node_list[int(rand)])
			t += 1

	# construct the corresponding mapped nodes in g2
	V_2 = []
	for i in V_1:
		V_2.append(mapping[i])

	#-------------------------------- Construct matrix H (Beginning) -----------------------------

	# M_1 = \beta \times I_{n_1 \times n_1} \otimes Oi(I_{n_2 \times n_2} ), here n_1 = n_2 = n
	M_1 = beta * np.kron(
		np.identity(n, np.int64),
		uti.Oi(np.identity(n, np.int64))
		)

	# M_2 = \beta \times Oi(I_{n_1 \times n_1}) \otimes I_{n_2 \times n_2}, here n_1 = n_2 = n
	M_2 = beta * np.kron(
		uti.Oi(np.identity(n, np.int64)),
		np.identity(n, np.int64)
		)

	# M_3 = -2\beta \times I_{n_1n_2 \times n_1n_2}
	M_3 =  -2 * beta * np.identity(n**2)

	# Extract submatrix of C for which only contains the selected nodes in V_1
	partial_C = np.zeros((n, n), np.int64)
	for i in range(n):
		for j in range(n):
			partial_C[i, j] = C[V_1[i], V_1[j]]

	# Extract submatrix for D for which only contains the selected nodes in V_2
	partial_D = np.zeros((n, n), np.int64)
	for i in range(n):
		for j in range(n):
			partial_D[i, j] = D[V_2[i], V_2[j]]

	# Finally, matrix H
	H = np.kron(partial_C, partial_D) + M_1 + M_2 + M_3

	#---------------------------------Construct matrix H (Ending) -----------------------------

	#------------------------------Construct bias vector J (beginning)-------------------------

	# J1
	J_1 = [0] * n**2
	for i1 in range(n):
		i = V_1[i1]
		nei = set(g1.neighbors(i))
		nei = list(nei - set(V_1))
		for i2 in range(n):
			u = V_2[i2]
			s = 0
			index = 0
			for k in nei:
				psi_k = mapping[k]
				s += C[i, k] * D[u, psi_k]
				index = n * (i1) + i2 # Here we use i1 insteand of i1 - 1 because list are zero indexed
			J_1[index] = s

	#J2
	J_2 = [0] * n**2
	for i1 in range(n):
		i = V_1[i1]
		for i2 in range(n):
			u = V_2[i2]
			nei = set(g2.neighbors(u))
			nei = list(nei - set(V_2))
			s = 0
			for h in nei:
				psi_h_inv = inverse_mapping[h]
				s += C[i, psi_h_inv] * D[u, h]
				index = n * (i1) + i2 # Here we use i1 insteand of i1 - 1 because list are zero indexed
			J_2[index] = -s


	J = [0] * n**2
	for ind in range(n**2):
		J[ind] = J_1[ind] + J_2[ind]

	#------------------------------QUBO: Construct bias vector J (ending)-------------------------


	# ------------------------------------------------------------------
	#                       PROPOSED REFINEMENT                        -
	# ------------------------------------------------------------------

	# The result of the subproblem of size n
	result2 = uti.solve_ising(H, J) #RESULTS ARE FLOATS!!!!!
	constraint_checker = []

	# Extract the index and upate the mapping
	for r in range(len(result2)):
		if result2[r] == 1.0:
			i = V_1[math.floor(r / n)]
			u = V_2[r % n]
			if u in constraint_checker:
				wrong = True
			constraint_checker.append(u)
			# Swapping are closed under V_1 and V_2
			mapping[i] = u
			inverse_mapping[u] = i

	# Updated objective and violations
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

	print("The new objective value: {}".format(objective))
	print("The upated number of  violations: {}".format(count))
	print("-----------------")

	# Break if solved
	if count == 0:
		break

# -----------------------------------------
#        FINAL MAPPING PERCENTAGE         -
# -----------------------------------------

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
print("The final objective value: {}".format(objective))
print("Final violations: {}".format(count))

matched_node = 0
for i in range(len(g1)):
    if gt_mapping[i] == mapping[i]:
        matched_node += 1
print("Final mapping percentage: {}".format(matched_node / len(g1))) #0.6333333333333333

if not wrong:
	print("The constraint works fine")


