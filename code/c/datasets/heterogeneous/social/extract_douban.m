load('flickr-lastfm.mat')

n1 = size(lastfm, 1);
n2 = size(flickr, 1);

online_file = fopen("online.edges", "w");
offline_file = fopen("offline.edges", "w");

for i = 1 : (n1-1)
    for j = i+1 : n1
        if lastfm(i, j) == 1
            fprintf(online_file, "%s %s\n", int2str(i-1), int2str(j-1)); % -1 because matlab is one-indexed
        end
    end
end

for i = 1 : (n2-1)
    for j = i+1 : n2
        if flickr(i, j) == 1
            fprintf(offline_file, "%s %s\n", int2str(i), int2str(j)); % -1 because matlab is one-indexed
        end
    end
end

fclose(online_file)
fclose(offline_file)