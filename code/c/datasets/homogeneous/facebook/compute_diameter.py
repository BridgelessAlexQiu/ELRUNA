import networkx as nx

# Read in networks
g1 = nx.read_edgelist("facebook_g1.edges")
g2 = nx.read_edgelist("facebook_g2.edges")

# Print out diameters
print("Diameter of G1: {}".format(nx.diameter(g1))) 
print("Diameter of G2: {}".format(nx.diameter(g2)))