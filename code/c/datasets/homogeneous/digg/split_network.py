import networkx as nx

# -------------------------- #
#      Original Network      #
# -------------------------- #
G_full = nx.read_edgelist("digg_full.edges", nodetype = int)
print("Full network info:")
print(nx.info(G_full))
print("\n")

# --------------------------- #
#       Induced Subgraph      #
# --------------------------- #
node_subset_1 = list(range(3000, 7500))
node_subset_2 = list(range(4500, 12500))

g1 = G_full.subgraph(node_subset_1)
g2 = G_full.subgraph(node_subset_2)

# ------------------------------------- #
#         Extract the Largest CC        #
# ------------------------------------- #
largest_cc_g1 = max(nx.connected_components(g1), key=len)
g1 = g1.subgraph(largest_cc_g1)

largest_cc_g2 = max(nx.connected_components(g2), key=len)
g2 = g2.subgraph(largest_cc_g2)

print("Network Info of g1:")
print(nx.info(g1))
#print("diameter: {}".format(nx.diameter(g1))) # Taking too long
print("\n")


print("Network Info of g2:")
print(nx.info(g2))
#print("diameter: {}".format(nx.diameter(g2)))
print("\n")


set_1 = set(g1.nodes())
set_2 = set(g2.nodes())
print("Number of node overlapping:")
print(len(set_1.intersection(set_2)))

#-------------------------------------------------------- #
#     Relabel the Network with Consecutive Integers       #
#-------------------------------------------------------- #
g1 = nx.convert_node_labels_to_integers(g1)
g2 = nx.convert_node_labels_to_integers(g2)

nx.write_edgelist(g1, "digg_g1.edges", data=False)
nx.write_edgelist(g2, "digg_g2.edges", data=False)