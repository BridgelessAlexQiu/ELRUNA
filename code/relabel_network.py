import networkx as nx 

file = "dataset/CA-HepTh.txt"
file_obj = open(file)
i = 0
set_of_nodes = set()
for line in file_obj:
    n1 = line.split('\t')[0]
    n2 = line.split('\t')[1][:-1]
    set_of_nodes.add(n1)
    set_of_nodes.add(n2)


