homo_network_name = ["dblp", "digg", "elegan", "facebook"]
hete_network_name = ["ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"]

# --------------------------- #
#        Homo Networks        #
# --------------------------- #
# Prelocation of homo networks
homo_network_location = "../../datasets/homogeneous"
new_homo_network_location = "../tab_dataset/homogeneous"

# for each homo network name
for rn in homo_network_name: # rn_g1.edges vs rn_g2.edges
    # ---------- g1 ---------- #
    g1_file_name = homo_network_location + '/' + rn + '/' + rn + "_g1.edges"
    new_g1_file_name = new_homo_network_location + '/' + rn + '/' + rn + "_g1.edges"

    g1_file = open(g1_file_name, 'r')
    new_g1_file = open(new_g1_file_name, "w")

    for line in g1_file:
        v1 = line.split(' ')[0]
        v2 = line.split(' ')[1]
        new_g1_file.write(v1 + "\t" + v2)

    g1_file.close()
    new_g1_file.close()

    # ---------- g2 ---------- #
    g2_file_name = homo_network_location + '/' + rn + '/' + rn + "_g2.edges"
    new_g2_file_name = new_homo_network_location + '/' + rn + '/' + rn + "_g2.edges"

    g2_file = open(g2_file_name, 'r')
    new_g2_file = open(new_g2_file_name, "w")

    for line in g2_file:
        v1 = line.split(' ')[0]
        v2 = line.split(' ')[1]
        new_g2_file.write(v1 + "\t" + v2)

    g2_file.close()
    new_g2_file.close()


# -------------------------- #
#        Hete Networks       #
# -------------------------- #
hete_network_location = "../../datasets/heterogeneous"
new_hete_network_location = "../tab_dataset/heterogeneous"
for rn in hete_network_name: 
    g1_name = rn.split("_")[0]

    g1_file_name = hete_network_location + '/' + rn + '/' + g1_name + ".edges"
    new_g1_file_name = new_hete_network_location + '/' + rn + '/' + g1_name + ".edges"

    g1_file = open(g1_file_name, 'r')
    new_g1_file = open(new_g1_file_name, "w")

    for line in g1_file:
        v1 = line.split(' ')[0]
        v2 = line.split(' ')[1]
        new_g1_file.write(v1 + "\t" + v2)

    g1_file.close()
    new_g1_file.close()

    #g2
    g2_name = rn.split("_")[1]

    g2_file_name = hete_network_location + '/' + rn + '/' + g2_name +".edges"
    new_g2_file_name = new_hete_network_location + '/' + rn + '/' + g2_name +".edges"

    g2_file = open(g2_file_name, 'r')
    new_g2_file = open(new_g2_file_name, "w")

    for line in g2_file:
        v1 = line.split(' ')[0]
        v2 = line.split(' ')[1]
        new_g2_file.write(v1 + "\t" + v2)

    g2_file.close()
    new_g2_file.close()