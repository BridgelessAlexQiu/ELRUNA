import networkx as nx
import numpy as np
#------------------------------------ #
#            Remove weights           #
#------------------------------------ #
in_file_obj = open("social_raw.arenas-pgp", 'r')
out_file_obj = open("social.edges", 'w')

for line in in_file_obj:
    i = line.split(' ')[0]
    j = line.split(' ')[1]
    out_file_obj.write(i + ' ' + j)

in_file_obj.close()
out_file_obj.close()

# --------------------------------- #
#           Real Networks           #
# --------------------------------- #
g1 = nx.read_edgelist("social.edges")

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
g1.remove_edges_from(nx.selfloop_edges(g1))

# ---------------------------- #
#           LCC info           #
# ---------------------------- #
print(nx.info(g1))
# print("The diameter: {}".format(nx.diameter(g1)))

# ---------------------------------------------- #
#          Write g1 to the .edges file           #
# ---------------------------------------------- #
g1_file_name = "social_g1.edges"
nx.write_edgelist(g1, g1_file_name, data = False)

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

# ---------------------------------------------------- #
#          Write gt_mapping to the .txt file           #
# ---------------------------------------------------- #
gt_file_name = "social_gt_mapping.txt"
gt_file = open(gt_file_name, 'w')
for i, u in gt_mapping.items():
    line = str(i) + " " + str(u) + "\n"
    gt_file.write(line)
gt_file.close()

perturbation_probability = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25]
for p in perturbation_probability:
    additional_edges = int(g1.number_of_edges() * p)
    g2 = nx.relabel_nodes(g1, gt_mapping)
    while additional_edges != 0:
        i = np.random.randint(0, len(g1))
        j = np.random.randint(0, len(g1))
        if i != j and (not g2.has_edge(i, j)):
            g2.add_edge(i,j)
            additional_edges -= 1

    # -------------------------- #
    #        Edgelist File       #
    # -------------------------- #
    g2_file_name = "social_" + str(p) + '_g2.edges'
    nx.write_edgelist(g2, g2_file_name, data = False)
