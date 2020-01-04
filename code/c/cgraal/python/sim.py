random_network_name = ["barabasi", "homle"]
real_network_name = ["bio", "bio2", "econ", "erdos", "newman", "retweet", "retweet_2", "router"]

random_network_size = [400, 400]
real_network_size = [993, 2831, 1258, 4991, 379, 4171, 7252, 2113]

# ----------------------- #
#      Random Network     #
# ----------------------- #
random_location = "../gw_dataset/self_under_noise/random_network"
for i in range(2):
    name = random_network_name[i]
    size = random_network_size[i]
    file_name = random_location + "/" + name + "/sim.txt"
    file_obj = open(file_name, "w")
    for u in range(size):
        for j in range(size):
            line = str(u) + "\t" + str(j) + "\t" + str(1.0) + "\n"
            file_obj.write(line)

    file_obj.close()  


# --------------------- #
#      Real Network     #
# --------------------- #
real_location = "../gw_dataset/self_under_noise/real_network"
for i in range(10):
    name = real_network_name[i]
    size = real_network_size[i]
    file_name = real_location + "/" + name + "/sim.txt"
    file_obj = open(file_name, "w")
    for u in range(size):
        for j in range(size):
            line = str(u) + "\t" + str(j) + "\t" + str(1.0) + "\n"
            file_obj.write(line)

    file_obj.close()     