clc
clear

homo_network_name = ["dblp", "digg", "elegan", "facebook"]
hete_network_name = ["ecoli_yeast", "flickr_lastfm", "flickr_myspace", "offline_online", "syne_yeast"]

homo_network_file_location = "datasets/homogeneous";
hete_network_file_location = "datasets/heterogeneous";

homo_output_file_location = "output/netalign/homogeneous";
hete_output_file_location = "output/netalign/heterogeneous";

homo_L_file_location = "L/homogeneous";
hete_L_file_location = "L/heterogeneous";

% ---------------------------- %
%         Homogeneous          %
% ---------------------------- %
for i = 1 : length(homo_network_name)
    nn = homo_network_name{i};
    % ---------- G1 ---------- %
    g1_file_location = strcat(homo_network_file_location, "/", nn, "/", nn, "_g1.txt");
    A1 = dlmread(g1_file_location);
    n1 = size(A1, 1); % size of the first network
    
    % --------- G2 ---------- %
    g2_file_name = strcat(homo_network_file_location, "/", nn, "/", nn, "_g2.txt");
    A2 = dlmread(g2_file_name);
    n2 = size(A2, 1); % size of the second network
    
    % --------- L --------- %
    l_file_name = strcat(homo_L_file_location, "/", nn, "/", nn, ".txt");
    L = dlmread(l_file_name);
    
    %Start NetAlign
    [S,w,li,lj] = netalign_setup(A1,A2,L);
    x = netalignbp(S,w,0,1,li,lj);

    % Extract mapping
    [ma, mb, mi, overlap, weight] = mwmround(x,S,w,li,lj);
    
    output_file_name = strcat(homo_output_file_location, "/", nn, "/", nn, ".txt");
    
    % Save to file
    outfile_id = fopen(output_file_name, "w");

    % We assume n1 <= n2
    for i2 = 1 : length(ma)
        fprintf(outfile_id, "%s\t%s\n", int2str(ma(i2)-1), int2str(mb(i2)-1)); % -1 because matlab is one-indexed
    end

    fclose(outfile_id);
end

% ---------------------------- %
%        Heterogeneous         %
% ---------------------------- %
for i = 1 : length(hete_network_name)
    nn = hete_network_name{i};
    arr = split(nn, "_");
    g1_name = arr(1);
    g2_name = arr(2);

% ---------- G1 ------------ %
    g1_file_location = strcat(hete_network_file_location, "/", nn, "/", g1_name, ".txt");
    A1 = dlmread(g1_file_location);
    n1 = size(A1, 1); % size of the first network

    % ---------- G2 ------------ %
    g2_file_location = strcat(hete_network_file_location, "/", nn, "/", g2_name, ".txt");
    A2 = dlmread(g2_file_location);
    n2 = size(A2, 1); % size of the second network
    
    % --------- L --------- %
    l_file_name = strcat(hete_L_file_location, "/", nn, "/", nn, ".txt");
    L = dlmread(l_file_name);
    
    %Start NetAlign
    [S,w,li,lj] = netalign_setup(A1,A2,L);
    x = netalignbp(S,w,0,1,li,lj);

    % Extract mapping
    [ma, mb, mi, overlap, weight] = mwmround(x,S,w,li,lj);
    
    output_file_name = strcat(hete_output_file_location, "/", nn, "/", nn, ".txt");
    
    % Save to file
    outfile_id = fopen(output_file_name, "w");

    % We assume n1 <= n2
    for i2 = 1 : length(ma)
        fprintf(outfile_id, "%s\t%s\n", int2str(ma(i2)-1), int2str(mb(i2)-1)); % -1 because matlab is one-indexed
    end

    fclose(outfile_id);
end