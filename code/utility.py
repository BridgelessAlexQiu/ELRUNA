import networkx as nx
import numpy as np
import operator
import random
# from docplex.mp.constants import ComparisonType
# from docplex.mp.model import Model
from collections import defaultdict
import cProfile
import matplotlib.pyplot as plt
import math
import numba
from numba import jit

"""
    Search Term:
    sort_dict: sd
    construct_random_graph: crg
    Enhanced Sorting:ises
"""

# ----------------------- #
#     degree seqeunce     #
# ----------------------- #
# Return the degree sequence, format (dict): {node1: degree, node2: degree, ...}
def degree_sequence(G):
    sequence = dict()
    for node, degree in G.degree():
        sequence[node] = degree
    return sequence

# ----------------------------------------------------------- #
#                Check if a matrix is symmetric               # 
# ----------------------------------------------------------- #
def is_symmetric(a, rtol=1e-05, atol=1e-08):
    return np.allclose(a, a.T, rtol=rtol, atol=atol)

# search term: sd
# ----------------------------------------- #
#             Sort Dictionary               #
# ----------------------------------------- #
def sort_dict(d : "the dictionary", dec = True):
    if dec:
        sorted_d = sorted(d.items(), key=lambda kv: kv[1], reverse = True)
    else:
        sorted_d = sorted(d.items(), key=lambda kv: kv[1])
    return sorted_d

# --------------------------------------- #
#         Random Graph Generator          #
# --------------------------------------- #
# * Search term: crg
# Return a particular random graph
def construct_random_graph(type = "homle", n = 200, p = 10, m = 0.4):
    if type == "homle":
        return nx.powerlaw_cluster_graph(n, p, m)
    elif type == "barabasi":
        return nx.barabasi_albert_graph(n, p)
    elif type == "erdos":
        return nx.erdos_renyi_graph(n, 0.3)
    elif type == "watts":
        return nx.connected_watts_strogatz_graph(n, 10, 0.4)
    elif type == "regular":
        return nx.random_regular_graph(4, n)
    else:
        raise ValueError('Unknown graph type!')

# --------------------------------------------------- #
#           Oppostive Identity Operation              #
# --------------------------------------------------- #
def Oi(I):
    one = np.ones((I.shape[0], I.shape[0]), np.int64)
    return (one - I)

# ------------------------------------------------------------ #
#                    Initial permuation matrix                 #
# ------------------------------------------------------------ #
# Construct the initial similarity matrix
def initial_solution(g1, g2, node_list, r : "the perturbation probability", n):
    dim = (len(g1), len(g2)) # dimeonsion of the permutation matrix
    pi = np.zeros(dim, np.int64) # the permutation matrix, initial entries are 0

    # Sort nodes by degrees in descending order. format : list of tuples with size 2
    sorted_ds_g1 = sorted(g1.degree(), key=operator.itemgetter(1), reverse=True)
    sorted_ds_g2 = sorted(g2.degree(), key=operator.itemgetter(1), reverse=True)

    # Adjacency matrix of two networks
    A1 = nx.to_numpy_matrix(g1, dtype = np.int64)
    A2 = nx.to_numpy_matrix(g2, node_list, dtype = np.int64) # the rows and columns are ordered according to the nodes in g1

    # Initial solution, the while loop is necessary here because we want to skip w.s.p
    i = 0
    while i < len(g1):
        # vertices with ith degree ranking in two graphs
        u1 = int(sorted_ds_g1[i][0])
        u2 = int(sorted_ds_g2[i][0])

        # Modified Big-Align Approach
        rand = random.uniform(0, 1)
        if rand >= r or i == n-1:
            pi[u1, u2] = 1
        else:
            i += 1
            v1 = int(sorted_ds_g1[i][0])
            v2 = int(sorted_ds_g2[i][0])
            pi[u1, v2] = 1
            pi[v1, u2] = 1

        i += 1
    return pi

