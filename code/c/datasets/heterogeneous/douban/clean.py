import networkx as nx
import numpy as np

name_1 = "offline"
name_2 = "online"

# --------------------------------- #
#           Real Networks           #
# --------------------------------- #
g1 = nx.read_edgelist(name_1 + "_raw.edges")
g2 = nx.read_edgelist(name_2 + "_raw.edges")

# ------------------------------------- #
#         Extract the Largest CC        #
# ------------------------------------- #
largest_cc_1 = max(nx.connected_components(g1), key=len)
largest_cc_2 = max(nx.connected_components(g2), key=len)
g1 = g1.subgraph(largest_cc_1)
g2 = g2.subgraph(largest_cc_2)

# -------------------------------------------------------- #
#      Relabel the Network with Consecutive Integers       #
# -------------------------------------------------------- #
g1 = nx.convert_node_labels_to_integers(g1)
g2 = nx.convert_node_labels_to_integers(g2)

# --------------------------------------------- #
#                  Remove Loops                 #
# --------------------------------------------- #
g1.remove_edges_from(nx.selfloop_edges(g1))
g2.remove_edges_from(nx.selfloop_edges(g2))

# ---------------------------- #
#           LCC info           #
# ---------------------------- #
print(name_1)
print(nx.info(g1))
print("The diameter: {}".format(nx.diameter(g1)))

print(name_2)
print(nx.info(g2))
print("The diameter: {}".format(nx.diameter(g2)))

# ---------------------------------------------- #
#          Write to the .edges file           #
# ---------------------------------------------- #
g1_file_name = name_1 + ".edges"
g2_file_name = name_2 + ".edges"
nx.write_edgelist(g1, g1_file_name, data = False)
nx.write_edgelist(g2, g2_file_name, data = False)
