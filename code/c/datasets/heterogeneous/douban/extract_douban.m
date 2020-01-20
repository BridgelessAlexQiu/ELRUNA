clear

load('Douban.mat')

n1 = size(offline, 1);
n2 = size(online, 1);

offline_file = fopen("offline.edges", "w");
online_file = fopen("online.edges", "w");

for i = 1 : (n1-1)
    for j = i+1 : n1
        if offline(i, j) == 1
            fprintf(offline_file, "%s %s\n", int2str(i-1), int2str(j-1)); % -1 because matlab is one-indexed
        end
    end
end

for i = 1 : (n2-1)
    for j = i+1 : n2
        if online(i, j) == 1
            fprintf(online_file, "%s %s\n", int2str(i), int2str(j)); % -1 because matlab is one-indexed
        end
    end
end

fclose(offline_file)
fclose(online_file)