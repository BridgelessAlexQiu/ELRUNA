in_file_obj = open("yeast.tab", 'r')
out_file_obj = open("yeast.edges", 'w')

for line in in_file_obj:
    i = line.split('\t')[0]
    j = line.split('\t')[1]
    out_file_obj.write(i + ' ' + j[:-1] + '\n')

in_file_obj.close()
out_file_obj.close()


in_file_obj = open("human.tab", 'r')
out_file_obj = open("human.edges", 'w')

for line in in_file_obj:
    i = line.split('\t')[0]
    j = line.split('\t')[1]
    out_file_obj.write(i + ' ' + j[:-1] + '\n')

in_file_obj.close()
out_file_obj.close()
