function [q,M] = maxrowmatch(Q,li,lj,m,n)
% MAXROWMATCH Compute a max-row matching in a sparse matrix
%
% q = maxrowmatch(Q,li,lj)
% [q,M] = maxrowmatch(Q,li,lj,m,n)
% Given a sparse matrix Q where each row corresponds to a possible
% edge in a bipartite matching (i.e. Q(i,:) corresponds with li(i), lj(i))
% then we compute the row-sum of Q subject to the constraint that
% the values summed are a matching in li, lj.  In other words,
% instead of q=Q*e, the standard row-sum, we compute
%   q(i) = Q(i,:)*m_i where m_i is the maximum matching 
%     of all the non-zero values Q(i,:) with edges from li,lj
% M is a sparse 
% 

% TODO Make auto compiling

if ~exist('m','var') || isempty(m), m = max(li); end
if ~exist('n','var') || isempty(n), n = max(lj); end

Qt = Q';
Qt = double(Qt);
[q mj mi medges] = column_maxmatchsum_mex(Qt,li,lj,m,n);
M = sparse(mi(1:medges),mj(1:medges),1,size(Q,1),size(Q,2));
q = q';