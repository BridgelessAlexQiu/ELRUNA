import networkx as nx 
import numpy as np 
import scipy as sp 
from scipy.linalg import block_diag
from scipy import sparse
import sys

# --------- command-line arg --------- #
network_type = sys.argv[1]
network_label = sys.argv[2]

# --------- noises --------- #
vector_p = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"]

print("{} network".format(network_label))

# ----------------- #
#        G1         #
# ----------------- #
g1_network_file_name = ""

if network_label != "newman" and network_type != "random_network":
    g1_network_file_name = "../../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.edges"
else:
    g1_network_file_name = "../../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.edgelist"

g1 = nx.read_edgelist(g1_network_file_name) # G1

# ------------------------- #
#         G1 nodelist       #
# ------------------------- #
g1_nodelist_file_name = "../node_list/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_g1.txt"

g1_nodelist_file = open(g1_nodelist_file_name, 'r')
g1_nodelist = []
for line in g1_nodelist_file:
    g1_nodelist.append(line.split('\n')[0])
g1_nodelist_file.close()

# ------ A ------#
A = nx.adjacency_matrix(g1, g1_nodelist) # adj matrix of G1
A = A.todense()


for p in vector_p:
    # ----------------- #
    #        G2         #
    # ----------------- #
    g2_network_file_name = ""
    if network_label != "newman" and network_type != "random_network":
        g2_network_file_name = "../../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.edges"
    else:
        g2_network_file_name = "../../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.edgelist"
        if network_type == "random_network" and p == "0.23":
            sys.exit(0)
    g2 = nx.read_edgelist(g2_network_file_name) # G2

    # ------------------------- #
    #         G2 nodelist       #
    # ------------------------- #
    g2_nodelist_file_name = "../node_list/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + "_g2.txt"
    g2_nodelist_file = open(g2_nodelist_file_name, 'r')
    g2_nodelist = []
    for line in g2_nodelist_file:
        g2_nodelist.append(line.split('\n')[0])
    g2_nodelist_file.close()

    # ------- B ------- #
    B = nx.adjacency_matrix(g2, g2_nodelist) # adj matrix of G2
    B = B.todense()

    # ----------------- #
    #        G3         #
    # ----------------- #
    C = block_diag(A, B) # the merged matrix
    g3 = nx.from_numpy_matrix(C)
    g3_file_name = "../datasets/self_under_noise/" + network_type + "/" + network_label + "/" + network_label + "_" + p + ".txt"
    nx.write_edgelist(g3, g3_file_name)
    
    

    




    