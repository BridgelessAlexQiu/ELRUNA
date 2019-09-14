g1_tab_file = open('regular_g1.tab', 'w')
g1_edgelist_file = open('regular_g1.edgelist', 'r')

for line in g1_edgelist_file:
	i = line.split(' ')[0]
	u = line.split(' ')[1][:-1]
	g1_tab_file.write(str(i) + '\t' + str(u) + '\n')

g1_tab_file.close()
g1_edgelist_file.close()

g2_tab_file_name = "regular_g2.tab"
g2_edgelist_file_name = "regular_g2.edgelist"

g2_tab_file = open(g2_tab_file_name, "w")
g2_edgelist_file = open(g2_edgelist_file_name, 'r')

for line in g2_edgelist_file:
	i = line.split(' ')[0]
	u = line.split(' ')[1][:-1]
	g2_tab_file.write(str(i) + '\t' + str(u) + '\n')

g2_tab_file.close()
g2_edgelist_file.close()