# --------------------------------------------------------------------------- #
#                 Refinement by Swapping Pairs (Baseline)                     #
# --------------------------------------------------------------------------- #
def pairwise_refine(g1, g1_node_list, pi, mapping, C, D, objective, max_iter = 300):
    for z in range(max_iter):
    # random sample 30 nodes from the graph
        V_1 = []
        for _ in range(30):
            rand = random.uniform(0, len(g1))
            V_1.append(g1_node_list[int(rand)])

        for i1 in range(len(V_1)-1):
            u1 = V_1[i1]
            # we don't include vertices in V_1 in the neighborhood
            n1 = set(g1.neighbors(u1))
            n1 = list(n1 - set(V_1))
            for j1 in range(i1 + 1):
                v1 = V_1[j1]
                u2 = mapping[u1]
                v2 = mapping[v1]
                old_part_1 = C[u1, v1] * D[u2, v2]
                new_part_1 = C[u1, v1] * D[v2, u2]

                new_part_2 = 0
                for n in n1:
                    new_part_2 += C[u1, n] * D[v2, mapping[n]]
                old_part_2 = 0
                for n in n1:
                    old_part_2 += C[u1, n] * D[u2, mapping[n]]

                n2 = set(g1.neighbors(v1))
                n2 = list(n2 - set(V_1))

                new_part_3 = 0
                for n in n2:
                    new_part_3 += C[v1, n] * D[u2, mapping[n]]
                old_part_3 = 0
                for n in n2:
                    old_part_3 += C[v1, n] * D[v2, mapping[n]]

                if (new_part_1 + new_part_2 + new_part_3) < (old_part_1 + old_part_2 + old_part_3):
                    objective = objective - (old_part_1 + old_part_2 + old_part_3) + (new_part_1 + new_part_2 + new_part_3)
                    mapping[u1] = v2
                    mapping[v1] = u2
                    pi[u1, u2] = 0
                    pi[u1, v2] = 1
                    pi[v1, v2] = 0
                    pi[v1, u2] = 1
    return mapping, pi

# # ------------------------------------------- #
# #                 Ising Solver                #
# # ------------------------------------------- #
# def solve_ising(B, bias):

#     mdl = Model()
#      # note that B is the sub-matrix
#     n = B.shape[0]

#     # dict of bianry decision variables, format: {i : bdv_i}
#     x = {i: mdl.binary_var(name='x_{0}'.format(i)) for i in range(n)}

#     # objective function
#     # (2 * x[i] - 1) * (2 * x[j] - 1): s_i \in {-1,+1}
#     couplers_func =  mdl.sum(B[i,j] * x[i] * x[j] for i in range(n) for j in range(n)) # s_i \in {0,1}
#     bias_func = mdl.sum(float(bias[i]) * x[i] for i in range(n))
#     ising_func = couplers_func + bias_func

#     mdl.minimize(ising_func)
#     solution = mdl.solve()
#     cplex_solution = solution.get_all_values()

#     # print('CPLEX solution: ', [int(1-2*i) for i in cplex_solution])  s_i \in {-1,+1}
#     # print('CPLEX solution: ', cplex_solution)
#     return cplex_solution

# -------------------------------------------------- #
#                     IsoRank                        #
# -------------------------------------------------- #
def IsoRank(A1, A2, tol = 0.000005, max_iter = 500, H = None):
	# Shapes of two matrices
	n1 = A1.shape[0]
	n2 = A2.shape[0]

	# Normalization of adjacency matrix
	row_sum_1 = np.zeros((n1, 1), np.float64)
	row_sum_2 = np.zeros((n2, 1), np.float64)

	for i in range(n1):
		row_sum_1[i, 0] = 1/np.sum(A1[i])
		row_sum_2[i, 0] = 1/np.sum(A2[i])

	W1 = np.multiply(row_sum_1, A1)
	W2 = np.multiply(row_sum_2, A2)

	# Inilization of similarity matrix
	S = np.full((n2, n1), 1/(n1 * n2))

	# Prior similarity matrix
	if not H:
		H = S

	# Main iterations
	for i in range(max_iter):
		prev = S
		W2_t = np.transpose(W2)
		M1 = np.matmul(W2_t, S)
		M2 = np.matmul(M1, W1)
		S = 0.5 * M2 + 0.5 * H
		delta = np.linalg.norm(S - prev)
		if delta < tol:
			print("Total number of iterations: {}".format(i))
			break
		print("One itration complete")

	return S


