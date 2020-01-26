clc
clear % clear output and workspace

homo_network_name = ["dblp", "digg", "elegan", "facebook"]
hete_network_name = ["ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"]

homo_network_file_location = "datasets/homogeneous";
hete_network_file_location = "datasets/heterogeneous";

homo_output_file_location = "output/homogeneous";
hete_output_file_location = "output/heterogeneous";

g = 0; % balance between matches and mismatches

k = 2; % top k eigenvectors are considered (for low-rank version)

% ---------------------------- %
%         Homogeneous          %
% ---------------------------- %
for i = 1 : length(homo_network_name)
    nn = homo_network_name{i};
    % ---------- G1 ------------ %
    g1_file_location = strcat(homo_network_file_location, "/", nn, "/", nn, "_g1.txt");
    A1 = dlmread(g1_file_location);
    n1 = size(A1, 1); % size of the first network

    % ---------- G2 ------------ %
    g2_file_location = strcat(homo_network_file_location, "/", nn, "/", nn, "_g2.txt");
    A2 = dlmread(g2_file_location);
    n2 = size(A2, 1); % size of the second network

    map = ones(n1, n2); % possible matchings 

    result = LowRank_Align(A1, A2, map, k, g); % result is the alignment matrix

    output_file_name = strcat(homo_output_file_location, "/", nn, "/", nn, ".txt");

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

% ----------------------------- %
%        Heterogeneous          %
% ----------------------------- %
for i = 1 : length(hete_network_name)
    nn = hete_network_name{i};
    g1_name = split(nn, "_")(1);
    g2_name = split(nn, "_")(2);

    % ---------- G1 ------------ %
    g1_file_location = strcat(hete_network_file_location, "/", nn, "/", g1_name, ".txt");
    A1 = dlmread(g1_file_location);
    n1 = size(A1, 1); % size of the first network

    % ---------- G2 ------------ %
    g2_file_location = strcat(hete_network_file_location, "/", nn, "/", g2_name, ".txt");
    A2 = dlmread(g2_file_location);
    n2 = size(A2, 1); % size of the second network

    map = ones(n1, n2); % possible matchings 

    result = LowRank_Align(A1, A2, map, k, g); % result is the alignment matrix

    output_file_name = strcat(hete_output_file_location, "/", nn, "/", nn, ".txt");

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
