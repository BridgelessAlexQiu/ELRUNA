import networkx as nx  

g1 = nx.read_edgelist("flickr.edges")

g2 = nx.read_edgelist("myspace.edges")

print("Diameter: ", nx.diameter(g1))

print("Diameter: ", nx.diameter(g2))
