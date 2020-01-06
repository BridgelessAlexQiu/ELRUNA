outfile_id = fopen("output/self_under_noise/random_network/homle/homle_0.15.txt", "w");

for i = 1 : 10
    for j = 1 : 10
        fprintf(outfile_id, "%s \t %s\n", int2str(i-1), int2str(j-1));
    end
end
fclose(outfile_id);