# ".././CGRAAL_unix64 net1.gw net2.gw similarity.file output1.file output2.file"
import os

homo_network_name = ["dblp", "digg", "elegan", "facebook"]
hete_network_name = ["ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"]

garbage_location = "/garbage"

sim_name = "sim.txt"

# ---------- Homo Network ----------- #
homo_network_location = "gw_dataset/homogeneous"
homo_output_location = "output/homogeneous"

for rn in homo_network_name:
    g1_name = homo_network_location + "/" + rn + "/" + rn + "_g1.gw"
    g2_name = homo_network_location + "/" + rn + "/" + rn + "_g2.gw"
    sim_location = homo_network_location + "/" + rn + "/" + "sim.txt"

    out1_garbage_name = "output" + garbage_location + "/" + rn + ".txt"
    out2_name = homo_output_location + "/" + rn + "/" + rn + ".txt"
    command = "./CGRAAL_unix64" + " " + g1_name + " " + g2_name + " " + sim_location + " " + out1_garbage_name + " " + out2_name

    print(command)
    print()

# ---------- Hete Network ----------- #
hete_network_location = "gw_dataset/heterogeneous"
hete_output_location = "output/heterogeneous"

for rn in hete_network_name:
    g1 = rn.split('_')[0]
    g2 = rn.split('_')[1]
    g1_name = hete_network_location + "/" + rn + "/" + g1 + ".gw"
    g2_name = hete_network_location + "/" + rn + "/" + g2 + ".gw"
    sim_location = hete_network_location + "/" + rn + "/" + "sim.txt"

    out1_garbage_name = "output" + garbage_location + "/" + rn + ".txt"
    out2_name = hete_output_location + "/" + rn + "/" + rn + ".txt"
    command = "./CGRAAL_unix64" + " " + g1_name + " " + g2_name + " " + sim_location + " " + out1_garbage_name + " " + out2_name

    print(command)
    print()