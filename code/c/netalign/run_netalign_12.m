clc
clear

network_name = ["google"];

noise = ["0", "0.01", "0.03", "0.05", "0.07", "0.09", "0.11", "0.13", "0.15", "0.17", "0.19", "0.21", "0.23", "0.25"];

network_file_location = "datasets/self_under_noise/real_network";

L_file_location = "L/self_under_noise/real_network";

output_file_location = "output/netalign/self_under_noise/real_network";

for i = 1 : length(network_name)
    nn = network_name{i};
    g1_file_name = strcat(network_file_location, "/", nn, "/", nn, "_g1.txt");
    
    A1 = dlmread(g1_file_name);
    n1 = size(A1, 1); % size of the first network
    
    for j = 1 : length(noise)
        p = noise{j};
        g2_file_name = strcat(network_file_location, "/", nn, "/", nn, "_", p, "_g2.txt");
        l_file_name = strcat(L_file_location, "/", nn, "/", nn, "_", p, "_l.txt");
        
        A2 = dlmread(g2_file_name);
        n2 = size(A2, 1); % size of the second network
        
        L = dlmread(l_file_name);
        
        %Start NetAlign
        [S,w,li,lj] = netalign_setup(A1,A2,L);
        x = netalignbp(S,w,0,1,li,lj);

        % Extract mapping
        [ma, mb, mi, overlap, weight] = mwmround(x,S,w,li,lj);
        
        output_file_name = strcat(output_file_location, "/", nn, "/", nn, "_", p, ".txt");
        
        % Save to file
        outfile_id = fopen(output_file_name, "w");

        % We assume n1 <= n2
        for i2 = 1 : length(ma)
            fprintf(outfile_id, "%s\t%s\n", int2str(ma(i2)-1), int2str(mb(i2)-1)); % -1 because matlab is one-indexed
        end

        fclose(outfile_id);
    end
end