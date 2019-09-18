import networkx as nx
# in_file_obj = open("worm_net_g1_weighted.edges", 'r')
# out_file_obj = open("worm_net_g1.edges", 'w')

# for line in in_file_obj:
#     i = line.split(' ')[0]
#     j = line.split(' ')[1]
#     out_file_obj.write(i + ' ' + j + '\n')

# in_file_obj.close()
# out_file_obj.close()

# --------------------------------- #
#           Real Networks           #
# --------------------------------- #
# path: networks/random_networks/name
g1 = nx.read_edgelist("worm_net_g1.edges")

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

# ---------------------------- #
#           LCC info           #
# ---------------------------- #

print(nx.info(g1))
print("The diameter: {}".format(nx.diameter(g1)))

# ------------------------------------------- #
#          Write to the .edges file           #
# ------------------------------------------- #
g1_file_name = "worm_net_g1_lcc.edges"
nx.write_edgelist(g1, g1_file_name, data = False)