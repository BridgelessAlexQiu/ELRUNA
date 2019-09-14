g1_tab_file = open('g1.tab', 'w')
g1_edgelist_file = open('newman_netscience_g1.edgelist', 'r')

for line in g1_edgelist_file:
	i = line.split(' ')[0]
	u = line.split(' ')[1][:-1]
	g1_tab_file.write(str(i) + '\t' + str(u) + '\n')

g1_tab_file.close()
g1_edgelist_file.close()

probability = [0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35, 0.37, 0.39, 0.41, 0.43, 0.45]
for p in probability:
	g2_tab_file_name = "g2_" + str(p) + ".tab"
	g2_edgelist_file_name = "newman_netscience_" + str(p) + "_g2.edgelist"

	g2_tab_file = open(g2_tab_file_name, "w")
	g2_edgelist_file = open(g2_edgelist_file_name, 'r')

	for line in g2_edgelist_file:
		i = line.split(' ')[0]
		u = line.split(' ')[1][:-1]
		g2_tab_file.write(str(i) + '\t' + str(u) + '\n')

	g2_tab_file.close()
	g2_edgelist_file.close()