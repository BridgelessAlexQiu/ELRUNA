import numpy as np
import networkx as nx
import random
import utility as uti
import cProfile
import timeit
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import copy

# # --------------------------------- #
# #           Random Graphs           #
# # --------------------------------- #
# random_graph_types = ["homle", "barabasi", "erdos", "watts", "regular"]
# # path: networks/random_networks/name
# for random_graph in random_graph_types:
#     g1 = uti.construct_random_graph(random_graph, n = 200)
#     g1 = nx.convert_node_labels_to_integers(g1) # relabel nodes as integers from 0 to ...
#     g1.remove_edges_from(g1.selfloop_edges()) # remove loops

#     g1_node_list = np.asarray(g1.nodes()) # list of node ids, starts from 0
#     g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

#     # Construct the ground truth mapping
#     gt_mapping = dict()
#     for i in range(len(g1_node_list)):
#             gt_mapping[g1_node_list[i]] = g2_node_list[i]

#     # Construct the ground truth inverse mapping
#     gt_inverse_mapping = dict()
#     for i in range(len(g2_node_list)):
#         gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

#     gt_file_name = "networks/random_networks/" + random_graph + '/edgelist/'+ random_graph + '_gt_mapping.txt' 
#     gt_file = open(gt_file_name, 'w')
#     for i, u in gt_mapping.items():
#         line = str(i) + " " + str(u) + "\n"
#         gt_file.write(line)
#     gt_file.close()

#     g1_file_name = "networks/random_networks/" + random_graph + '/edgelist/' + random_graph + '_g1.edgelist'
#     nx.write_edgelist(g1, g1_file_name, data = False)

#     if random_graph != "regular":
#         perturbation_probability = [0, 0.001, 0.0011, 0.0012, 0.0013, 0.0014, 0.0015, 0.0016, 0.003, 0.005, 0.007, 0.009, 0.0091, 0.0092, 0.0093, 0.0094, 0.0095, 0.011, 0.013, 0.015]
#         for p in perturbation_probability:
#             g2 = nx.relabel_nodes(g1, gt_mapping)
#             total_number_of_added_edges = 0
#             for i in g2.nodes():
#                 for j in g2.nodes():
#                     if i != j:
#                         random_number = random.uniform(1, 1000)
#                         if (int(random_number) <= 1000 * p) and (not g2.has_edge(i, j)):
#                             total_number_of_added_edges += 1
#                             g2.add_edge(i,j)
#             # -------------------------- #
#             #        Edgelist File       #
#             # -------------------------- #
#             g2_file_name = "networks/random_networks/" + random_graph + '/edgelist/' + random_graph + '_' + str(p) + '_g2.edgelist'
#             nx.write_edgelist(g2, g2_file_name, data = False)
#     else:
#         g2 = nx.relabel_nodes(g1, gt_mapping)
#         # -------------------------- #
#         #        Edgelist File       #
#         # -------------------------- #
#         g2_file_name = "networks/random_networks/" + random_graph + '/edgelist/' + random_graph + '_g2.edgelist'	
#         nx.write_edgelist(g2, g2_file_name, data = False)


# --------------------------------- #
#           Real Networks           #
# --------------------------------- #
# path: networks/random_networks/name
g1 = nx.read_gml("dataset/newman_netscience.gml")
# ------------------------------------- #
#         Extract the Largest CC        #
# ------------------------------------- #
largest_cc = max(nx.connected_components(g1), key=len)
g1 = g1.subgraph(largest_cc)

# -------------------------------------------------------- #
#      Relabel the Network with Consecutive Integers       #
# -------------------------------------------------------- #
g1 = nx.convert_node_labels_to_integers(g1)

# --------------------------------------------- #
#                  Remove Loops                 #
# --------------------------------------------- #
g1.remove_edges_from(g1.selfloop_edges())

# ---------------------------------------------- #
#       Construct the Ground Truth Mapping       #
# ---------------------------------------------- #
g1_node_list = np.asarray(g1.nodes())
g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

# Construct the ground truth mapping
gt_mapping = dict()
for i in range(len(g1_node_list)):
        gt_mapping[g1_node_list[i]] = g2_node_list[i]

# Construct the ground truth inverse mapping
gt_inverse_mapping = dict()
for i in range(len(g2_node_list)):
    gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

gt_file_name = "networks/real_networks/newman_netscience/edgelist/newman_netscience_gt_mapping.txt" 
gt_file = open(gt_file_name, 'w')
for i, u in gt_mapping.items():
    line = str(i) + " " + str(u) + "\n"
    gt_file.write(line)
gt_file.close()

g1_file_name = "networks/real_networks/newman_netscience/edgelist/newman_netscience_g1.edgelist"
nx.write_edgelist(g1, g1_file_name, data = False)

perturbation_probability = [0, 0.001, 0.0011, 0.0012, 0.0013, 0.0014, 0.0015, 0.002, 0.003, 0.005, 0.007, 0.009, 0.011, 0.013, 0.015]
for p in perturbation_probability:
    g2 = nx.relabel_nodes(g1, gt_mapping)
    total_number_of_added_edges = 0
    for i in g2.nodes():
        for j in g2.nodes():
            if i != j:
                random_number = random.uniform(1, 1000)
                if (int(random_number) <= 1000 * p) and (not g2.has_edge(i, j)):
                    total_number_of_added_edges += 1
                    g2.add_edge(i,j)
    # -------------------------- #
    #        Edgelist File       #
    # -------------------------- #
    g2_file_name = "networks/real_networks/newman_netscience/edgelist/newman_netscience_" + str(p) + '_g2.edgelist'
    nx.write_edgelist(g2, g2_file_name, data = False)