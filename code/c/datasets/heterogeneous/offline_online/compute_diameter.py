import networkx as nx  

g1 = nx.read_edgelist("offline.edges")

g2 = nx.read_edgelist("online.edges")

print("Diameter: ", nx.diameter(g1))

print("Diameter: ", nx.diameter(g2))
