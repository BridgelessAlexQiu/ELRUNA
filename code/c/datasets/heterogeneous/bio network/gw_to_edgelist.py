# Author: Zirou Qiu
# Desciption: 
#   1. convert .gw to .edges file
#   2. extract the lcc from each network, and remove loops and relable vertices with ints

import networkx nx

# names of each network
networks = ["cjejuni", "ecoli", "human", "meso", "syne", "yeast"]

# ------------------------------------ #
#       Iterate over each network      #
# ------------------------------------ #
for network in networks:
    # contruct the name
    gw_network_name = "gw/" + network + ".gw"
    edgelist_network_name = "edgelist/" + network + "_raw.edges"

    # create the file object
    in_file_obj = open(gw_network_name, 'r') 
    out_file_obj = open(edgelist_network_name, "w")

    # extract vertices from each line
    for line in in_file_obj:
        # extract two vertices
        v1 = line.split(' ')[0]
        v2 = line.split(' ')[1]
    out_file_obj.write(v1 + ' ' + v2 + '\n') # write to the .edges file

    # close the file object
    in_file_obj.close()
    out_file_obj.close()


# ------------------------------ #
#       Clean each network       #
# ------------------------------ #
for network in networks:
    in_network_name = "edgelist/" + network + "_raw.edges"
    out_network_name = "edgelist/" + network + ".edges"
    g1 = nx.readedgelist(in_network_name)

    # Extract LCC
    largest_cc_1 = max(nx.connected_components(g1), key=len)
    g1 = g1.subgraph(largest_cc_1)

    # Relabel the vertices
    g1 = nx.convert_node_labels_to_integers(g1)

    # Remove loops
    g1.remove_edges_from(nx.selfloop_edges(g1))

    # Pint network info
    print(network + ":")
    print(nx.info(g1))
    print("The diameter: {}".format(nx.diameter(g1)))

    # Finally, write to .edges file
    nx.write_edgelist(g1, out_network_name, data = False)