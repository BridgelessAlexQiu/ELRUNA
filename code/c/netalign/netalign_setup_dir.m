function [S,w,li,lj] = netalign_setup(A,B,L)
% NETALIGN_SETUP Setup the data for the netalign codes from the problem data
% 
% [S,w,li,lj] = netalign_setup(A,B,L) computes the data for the netalign
% codes netalignbp, isorank, netalign_lp_prob from the problem data for the
% network alignment problem itself (graph A, graph B, and bipartite links
% L).
%
% Example:
%   load ('../data/example-overlap.mat'); % loads A, B, L
%   [S,w,li,lj] = netalign_setup(A,B,L);
%   netalign_exact(S,w,1,1,li,lj)

[Se Le] = make_squares(A,B',L);
li = Le(:,1);
lj = Le(:,2);
w = Le(:,3);
Se1 = Se(:,1);
Se2 = Se(:,2);
clear Se Le;
S = sparse(Se1,Se2,true,nnz(L),nnz(L));
