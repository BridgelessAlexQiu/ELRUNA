function L = expand_match(A,B,L)
% EXPAND_MATCH Expand a set of possible matchings with breadth first search
%
% L2 = expand_match(A,B,L) returns a new sparse match matrix L2 for the
% network alignment problem where L2 includes the neighbors of all existing
% matchings.
%
% 

% David F. Gleich and Ying Wang
% Copyright, Stanford University, 2009

% TODO Example

%  History
%  2009-05-29 Initial coding, based on old c code


nA = size(A,1);


[rpB ciB vB] = sparse_to_csr(B);
[lai laj lav] = compute_expanded_match(nA,rpB,ciB,vB,L);
clear rpB ciB vB

nB = size(B,1);
[rpA ciA vA] = sparse_to_csr(A);
[lbj lbi lbv] = compute_expanded_match(nB,rpA,ciA,vA,L');
clear rpA ciA vA

lai = [lai; lbi];
laj = [laj; lbj];
lav = [lav; lbv];
clear lbi lbj lbv

L = sparse(lai, laj, lav, nA, nB);



function [l2i l2j l2v]=compute_expanded_match(nA,rpB,ciB,vB,L)
% just do one step of bfs and expand the current match

% allocate edges
l2i = zeros(nnz(L),1);
l2j = l2i;
l2v = l2i;
curedge = 0;

% convert to CSR
[rpAB ciAB vAB] = sparse_to_csr(L);
nB = length(rpB)-1;
% allocate temp arrays
work = zeros(nB,1);
work_used = zeros(nB,1);
dwork = zeros(nB,1);
for i=1:nA
    num_adj = 0;
    for ri=rpAB(i):rpAB(i+1)-1
        j = ciAB(ri);
        deg_in_B = rpB(j+1)-rpB(j);
        for ri2=rpB(j):rpB(j+1)-1
            k = ciB(ri2);
            if work(k) == 0
                dwork(num_adj+1) = vAB(ri)/deg_in_B;
                work_used(num_adj+1) = k;
                work(k) = num_adj+1;
                num_adj = num_adj + 1;
            else
                dwork(work(k)) = max( dwork(work(k)), vAB(ri)/deg_in_B );
            end
        end
        % make sure we include j
        if work(j) == 0
            dwork(num_adj+1) = vAB(ri);
            work_used(num_adj+1) = j;
            work(j) = num_adj+1;
            num_adj = num_adj + 1;
        else
            dwork(work(k)) = max( dwork(work(k)), vAB(ri) );
        end
    end
    % copy the data and reset the arrays
    % first check if there is enough space
    while curedge + num_adj > length(l2i)
        % double the arrays
        l2i = [l2i; l2i]; l2j = [l2j; l2j]; l2v = [l2v; l2v]; %#ok<AGROW>
    end
    for j=1:num_adj
        curedge = curedge + 1;
        l2i(curedge) = i;
        l2j(curedge) = work_used(j);
        l2v(curedge) = dwork(j);
        work(work_used(j)) = 0;
        work_used(j) = 0;
        dwork(j) = 0;
    end
end
% resize at the end
l2i = l2i(1:curedge);
l2j = l2j(1:curedge);
l2v = l2v(1:curedge);