# ------------------------------------------------- #
#        Initial Solution with Naive Sorting        #
# ------------------------------------------------- #
def initial_solution_naive_sorting(S, b, g1, g2, max_iter):
	# the sizes of two networks
	g1_size = len(g1)
	g2_size = len(g2)

	#--------------------------------------- #
	#          Iteration starts here         #
	#--------------------------------------- #
	for _ in range(max_iter):
		# ------------------------
		#       new S and b      -
		# ------------------------
		b_new = -np.ones(((g1_size + g2_size), 1), np.float64)
		S_new = np.empty((g1_size, g2_size), np.float64) # the only time we use S_new is assignment, therefore, its initial value doesn't matter

		# NOTE: for b and b_new, the index of u is u + g1_size
		for i in g1.nodes():
			for u in g2.nodes():
				# ---------------------------------------
				#    The complete bipartite graph       -
				# ---------------------------------------
				# Instead of constructing the actural graph (which is costly), we create a dictionary B with the format:
				# {(j, v) : weight}
				B = []
				neighbors_of_i = {}
				neighbors_of_u = {}
				for j in g1.neighbors(i):
					for v in g2.neighbors(u):
						B.append(((j,v), S[j,v]))
						neighbors_of_i[j] = 0
						neighbors_of_u[v] = 0
				
				# format (list of tuples): [ ( (j, v), weight ) ]
				sorted_B = sorted(B, key=lambda x: x[1], reverse = True)
				
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
	return S

# Search Term: ises
# -------------------------------------------------- #
#          Initial Solution Enhacned Sorting         #
# -------------------------------------------------- #
def initial_solution_enhanced(S, b_g1, b_g2, g1, g2, g1_neighbor_sequence, g2_neighbor_sequence, g1_degree_sequence, g2_degree_sequence, g1_size, g2_size, max_iter, cut_off):
    #--------------------------------------- #
	#          Iteration starts here         #
	#--------------------------------------- #
    for num_of_iter in range(max_iter):
        # -----------------------#
		#       new S and b      #
        # -----------------------#
        sum_b_g1 = [0.0] * g1_size
        sum_b_g2 = [0.0] * g2_size
        for i in g1.nodes():
            for nei in g1.neighbors(i):
                sum_b_g1[i] += b_g1[nei]
        for u in g2.nodes():
            for nei in g2.neighbors(u):
                sum_b_g2[u] += b_g2[nei]

        b_g1_new = [0.0] * g1_size
        b_g2_new = [0.0] * g2_size
        S_new = [[None for u in range(g2_size)] for i in range(g1_size)] # the only time we use S_new is assignment, therefore, its initial value doesn't matter
        
        # Iterate over all paris
        for i in g1.nodes():
            for u in g2.nodes():
                B = []
                c = 0 # sum
                g1_is_deleted = [0] * g1_degree_sequence[i]
                g2_is_deleted = [0] * g2_degree_sequence[u]

                # Iterate over neighborhood
                for j_index in range(g1_degree_sequence[i]):
                    for v_index in range(g2_degree_sequence[u]):
                        if not g2_is_deleted[v_index]:
                            j = g1_neighbor_sequence[i][j_index]
                            v = g2_neighbor_sequence[u][v_index]
                            if S[j][v] == b_g1[j] == b_g2[v]:
                                c += S[j][v]
                                g1_is_deleted[j_index] = 1
                                g2_is_deleted[v_index] = 1
                                break
                            elif (num_of_iter <= cut_off):
                                B.append( ((j_index,v_index), S[j][v]) )
                            elif (S[j][v] == b_g1[j] < b_g2[v]) or (S[j][v] == b_g2[v] < b_g1[j]):
                                B.append( ((j_index,v_index), S[j][v]) )

                # Sort B by weight
                sorted_B = sorted(B, key=lambda x: x[1], reverse = True)
                
                # if not empty
                if sorted_B:
                    for pair in sorted_B:
                        if pair[1] > 0:
                            j_index = pair[0][0]
                            v_index = pair[0][1]
                            if (not g1_is_deleted[j_index]) and (not g2_is_deleted[v_index]):
                                j = g1_neighbor_sequence[i][j_index]
                                v = g2_neighbor_sequence[u][v_index]
                                larger = max(b_g1[j], b_g2[v])
                                c += 2 * pair[1] - larger
                                g1_is_deleted[j_index] = 1
                                g2_is_deleted[v_index] = 1

                # Compute the updated similarity
                maxi = max(sum_b_g1[i], sum_b_g2[u])
                S_new[i][u] = c / maxi

                if S_new[i][u] > b_g1_new[i]:
                    b_g1_new[i] = S_new[i][u]
                if S_new[i][u] > b_g2_new[u]:
                    b_g2_new[u] = S_new[i][u]
    
        # ------ #
        # Update #
        # ------ #
        b_g1 = b_g1_new
        b_g2 = b_g2_new
        S = S_new

    return S

