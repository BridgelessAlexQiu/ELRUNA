import networkx as nx  

g1 = nx.read_edgelist("flikcr.edges")

g2 = nx.read_edgelist("lastfm.edges")

print("Diameter: ", nx.diameter(g1))

print("Diameter: ", nx.diameter(g2))
