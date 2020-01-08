function [Se Le Si]  = make_dir_squares(A,B,L)
% MAKE_DIR_SQUARES Lists all the directed squares between A, B, and L
%
% A directed square for directed graphs returns (i,ip) and (j,jp) where
% i->ip and j->jp preserves the direction of the edge.
%
% Input
% A : n by n sparse matrix, out edges in rows
% B : m by m sparse matrix, out edges in rows
% L : n by m matrix, where L(i,j) indicates that i in A matches to j in B
%     with weight L(i,j)
%
% Output (let s = Si(:,i)), 
% Se : e = Se(:,i) gives the indices of s(1)<->s(3) and e(2) : s(2)<->s(4) in L
% Le : le = Le(i,:) is the list of edges in L corresponding to Se
% Si : s = Si(:,i) is square between (s(1) s(2)) in A and (s(3) s(4)) in B
%
% This function is about half the speed of a C++ implementation.
%
% Example:
%   A = [0 1; 0 0]; B = [0 0; 1 0]; L = [1 1; 1 1];
%   [SeD,LeD] = make_dir_squares(A,B,L); % (i<->j->jp<->ip<-i - dir. squares)
%   [SeU,LeU] = make_squares(A,B,L);     % (i<->j->jp<->ip->i - cycle squares)
%   [Se,Le] = make_squares(A|A',B|B',L); % both types of squares
% 

% David Gleich
% Copyright, Stanford University, 2009

% History
% 2009-08-10: Initial version

n = size(A,1); m = size(B,1);
[rpA ciA] = sparse_to_csr(A); [rpB ciB] = sparse_to_csr(B);

[rpAB ciAB vAB] = sparse_to_csr(L);
Se=zeros(1,2);

buildsi = nargout>2;
if buildsi
    Si=zeros(4,1); 
end    

wv=zeros(m,1); sqi=0;
for i=1:n
    % for each node in A
    
    for ri1=rpA(i):rpA(i+1)-1
        % for each neighbor of A
        ip = ciA(ri1); % (i,ip) is a directed edge in A
        if i==ip, continue; end % skip self-loops
        
        % label everything that node ip in A maps to in B
        for ri2=rpAB(ip):rpAB(ip+1)-1
            wv(ciAB(ri2))=ri2;
        end
    end
    
    
    for ri2=rpAB(i):rpAB(i+1)-1
        % find all the neighbors of i in B
        j = ciAB(ri2); % call them j
        for ri3=rpB(j):rpB(j+1)-1
            % for each neighbor of j
            jp=ciB(ri3); % call it jp
            if j==jp, continue; end
            if wv(jp)>0 
                % check if j links to A (so, we have a square!)
                sqi=sqi+1;
                if sqi>size(Se,1) % just double the arrays
                    Se=[Se; Se]; %#ok<AGROW>
                    if buildsi, Si=[Si Si]; end %#ok<AGROW>
                end                           
                Se(sqi,1)=ri2; Se(sqi,2)=wv(jp);
                if buildsi
                    Si(1,sqi)=i; Si(2,sqi)=ip; Si(3,sqi)=j; Si(4,sqi)=jp;
                end
            end
        end
    end
    
    % remove labels for things in A adjacent to B
    for ri1=rpA(i):rpA(i+1)-1
        % for each neighbor of A
        ip = ciA(ri1); % (i,ip) is a directed edge in A
        if i==ip, continue; end % skip self-loops
        
        % label everything that node ip in A maps to in B
        for ri2=rpAB(ip):rpAB(ip+1)-1
            wv(ciAB(ri2))=0;
        end
    end
end
Se=Se(1:sqi,:);
if buildsi
    Si=Si(:,1:sqi);
end    

if nargout>1
    Le = zeros(nnz(L),3);
    for i=1:n 
        for j=rpAB(i):rpAB(i+1)-1
            Le(j,1)=i; Le(j,2)=ciAB(j); Le(j,3)=vAB(j);
        end
    end
end
