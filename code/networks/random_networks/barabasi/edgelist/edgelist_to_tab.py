g1_tab_file = open('g1.tab', 'w')
g2_tab_file = open("g2.tab", "w")


g1_edgelist_file = open('barabasi_g1.edgelist', 'r')
g2_edgelist_file = open('barabasi_0.011_g2.edgelist', 'r')

for line in g1_edgelist_file:
	i = line.split(' ')[0]
	u = line.split(' ')[1][:-1]
	g1_tab_file.write(str(i) + '\t' + str(u) + '\n')

for line in g2_edgelist_file:
	i = line.split(' ')[0]
	u = line.split(' ')[1][:-1]
	g2_tab_file.write(str(i) + '\t' + str(u) + '\n')

g1_tab_file.close()
g2_tab_file.close()
g1_edgelist_file.close()
g2_edgelist_file.close()