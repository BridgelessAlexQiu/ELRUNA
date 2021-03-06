import networkx as nx
import numpy as np
#------------------------------------ #
#            Remove weights           #
#------------------------------------ #
in_file_obj = open("facebook_raw.facebook-wosn-links", 'r')
out_file_obj = open("facebook_cleaned.edges", 'w')

for line in in_file_obj:
    i = line.split(' ')[0]
    j = line.split(' ')[1]
    out_file_obj.write(i + ' ' + j + '\n')

in_file_obj.close()
out_file_obj.close()

# --------------------------------- #
#           Real Networks           #
# --------------------------------- #
g1 = nx.read_edgelist("facebook_cleaned.edges")

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
g1_file_name = "facebook_full.edges"
nx.write_edgelist(g1, g1_file_name, data = False)
