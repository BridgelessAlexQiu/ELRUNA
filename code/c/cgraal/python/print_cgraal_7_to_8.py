# ".././CGRAAL_unix64 net1.gw net2.gw similarity.file output1.file output2.file"
import os

real_network_name = ["bio2", "retweet"]

p_real = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"]

garbage_location = "/garbage"

sim_name = "sim.txt"

# ---------- Real Network ------------- #
real_network_location = "gw_dataset/self_under_noise/real_network"
output_location = "output/real_network"

for rn in real_network_name:
    g1_name = real_network_location + "/" + rn + "/" + rn + "_g1.gw"
    sim_location = real_network_location + "/" + rn + "/" + "sim.txt"
    for rp in p_real:
        g2_name = real_network_location + "/" + rn + "/" + rn + "_" + rp + "_g2.gw"
        out1_garbage_name = "output" + garbage_location + "/" + rn + "_" + rp + ".txt"
        out2_name = output_location + "/" + rn + "/" + rn + "_" + rp + ".txt"
        command = "./CGRAAL_unix64" + " " + g1_name + " " + g2_name + " " + sim_location + " " + out1_garbage_name + " " + out2_name

        print(command)
        print()