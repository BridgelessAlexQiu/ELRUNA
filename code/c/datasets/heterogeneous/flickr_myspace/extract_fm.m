clear
load('flickr-myspace.mat')

n1 = size(flickr, 1);
n2 = size(myspace, 1);

flickr_file = fopen("flickr.edges", "w");
myspace_file = fopen("myspace.edges", "w");

for i = 1 : (n1-1)
    for j = i+1 : n1
        if flickr(i, j) == 1
            fprintf(flickr_file, "%s %s\n", int2str(i-1), int2str(j-1)); % -1 because matlab is one-indexed
        end
    end
end

for i = 1 : (n2-1)
    for j = i+1 : n2
        if myspace(i, j) == 1
            fprintf(myspace_file, "%s %s\n", int2str(i), int2str(j)); % -1 because matlab is one-indexed
        end
    end
end

fclose(flickr_file)
fclose(myspace_file)