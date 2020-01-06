% Clear the command line 
clc
close all

% Read in A1 and A2
A1 = dlmread("datasets/self_under_noise/real_network/bio/bio_g1.txt", ',');
A2 = dlmread("datasets/self_under_noise/real_network/bio/bio_g1.txt", ',');

% -------------------------------
% -     Running EigenAlign      -
% -------------------------------
disp('Running EigenAlign');

gamma=0; % The weight between matches and mismatches. gamma = 0 if we only optimize matches

n1 = size(A1, 1); % # of nodes in g1

n2 = size(A2, 1); % # of nodes in g2

map=ones(n1, n2); % an n1 by n2 matrix of all ones

k = 2;

result=LowRank_Align(A1,A2,map, k, gamma); % result{1} is the alignment matrix

% Extrac the one-to-one mappings
for i = 1 : n1
    for j = 1 : n2
        if result(i, j) == 1
            disp([i, ":", j]);
        end
    end
end