# --------------------------------------------------------- #
#          Initial Solution Enhacned Sorting Testing        #
# --------------------------------------------------------- #
# @jit(nopython=True)
def initial_solution_enhanced_testing(S, b_g1, b_g2, g1_neighbor_sequence, g2_neighbor_sequence, g1_degree_sequence, g2_degree_sequence, g1_size, g2_size, max_iter, g1_node_coverage_percentage, g2_node_coverage_percentage):
    #--------------------------------------- #
	#          Iteration starts here         #
	#--------------------------------------- #
    for num_of_iter in range(max_iter):
        #------------------ #
        #      Sum of b     #
        #------------------ #
        sum_b_g1 = [0.0] * g1_size
        sum_b_g2 = [0.0] * g2_size
        for i in range(g1_size):
            for nei in g1_neighbor_sequence[i]:
                sum_b_g1[i] += b_g1[nei]
        for u in range(g2_size):
            for nei in g2_neighbor_sequence[u]:
                sum_b_g2[u] += b_g2[nei]

        # -----------------------#
		#       new S and b      #
        # -----------------------#
        b_g1_new = [0.0] * g1_size
        b_g2_new = [0.0] * g2_size
        S_new = [[None for u in range(g2_size)] for i in range(g1_size)] # the only time we use S_new is assignment, therefore, its initial value doesn't matter
        
        # Iterate over all paris
        for i in range(g1_size):
            for u in range(g2_size):
                B = []
                c = 0 # sum
                g1_is_deleted = [0] * g1_degree_sequence[i]
                g2_is_deleted = [0] * g2_degree_sequence[u]

                # Iterate over neighborhood
                for j_index in range(g1_degree_sequence[i]):
                    for v_index in range(g2_degree_sequence[u]):
                        if not g2_is_deleted[v_index]:
                            j = g1_neighbor_sequence[i][j_index]
                            v = g2_neighbor_sequence[u][v_index]
                            if S[j][v] == b_g1[j] == b_g2[v]:
                                c += S[j][v]
                                g1_is_deleted[j_index] = 1
                                g2_is_deleted[v_index] = 1
                                break
                            elif (S[j][v] >= g1_node_coverage_percentage[j][num_of_iter] * b_g1[j]) or (S[j][v] >= g2_node_coverage_percentage[v][num_of_iter] * b_g2[v]):
                                B.append( ((j_index,v_index), S[j][v]) )

                # Sort B by weight
                sorted_B = sorted(B, key=lambda x: x[1], reverse = True)
                
                # if not empty
                if sorted_B:
                    for pair in sorted_B:
                        if pair[1] > 0:
                            j_index = pair[0][0]
                            v_index = pair[0][1]
                            if (not g1_is_deleted[j_index]) and (not g2_is_deleted[v_index]):
                                j = g1_neighbor_sequence[i][j_index]
                                v = g2_neighbor_sequence[u][v_index]
                                discrepancy = 0
                                if (pair[1] != b_g1[j]) and (pair[1] != b_g2[v]) and (pair[1] >= g1_node_coverage_percentage[j][num_of_iter]*b_g1[j]) and (pair[1] >= g2_node_coverage_percentage[v][num_of_iter]*b_g2[v]):
                                    c += pair[1]
                                else:
                                    if pair[1] == b_g1[j]:
                                        discrepancy = b_g2[v]
                                    elif pair[1] == b_g2[v]:
                                        discrepancy = b_g1[j]
                                    elif pair[1] < g1_node_coverage_percentage[j][num_of_iter]*b_g1[j]:
                                        # larger: j, smaller: v
                                        discrepancy = (1 - (pair[1] - g2_node_coverage_percentage[v][num_of_iter] * b_g2[v]) / (b_g2[v] - g2_node_coverage_percentage[v][num_of_iter] * b_g2[v])) * g1_node_coverage_percentage[j][num_of_iter] * b_g1[j] + (pair[1] - g2_node_coverage_percentage[v][num_of_iter] * b_g2[v]) / (b_g2[v] - g2_node_coverage_percentage[v][num_of_iter] * b_g2[v]) * b_g1[j]
                                    else:
                                        # larger: v, smaller: v
                                        discrepancy = (1 - (pair[1] - g1_node_coverage_percentage[j][num_of_iter] * b_g1[j]) / (b_g1[j] - g1_node_coverage_percentage[j][num_of_iter] * b_g1[j])) * g2_node_coverage_percentage[v][num_of_iter] * b_g2[v] + (pair[1] - g1_node_coverage_percentage[j][num_of_iter] * b_g1[j]) / (b_g1[j] - g1_node_coverage_percentage[j][num_of_iter] * b_g1[j]) * b_g2[v]
                                    #? Should I consider the discrepancy or not? 
                                    # c += pair[1] 
                                    c += 2 * pair[1] - discrepancy
                                g1_is_deleted[j_index] = 1
                                g2_is_deleted[v_index] = 1

                # Compute the updated similarity
                maxi = max(sum_b_g1[i], sum_b_g2[u])
                if maxi == 0:
                    S_new[i][u] = 0
                else:
                    S_new[i][u] = c / maxi

                if S_new[i][u] > b_g1_new[i]:
                    b_g1_new[i] = S_new[i][u]
                if S_new[i][u] > b_g2_new[u]:
                    b_g2_new[u] = S_new[i][u]
        # ------ #
        # Update #
        # ------ #
        b_g1 = b_g1_new
        b_g2 = b_g2_new
        S = S_new
    return S

