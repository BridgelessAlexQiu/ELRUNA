homo_network_name = ["dblp", "digg", "elegan", "facebook"]
hete_network_name = ["ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"]

homo_g1_size = [3134, 6634, 2194, 9932]
homo_g2_size = [3875, 7058, 2831, 10380]

hete_g1_size = [1274, 12974, 6714, 1118, 1837]
hete_g2_size = [1994, 15436, 10693, 3906, 1994]

# --------------------- #
#      Homo Network     #
# --------------------- #
homo_location = "../gw_dataset/homogeneous"
for i in range(4):
    name = homo_network_name[i]
    g1_size = homo_g1_size[i]
    g2_size = homo_g2_size[i]
    file_name = homo_location + "/" + name + "/sim.txt"
    file_obj = open(file_name, "w")
    for u in range(g1_size):
        for j in range(g2_size):
            line = str(u) + "\t" + str(j) + "\t" + str(1.0) + "\n"
            file_obj.write(line)

    file_obj.close()


# --------------------- #
#      Real Network     #
# --------------------- #
hete_location = "../gw_dataset/heterogeneous"
for i in range(5):
    name = hete_network_name[i]
    g1_size = hete_g1_size[i]
    g2_size = hete_g2_size[i]
    file_name = hete_location + "/" + name + "/sim.txt"
    file_obj = open(file_name, "w")
    for u in range(g1_size):
        for j in range(g2_size):
            line = str(u) + "\t" + str(j) + "\t" + str(1.0) + "\n"
            file_obj.write(line)

    file_obj.close()     