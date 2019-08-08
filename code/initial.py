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
