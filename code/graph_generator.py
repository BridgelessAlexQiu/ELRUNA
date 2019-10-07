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
#     g1 = uti.construct_random_graph(random_graph, n = 400)
#     g1 = nx.convert_node_labels_to_integers(g1) # relabel nodes as integers from 0 to ...
#     g1.remove_edges_from(g1.selfloop_edges()) # remove loops

#     g1_node_list = np.asarray(g1.nodes()) # list of node ids, starts from 0
#     g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

#     g1_size = len(g1)

#     print(random_graph + ":", nx.diameter(g1))

#     # Construct the ground truth mapping
#     gt_mapping = dict()
#     for i in range(len(g1_node_list)):
#             gt_mapping[g1_node_list[i]] = g2_node_list[i]

#     # Construct the ground truth inverse mapping
#     gt_inverse_mapping = dict()
#     for i in range(len(g2_node_list)):
#         gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

#     gt_file_name = "c/datasets/random_network/" + random_graph + '/' + random_graph + '_gt_mapping.txt' 
#     gt_file = open(gt_file_name, 'w')
#     for i, u in gt_mapping.items():
#         line = str(i) + " " + str(u) + "\n"
#         gt_file.write(line)
#     gt_file.close()

#     g1_file_name = "c/datasets/random_network/" + random_graph + '/' + random_graph + '_g1.edgelist'
#     nx.write_edgelist(g1, g1_file_name, data = False)

#     if random_graph != "regular":
#         perturbation_probability = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21]
#         for p in perturbation_probability:
#             additional_edges = int(g1.number_of_edges() * p)
#             g2 = nx.relabel_nodes(g1, gt_mapping)
#             while additional_edges != 0:
#                 i = np.random.randint(0, len(g1))
#                 j = np.random.randint(0, len(g1))
#                 if i != j and (not g2.has_edge(i, j)):
#                     g2.add_edge(i,j)
#                     additional_edges -= 1
#             # -------------------------- #
#             #        Edgelist File       #
#             # -------------------------- #
#             g2_file_name = "c/datasets/random_network/" + random_graph + '/'+ random_graph + '_' + str(p) + '_g2.edgelist'
#             nx.write_edgelist(g2, g2_file_name, data = False)
#     else:
#         g2 = nx.relabel_nodes(g1, gt_mapping)
#         # -------------------------- #
#         #        Edgelist File       #
#         # -------------------------- #
#         g2_file_name = "c/datasets/random_network/" + random_graph + '/' + random_graph + '_g2.edgelist'	
#         nx.write_edgelist(g2, g2_file_name, data = False)


# # --------------------------------- #
# #           Real Networks           #
# # --------------------------------- #
# # path: networks/random_networks/name
# g1 = nx.read_gml("dataset/newman_netscience.gml")
# # ------------------------------------- #
# #         Extract the Largest CC        #
# # ------------------------------------- #
# largest_cc = max(nx.connected_components(g1), key=len)
# g1 = g1.subgraph(largest_cc)

# # -------------------------------------------------------- #
# #      Relabel the Network with Consecutive Integers       #
# # -------------------------------------------------------- #
# g1 = nx.convert_node_labels_to_integers(g1)

# # --------------------------------------------- #
# #                  Remove Loops                 #
# # --------------------------------------------- #
# g1.remove_edges_from(g1.selfloop_edges())

# # ---------------------------------------------- #
# #       Construct the Ground Truth Mapping       #
# # ---------------------------------------------- #
# g1_node_list = np.asarray(g1.nodes())
# g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

# # Construct the ground truth mapping
# gt_mapping = dict()
# for i in range(len(g1_node_list)):
#         gt_mapping[g1_node_list[i]] = g2_node_list[i]

# # Construct the ground truth inverse mapping
# gt_inverse_mapping = dict()
# for i in range(len(g2_node_list)):
#     gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

# gt_file_name = "networks/real_networks/newman_netscience/edgelist/newman_netscience_gt_mapping.txt" 
# gt_file = open(gt_file_name, 'w')
# for i, u in gt_mapping.items():
#     line = str(i) + " " + str(u) + "\n"
#     gt_file.write(line)
# gt_file.close()

# g1_file_name = "networks/real_networks/newman_netscience/edgelist/newman_netscience_g1.edgelist"
# nx.write_edgelist(g1, g1_file_name, data = False)

# perturbation_probability = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35, 0.37, 0.39, 0.41, 0.43, 0.45]
# for p in perturbation_probability:
#     additional_edges = int(g1.number_of_edges() * p)
#     g2 = nx.relabel_nodes(g1, gt_mapping)
#     while additional_edges != 0:
#         i = np.random.randint(0, len(g1))
#         j = np.random.randint(0, len(g1))
#         if i != j and (not g2.has_edge(i, j)):
#             g2.add_edge(i,j)
#             additional_edges -= 1
#     # -------------------------- #
#     #        Edgelist File       #
#     # -------------------------- #
#     g2_file_name = "networks/real_networks/newman_netscience/edgelist/newman_netscience_" + str(p) + '_g2.edgelist'
#     nx.write_edgelist(g2, g2_file_name, data = False)