# ------------------------------------------------- #
#          Initial Solution Fast Approximation      #
# ------------------------------------------------- #
def initial_solution_apprximation(S, b, g1, g2, max_iter):
	# the sizes of two networks
	g1_size = len(g1)
	g2_size = len(g2)

	#--------------------------------------- #
	#          Iteration starts here         #
	#--------------------------------------- #
	for _ in range(max_iter):
		# -----------------------#
		#       new S and b      #
		# -----------------------#
		b_new = -np.ones(((g1_size + g2_size), 1), np.float64)
		S_new = np.empty((g1_size, g2_size), np.float64) # the only time we use S_new is assignment, therefore, its initial value doesn't matter

		# NOTE: for b and b_new, the index of u is u + g1_size
		for i in g1.nodes():
			for u in g2.nodes():
				c = 0 # sum
				is_deleted = defaultdict(lambda : 0)
				# Iterate all pairs of neighbors
				for j in g1.neighbors(i):
					for v in g2.neighbors(u):
						if (not is_deleted[v]) and ( (S[j,v] == b[j]) or (S[j,v] == b[v + g1_size])):
							larger = max(b[j], b[v + g1_size])
							c += 2 * S[j,v] - larger
							is_deleted[v] = 1
							break

				# Compute the updated similarity
				maxi = max(len(list(g1.neighbors(i))), len(list(g2.neighbors(u))))
				S_new[i,u] = c / maxi
				if S_new[i,u] > b_new[i]:
					b_new[i] = S_new[i,u]
				if S_new[i,u] > b_new[u + g1_size]:
					b_new[u + g1_size] = S_new[i,u]

		# ------ #
		# Update #
		# ------ #
		b = b_new
		S = S_new
	return S


# --------------------------------------------------------------- #
#           Compute Violation (number of unmapped edges)          #
# --------------------------------------------------------------- #

def compute_violation(g1, g2, C, D, mapping, gt_mapping):
    vilation = 0      
    for i1 in range(len(g1)):
        i2 = mapping[i1]
        for j1 in range(len(g1)):
            j2 = mapping[j1]
            if C[i1, j1] == 1:
                if D[i2, j2] == 0:
                    count += 1
            if C[i1, j1] == 0:
                if D[i2, j2] == 1:
                    count += 1
                    
    print("Initial violations: {} (0 violation indicates isomorphic mappings)".format(count/2))