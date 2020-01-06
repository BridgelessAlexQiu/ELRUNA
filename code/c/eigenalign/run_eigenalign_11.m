clc
clear % clear output and workspace

network_name = ["social"];

noise = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"];

network_file_location = "datasets/self_under_noise/real_network";

output_file_location = "output/self_under_noise/real_network";

g = 0; % balance between matches and mismatches

k = 2; % top k eigenvectors are considered (for low-rank version)

%---------------- Main for loop ---------------%
for i = 1 : length(network_name)
    nn = network_name{i};
    g1_file_location = strcat(network_file_location, "/", nn, "/", nn, "_g1.txt");

    A1 = dlmread(g1_file_location);
    n1 = size(A1, 1); % size of the first network
    
    for j = 1 : length(noise)
        p = noise{j}
        g2_file_location = strcat(network_file_location, "/", nn, "/", nn, "_", p, "_g2.txt");

        A2 = dlmread(g2_file_location);
        n2 = size(A2, 1); % size of the second network

        map = ones(n1, n2); % possible matchings 

        result = LowRank_Align(A1, A2, map, k, g); % result is the alignment matrix

        output_file_name = strcat(output_file_location, "/", nn, "/", nn, "_", p, ".txt");

        disp(output_file_name);

        outfile_id = fopen(output_file_name, "w");

        % Extract the matchingss
        for u = 1 : n1
            for v = 1 : n2
                if result(u, v) == 1
                    fprintf(outfile_id, "%s \t %s\n", int2str(u-1), int2str(v-1)); % very important since matrices in matlab are one-indexed
                end
            end
        end

        fclose(outfile_id);

    end

end 

