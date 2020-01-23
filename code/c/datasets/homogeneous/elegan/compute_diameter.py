import networkx as nx  

g1 = nx.read_edgelist("elegan_g1.edges")

g2 = nx.read_edgelist("elegan_g2.edges")

print("Diameter: ", nx.diameter(g1))

print("Diameter: ", nx.diameter(g2))
