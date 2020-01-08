function [overlap,OA,OB] = count_overlap(A,B,m)
% COUNT_OVERLAP Count the edge overlap of a mapping between two graphs
%
% Given two graphs and a matching between the vectices, this function counts
% the edges overlapped between the graphs.
%
% COUNT_OVERLAP(A,B,m) returns the edge overlap between adjacency matrices
% A and B given the c x 2 matching m where m(i,1) and mi(i,2) is a match
% between mi(i,1) in A and mi(i,2) in B.  (In other words, m is a list of
% edges between the two graphs.)
%
% The output is equivalent to mi'*(S*mi)/2 where S is the set of all
% possible squares.
%
% [overlap,OA,OB] = count_overlap(A,B,m) also returns the overlapped edges
% of A and B as sparse matrices with the same size.
%
% Example:
%   load ('../data/example-overlap.mat'); % loads A, B, L
%   [S,w,li,lj] = netalign_setup(A,B,L);
%   mi = netalign_exact(S,w,1,1,li,lj); 
%   mi'*S*mi/2 % standard overlap computation with S
%   count_overlap(A,B,[li(mi),lj(mi)])

% David F. Gleich and Ying Wang
% Copyright, Stanford University 2009

% TODO Add overlapped edges output
% TODO Validate the matching

%  History
%  2009-06-03: Initial coding
%  2009-07-01: Output overlap graphs

if ~isstruct(A)
    [rpA ciA] = sparse_to_csr(A);
else
    rpA = A.rp;
    ciA = A.ci;
end

if ~isstruct(B)
    [rpB ciB] = sparse_to_csr(B);
else
    rpB = B.rp;
    ciB = B.ci;
end

nA = length(rpA)-1;
nB = length(rpB)-1;

nmatches = size(m,1);
overlap = 0;

% index the matches in a to b
mAB = zeros(nA,1);
mAB(m(:,1)) = m(:,2);

bindex = zeros(nB,1); % bindex is a work vector

if nargout>1
    % recursive call to count the overlap first, then fill it up
    % with this call
    noverlap = count_overlap(...
        struct('rp',rpA,'ci',ciA),struct('rp',rpB,'ci',ciB),m);
    oa = zeros(noverlap*2,2);
    ob = oa;
end
   
% the following loop double-counts the overlap because it will find the
% overlap from va and va2.

for i=1:nmatches
    va = m(i,1);
    vb = m(i,2);
    
    % index the edges in B
    for riB=rpB(vb):rpB(vb+1)-1
        bindex(ciB(riB))=1;
    end
    
    % for all the edges in A, see if there is an edge in B too
    for riA=rpA(va):rpA(va+1)-1
        % va2 is the neighbor of va
        va2 = ciA(riA);
        
        % skip self-loops
        if va2 == va, continue; end 
        
        va2image = mAB(va2); % get the image
        if va2image
            if bindex(va2image)
                overlap = overlap + 1; % the image is also an edge in B!
                if nargout>1
                    oa(overlap,1) = va;
                    oa(overlap,2) = va2;
                    ob(overlap,1) = vb;
                    ob(overlap,2) = va2image;
                end
            end
        end
    end
    
    % clear the index of edges in B
    for riB=rpB(vb):rpB(vb+1)-1
        bindex(ciB(riB))=0;
    end
    
end

overlap = overlap/2; % we counted the overlap from va and va2

if nargout>1
    OA = sparse(oa(:,1),oa(:,2),1,nA,nA);
    OB = sparse(ob(:,1),ob(:,2),1,nB,nB);
end