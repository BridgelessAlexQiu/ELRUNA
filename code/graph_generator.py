# import numpy as np
# import networkx as nx
# import random
# import utility as uti
# import cProfile
# import timeit
# import math
# from collections import defaultdict
# import matplotlib.pyplot as plt
# import copy

# # --------------------------------- #
# #           Random Graphs           #
# # --------------------------------- #
# random_graph_types = ["homle", "barabasi", "erdos", "watts", "regular"]
# # path: networks/random_networks/name
# for random_graph in random_graph_types:
# 	g1 = uti.construct_random_graph(random_graph, n = 200)
# 	g1 = nx.convert_node_labels_to_integers(g1) # relabel nodes as integers from 0 to ...
# 	g1.remove_edges_from(g1.selfloop_edges()) # remove loops

# 	g1_node_list = np.asarray(g1.nodes()) # list of node ids, starts from 0
# 	g2_node_list = np.random.permutation(g1_node_list) # random permutation of the list of node id

# 	# Construct the ground truth mapping
# 	gt_mapping = dict()
# 	for i in range(len(g1_node_list)):
# 			gt_mapping[g1_node_list[i]] = g2_node_list[i]

# 	# Construct the ground truth inverse mapping
# 	gt_inverse_mapping = dict()
# 	for i in range(len(g2_node_list)):
# 		gt_inverse_mapping[g2_node_list[i]] = g1_node_list[i]

# 	g2 = nx.relabel_nodes(g1, gt_mapping)
	
# 	if random_graph != "regular":
# 		g1_file_name = "networks/random_networks/" + random_graph + '/edgelist/' + random_graph + '_g1.edgelist'
# 		nx.write_edgelist(g1, g1_file_name, data = False)

# 		perturbation_probability = [0, 0.001, 0.003, 0.005, 0.007, 0.009, 0.011, 0.013, 0.015]
# 		for p in perturbation_probability:
# 			g2_copy = copy.deepcopy(g2)# deep copy of g2
# 			total_number_of_added_edges = 0
# 			for i in g2_copy.nodes():
# 				for j in g2_copy.nodes():
# 					if i != j:
# 						random_number = random.uniform(1, 1000)
# 						if (int(random_number) <= 1000 * p) and (not g2_copy.has_edge(i, j)):
# 							total_number_of_added_edges += 1
# 							g2_copy.add_edge(i,j)
# 			# -------------------------- #
# 			#        Edgelist File       #
# 			# -------------------------- #
# 			g2_file_name = "networks/random_networks/" + random_graph + '/edgelist/' + random_graph + '_' + str(p) + '_g2.edgelist'
# 			nx.write_edgelist(g2_copy, g2_file_name, data = False)
# 	else:
# 		# -------------------------- #
# 		#        Edgelist File       #
# 		# -------------------------- #
# 		g1_file_name = "networks/random_networks/" + random_graph + '/edgelist/' + random_graph + '_g1.edgelist'
# 		g2_file_name = "networks/random_networks/" + random_graph + '/edgelist/' + random_graph + '_g2.edgelist'	
# 		nx.write_edgelist(g1, g1_file_name, data = False)
# 		nx.write_edgelist(g2, g2_file_name, data = False)


