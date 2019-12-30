import networkx as nx  

g1 = nx.read_edgelist("retweet_2_g1.edges")

print("Diameter: ", nx.diameter(g1))