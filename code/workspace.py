import utility as uti
import numpy as np
import networkx as nx
import random
from collections import defaultdict

#----------------------------------------Example graphs---------------------------------------
g1 = uti.construct_random_graph("barabasi_c")

#--------------------------------Construct the ground truth mapping----------------------------

g1_node_list = np.asarray(g1.nodes()) # list of node ids, starts from 0
g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

# Construct the ground truth mapping
gt_mapping = dict()
for i in range(len(g1_node_list)):
    gt_mapping[g1_node_list[i]] = g2_node_list[i]

# relabel the graph
g2 = nx.relabel_nodes(g1, gt_mapping)

#-----------------------------------Initial solution--------------------------------------------

# initial Permutation matrix
pi = uti.initial_solution(g1, g2, g1_node_list, 0.2) # the last parameter is the pertubation probability

# initial mapping, format (dict): {vertex in g1 : vertx in g2}
mapping = dict()
for i in range(len(g1)):
    for j in range(len(g2)):
        if pi[i, j] == 1:
            mapping[i] = j

matched_node = 0
for i in range(len(g1)):
    if gt_mapping[i] == mapping[i]:
        matched_node += 1
print("Initial mapping percentage: {}".format(matched_node / len(g1))) #0.6333333333333333

#----------------------------------------Initial Objective----------------------------------------------

# Cost matrix and Distance matrix
C = nx.to_numpy_matrix(g1, dtype = np.int8)
D = nx.to_numpy_matrix(g2, g1_node_list, dtype = np.int8) # the rows and columns are ordered according to the nodes in g1

# To make g2 complete, we connect pairs of vertices that are not adjacent with edges of weight 2
for i in range(len(g2)):
    for j in range(len(g2)):
        if D[i, j] == 0:
            D[i, j] = 2

# initial objective
objective = 0
for i1 in range(len(g1)):
    for j1 in range(len(g1)):
        i2 = mapping[i1]
        j2 = mapping[j1]
        objective += C[i1, j1] * D[i2, j2]

print("The initial objective value: {}".format(objective))

#----------------------------------------Refinement--------------------------------------------
max_iter = 200
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

matched_node = 0
for i in range(len(g1)):
    if gt_mapping[i] == mapping[i]:
        matched_node += 1
print("Final mapping percentage: {}".format(matched_node / len(g1))) # 0.9333333333333333

