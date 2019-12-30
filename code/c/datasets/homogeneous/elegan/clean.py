import networkx as nx
import numpy as np

#------------------------------------ #
#            Remove weights           #
#------------------------------------ #
in_file_obj = open("elegan_g1_raw.edges", 'r')
out_file_obj = open("elegan_g1_unweighted.edges", 'w')

for line in in_file_obj:
    i = line.split(' ')[0]
    j = line.split(' ')[1]
    out_file_obj.write(i + ' ' + j + '\n')

in_file_obj.close()
out_file_obj.close()


in_file_obj = open("elegan_g2_raw.edges", 'r')
out_file_obj = open("elegan_g2_unweighted.edges", 'w')

for line in in_file_obj:
    i = line.split(' ')[0]
    j = line.split(' ')[1]
    out_file_obj.write(i + ' ' + j + '\n')

in_file_obj.close()
out_file_obj.close()


# --------------------------------- #
#           Real Networks           #
# --------------------------------- #
g1 = nx.read_edgelist("elegan_g1_unweighted.edges")
g2 = nx.read_edgelist("elegan_g2_unweighted.edges")

# ------------------------------------- #
#         Extract the Largest CC        #
# ------------------------------------- #
largest_cc_g1 = max(nx.connected_components(g1), key=len)
g1 = g1.subgraph(largest_cc_g1)

largest_cc_g2 = max(nx.connected_components(g2), key=len)
g2 = g2.subgraph(largest_cc_g2)

# -------------------------------------------------------- #
#      Relabel the Network with Consecutive Integers       #
# -------------------------------------------------------- #
g1 = nx.convert_node_labels_to_integers(g1)
g2 = nx.convert_node_labels_to_integers(g2)

# --------------------------------------------- #
#                  Remove Loops                 #
# --------------------------------------------- #
g1.remove_edges_from(g1.selfloop_edges())
g2.remove_edges_from(g2.selfloop_edges())

# ---------------------------- #
#           LCC info           #
# ---------------------------- #
print(nx.info(g1))
print("The diameter: {}".format(nx.diameter(g1)))

print(nx.info(g2))
print("The diameter: {}".format(nx.diameter(g2)))

# ---------------------------------------------- #
#          Write g1 to the .edges file           #
# ---------------------------------------------- #
g1_file_name = "elegan_g1.edges"
nx.write_edgelist(g1, g1_file_name, data = False)

g2_file_name = "elegan_g2.edges"
nx.write_edgelist(g2, g2_file_name, data = False)
