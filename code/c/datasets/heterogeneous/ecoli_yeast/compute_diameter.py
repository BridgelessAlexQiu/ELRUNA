import networkx as nx  

g1 = nx.read_edgelist("ecoli.edges")

g2 = nx.read_edgelist("yeast.edges")

print("Diameter: ", nx.diameter(g1))

print("Diameter: ", nx.diameter(g2))
