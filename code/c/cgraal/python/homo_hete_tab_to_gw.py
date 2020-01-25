#! CAUSION: THE STUPID list2leda file DOES NOT OVERWRITE BUT APPEND

# import os

# homo_network_name = ["dblp", "digg", "elegan", "facebook"]
# hete_network_name = ["ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"]

# # --------------------------- #
# #        Homo Networks        #
# # --------------------------- #
# new_homo_network_location = "gw_dataset/homogeneous"
# homo_network_command = "./list2leda tab_dataset/homogeneous"

# for rn in homo_network_name:
#     #g1
#     g1_file_name = rn + '/' + rn + "_g1.edges"
#     new_g1_file_name = rn + '/' + rn + "_g1.gw"

#     command = homo_network_command + '/' + g1_file_name + " >> " + new_homo_network_location + "/" + new_g1_file_name

#     os.system(command)

#     #g2
#     g2_file_name =  rn + '/' + rn + "_g2.edges"
#     new_g2_file_name = rn + '/' + rn + "_g2.gw"

#     command = homo_network_command + '/' + g2_file_name + " >> " + new_homo_network_location + "/" + new_g2_file_name

#     os.system(command)

# # -------------------------- #
# #        Hete Networks       #
# # -------------------------- #
# new_hete_network_location = "gw_dataset/heterogeneous"
# hete_network_command = "./list2leda tab_dataset/heterogeneous"

# for rn in hete_network_name:
#     #g1
#     g1_name = rn.split("_")[0]
#     g1_file_name = rn + '/' + g1_name + ".edges"
#     new_g1_file_name = rn + '/' + g1_name + ".gw"

#     command = hete_network_command + '/' + g1_file_name + " >> " + new_hete_network_location + "/" + new_g1_file_name

#     os.system(command)

#     #g2
#     g2_name = rn.split("_")[1]
#     g2_file_name = rn + '/' + g2_name + ".edges"
#     new_g2_file_name = rn + '/' + g2_name + ".gw"

#     command = hete_network_command + '/' + g2_file_name + " >> " + new_hete_network_location + "/" + new_g2_file_name

#     os.system(command)