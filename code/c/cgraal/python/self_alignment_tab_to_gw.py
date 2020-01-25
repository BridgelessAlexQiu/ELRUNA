#! CAUSION: THE STUPID list2leda file DOES NOT OVERWRITE BUT APPEND

import os

random_network_name = ["barabasi", "homle"]
real_network_name = ["bio", "bio2", "econ", "erdos", "google", "newman", "retweet", "retweet_2", "router", "social"]

p_random = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21"]
p_real = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"]

# # ----------------------------- #
# #        Random Networks        #
# # ----------------------------- #
# new_random_network_location = "../gw_dataset/self_under_noise/random_network"
# random_network_command = ".././list2leda tab_dataset/self_under_noise/random_network"

# for rn in random_network_name:
#     #g1
#     g1_file_name = rn + '/' + rn + "_g1.edgelist"
#     new_g1_file_name = rn + '/' + rn + "_g1.gw"

#     command = random_network_command + '/' + g1_file_name + " >> " + new_random_network_location + "/" + new_g1_file_name

#     os.system(command)

#     #g2
#     for rp in p_random:
#         g2_file_name =  rn + '/' + rn + "_" + rp + "_g2.edgelist"
#         new_g2_file_name = rn + '/' + rn + "_" + rp + "_g2.gw"

#         command = random_network_command + '/' + g2_file_name + " >> " + new_random_network_location + "/" + new_g2_file_name

#         os.system(command)

# # -------------------------- #
# #        Real Networks       #
# # -------------------------- #
# real_network_command = ".././list2leda tab_dataset/self_under_noise/real_network"
# new_real_network_location = "../gw_dataset/self_under_noise/real_network"

# for rn in real_network_name:
#     #g1
#     g1_file_name = rn + '/' + rn + "_g1.edgelist"
#     new_g1_file_name = rn + '/' + rn + "_g1.gw"

#     command = real_network_command + '/' + g1_file_name + " >> " + new_real_network_location + "/" + new_g1_file_name

#     os.system(command)

#     #g2
#     for rp in p_real:
#         g2_file_name = rn + '/' + rn + "_" + rp + "_g2.edgelist"
#         new_g2_file_name = rn + '/' + rn + "_" + rp + "_g2.gw"

#         command = real_network_command + '/' + g2_file_name + " >> " + new_real_network_location + "/" + new_g2_file_name

#         os.system(command)