function [s Mcc]=evaluate_alignment(A,B,mi,li,lj)
% EVALUATE_ALIGNMENT Report properties of the graph alignment
%
% evaluate_alignment(A,B,mi,li,lj) returns properties of an alignment
% between graphs A and B.
% evaluate_alignment(A,B,ma,mb) returns properties of an alignment
% between graphs A and B.
%
%   Edges - number of edges (2-cliques) preserved by the mapping
%   Triangles - number of triangles (3-cliques) preserved by the mapping
%   Largest Component - largest connected component with the mapping
%

%  History
%  2009-07-01: Initial coding

if nargin==4
    ma = mi;
    mb = li;
    % given as pairs
    X = sparse(ma,mb,1,size(A,1),size(B,1));
else
    % given as an indicator
    % make sure x is binary
    if any(logical(mi)~=mi)
        error('netalign:invalidMatching',...
            'the matching indicator mi is not binary')
    end
    X = sparse(li,lj,mi,size(A,1),size(B,1));
end
% make sure x is a matching
s1 = sum(X,1);
s2 = sum(X,2);
if any(s1~=logical(s1)) || any(s2~=logical(s2))
    error('netalign:invalidMatching',...
        'the given alignment is not a matching');
end

[rpA ciA] = sparse_to_csr(A);
[rpB ciB] = sparse_to_csr(B);
As = struct('rp',rpA,'ci',ciA);
Bs = struct('rp',rpB,'ci',ciB);
nA = length(rpA)-1;
nB = length(rpB)-1;

[ma mb] = find(X);

% the overlapped graph
[nedges,OA,OB]=count_overlap(As,Bs,[ma mb]);
G = [OA X; X' OB];
[ci,sizes] = scomponents(G);

[ma mb] = find(X);


% create the output as a structure
s = [];
s.size = length(ma);
[s.largest_component,max_ci] = max(sizes);
s.edges = count_overlap(As,Bs,[ma mb]);
s.triangles = count_triangle_overlap(As,Bs,[ma mb]);

s.largest_component_A = sum(ci(1:nA)==max_ci);
s.largest_component_B = sum(ci(nA+1:end)==max_ci);

Mcc = sparse(find(ci(1:nA)==max_ci), find(ci(nA+1:end)==max_ci), 1, nA, nB);
% display output unless requested
if nargout == 0
    fprintf('%25s  %i\n', 'Size', s.size);
    fprintf('%25s  %i\n', 'Edge Overlap', s.edges);
    fprintf('%25s  %i\n', 'Triangle Overlap', s.triangles);
    fprintf('%25s  %i\n', 'Largest Component', s.largest_component);
    fprintf('%25s  %i\n', 'Largest Component (A)', s.largest_component_A);
    fprintf('%25s  %i\n', 'Largest Component (B)', s.largest_component_B);
end
    

function [ntris]=count_triangle_overlap(A,B,m)

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

% index the matches in a to b
mAB = zeros(nA,1);
mAB(m(:,1)) = m(:,2);
mBA = zeros(nB,1);
mBA(m(:,2)) = m(:,1);

ntris = 0;
nmatches = size(m,1);


aindex = zeros(nA,1);
bindex = zeros(nB,1); % bindex is a work vector

for i=1:nmatches
    % count the number of triangles from this match
    va = m(i,1);
    vb = m(i,2);
    
    % index the neighbors in A
    for riA=rpA(va):rpA(va+1)-1
        if ciA(riA)==va, continue; end % skip self loops
        aindex(ciA(riA))=1;
    end
    
    % index the edges in B
    for riB=rpB(vb):rpB(vb+1)-1
        if ciB(riB)==vb, continue; end % skip self loops
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
                % let's see if we can complete a triangle in A from
                % this edge
                for riA2=rpA(va2):rpA(va2+1)-1
                    va3 = ciA(riA2);
                    if va3 == va2, continue; end % skip self-loops
                    if aindex(va3)
                        % va,va2,va3 is a triangle and va,va2 is in b
                        % so check if (va,va3) and (va2,va3) are 
                        % preserved by the mapping
                        
                        va3image = mAB(va3);
                        if va3image && bindex(va3image)
                            % (va,va3) is present, check (va2,va3)
                            for riB=rpB(va2image):rpB(va2image+1)-1
                                b3 = ciB(riB);
                                if mBA(b3)==va3
                                    ntris = ntris + 1;
                                end
                            end
                        end
                    end      
                end
            end
        end
    end
    
    % clear the index of edges in A
    for riA=rpA(va):rpA(va+1)-1
        aindex(ciA(riA))=0;
    end
    
    % clear the index of edges in B
    for riB=rpB(vb):rpB(vb+1)-1
        bindex(ciB(riB))=0;
    end
end
ntris = ntris/6;
