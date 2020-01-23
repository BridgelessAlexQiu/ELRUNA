import networkx as nx  

g1 = nx.read_edgelist("yeast.edges")

g2 = nx.read_edgelist("syne.edges")

print("Diameter: ", nx.diameter(g1))

print("Diameter: ", nx.diameter(g2))
