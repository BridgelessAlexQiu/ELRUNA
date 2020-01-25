random_network_name = ["barabasi", "homle"]
real_network_name = ["bio", "bio2", "econ", "erdos", "google", "newman", "retweet", "retweet_2", "router", "social"]

p_random = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21"]
p_real = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"]

# ----------------------------- #
#        Random Networks        #
# ----------------------------- #
random_network_location = "../../datasets/self_under_noise/random_network"
new_random_network_location = "../tab_dataset/self_under_noise/random_network"
for rn in random_network_name:
    #g1
    g1_file_name = random_network_location + '/' + rn + '/' + rn + "_g1.edgelist"
    new_g1_file_name = new_random_network_location + '/' + rn + '/' + rn + "_g1.edgelist"

    g1_file = open(g1_file_name, 'r')
    new_g1_file = open(new_g1_file_name, "w")

    for line in g1_file:
        v1 = line.split(' ')[0]
        v2 = line.split(' ')[1]
        new_g1_file.write(v1 + "\t" + v2)

    g1_file.close()
    new_g1_file.close()

    #g2
    for rp in p_random:
        g2_file_name = random_network_location + '/' + rn + '/' + rn + "_" + rp + "_g2.edgelist"
        new_g2_file_name = new_random_network_location + '/' + rn + '/' + rn + "_" + rp + "_g2.edgelist"

        g2_file = open(g2_file_name, 'r')
        new_g2_file = open(new_g2_file_name, "w")

        for line in g2_file:
            v1 = line.split(' ')[0]
            v2 = line.split(' ')[1]
            new_g2_file.write(v1 + "\t" + v2)

        g2_file.close()
        new_g2_file.close()


# -------------------------- #
#        Real Networks       #
# -------------------------- #
real_network_location = "../../datasets/self_under_noise/real_network"
new_real_network_location = "../tab_dataset/self_under_noise/real_network"
for rn in real_network_name:
    #g1
    if rn == "newman":
        g1_file_name = real_network_location + '/' + rn + '/' + rn + "_g1.edgelist"
    else: 
        g1_file_name = real_network_location + '/' + rn + '/' + rn + "_g1.edges"

    new_g1_file_name = new_real_network_location + '/' + rn + '/' + rn + "_g1.edgelist"

    g1_file = open(g1_file_name, 'r')
    new_g1_file = open(new_g1_file_name, "w")

    for line in g1_file:
        v1 = line.split(' ')[0]
        v2 = line.split(' ')[1]
        new_g1_file.write(v1 + "\t" + v2)

    g1_file.close()
    new_g1_file.close()

    #g2
    for rp in p_real:
        if rn == "newman":
            g2_file_name = real_network_location + '/' + rn + '/' + rn + "_" + rp + "_g2.edgelist"
        else: 
            g2_file_name = real_network_location + '/' + rn + '/' + rn + "_" + rp + "_g2.edges"

        new_g2_file_name = new_real_network_location + '/' + rn + '/' + rn + "_" + rp + "_g2.edgelist"

        g2_file = open(g2_file_name, 'r')
        new_g2_file = open(new_g2_file_name, "w")

        for line in g2_file:
            v1 = line.split(' ')[0]
            v2 = line.split(' ')[1]
            new_g2_file.write(v1 + "\t" + v2)

        g2_file.close()
        new_g2_file.close()