function [Se, Le, Si]  = make_squares(A,B,L)
% MAKE_SQUARES Returns a list of all the squares between A, B, and L
%
% Input
% A : n by n sparse matrix, out edges in rows
% B : m by m sparse matrix, out edges in rows
% L : n by m matrix, where L(i,j) indicates that i in A matches to j in B
%     with weight L(i,j)
%
% Output
% Se : e = Se(:,i) gives the indices of s(1)<->s(3) and e(2) : s(2)<->S(4) in L
% Le : le = Le(i,:) is the list of edges in L corresponding to Se
% Si : s = Si(:,i) is square between (s(1) s(2)) in A and (s(3) s(4)) in B
%
% This function is about half the speed of a C++ implementation.

% David Gleich
% Copyright, Stanford University, 2008

% History
% 2008-04-04: Initial version
% 2008-04-07: Changed to growing Se,Si inside the loop by doubling,
%             eliminating the need for twice the computation.
% 2009-05-29: Eliminated Si computation unless requested.
% 2009-06-02: Transposed the Se array

n = size(A,1); m = size(B,1);
[rpA, ciA] = sparse_to_csr(A); [rpB, ciB] = sparse_to_csr(B);

[rpAB, ciAB, vAB] = sparse_to_csr(L);
Se=zeros(1,2);

buildsi = nargout>2;
if buildsi
    Si=zeros(4,1); 
end    

wv=zeros(m,1); sqi=0;
for i=1:n
    % label everything in to i in B
    for ri1=rpAB(i):rpAB(i+1)-1
        wv(ciAB(ri1))=ri1;
    end
    for ri1=rpA(i):rpA(i+1)-1
        ip = ciA(ri1);
        if i==ip, continue; end
        for ri2=rpAB(ip):rpAB(ip+1)-1
            jp = ciAB(ri2);
            for ri3=rpB(jp):rpB(jp+1)-1
                j=ciB(ri3);
                if j==jp, continue; end
                if wv(j)>0
                    % we have a square!
                    sqi=sqi+1;
                    if sqi>size(Se,1) % just double the arrays
                        Se=[Se; Se]; %#ok<AGROW>
                        if buildsi, Si=[Si Si]; end %#ok<AGROW>
                    end                           
                    Se(sqi,1)=ri2; Se(sqi,2)=wv(j);
                    if buildsi
                        Si(1,sqi)=i; Si(2,sqi)=ip; Si(3,sqi)=j; Si(4,sqi)=jp;
                    end
                end
            end
        end
    end
    % remove labels for things in in adjacent to B
    for ri1=rpAB(i):rpAB(i+1)-1
        wv(ciAB(ri1))=0;
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
