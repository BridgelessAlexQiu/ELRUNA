function [rp ci ai tripi n m]= bipartite_matching_setup(A,ei,ej,n,m)
% BIPARTITE_MATCHING_SETUP Setup a bipartite matching problem
%
%   This code is designed to be used for multiple bipartite matching
%   problems with the same graph structure but different weights.  It saves
%   the common data structure setup and lets you muck with the weights
%   after the setup.  To run the algorithm, use
%   BIPARTITE_MATCHING_PRIMAL_DUAL.
%
%   There are two possible inputs: a sparse matrix A giving the weights
%   in a bipartite matching problem A(i,j) is the weight of 
%   item i (in set 1) to item j (in set 2)
%
%   [setup{:}]=bipartite_matching_setup(A) for a rectangular matrix A 
%
%   [setup{:}]=bipartite_matching_setup(x,ei,ej,n,m) for a matrix stored in
%   triplet format.  Thus, [x(i),ei(i),ej(i)] says that element ei(i) in
%   set 1 should match to element ej(i) in set 2.  (Think of this as
%   [ei,ej,x]=find(A) in comparision to the first format.)
%
%   See the documentation and code BIPARTITE_MATCHING to see an advantage
%   of the triplet input.
%
% Example:
%   [rp ci ai tripi n m] = bipartite_matching_setup(A);
%   [val m1 m2] = bipartite_matching_primal_dual(rp, ci, ai, tripi, n, m);
%
%   % is the equivalent of
%
%   [valA mA1 mA2] = bipartite_matching(A);
%   val, valA
%
% See also BIPARTITE_MATCHING, BIPARTITE_MATCHING_PRIMAL_DUAL

% History
% :2010-05-28: Added comments

% David Gleich and Ying Wang
% Copyright, Stanford University, 2008-2010
% Computational Approaches to Digital Stewardship


if nargin == 1
    [nzi nzj nzv]=find(A); 
    [n m]=size(A);
    triplet = 0;
elseif nargin >= 3 && nargin <= 5    
    nzi = ei;
    nzj = ej;
    nzv = A;
    if ~exist('n','var') || isempty(n), n = max(nzi); end
    if ~exist('m','var') || isempty(m), m = max(nzj); end
    triplet = 1;
else    
    error(nargchk(3,5,nargin,'struct'));
end
nedges = length(nzi);

rp = ones(n+1,1); % csr matrix with extra edges
ci = zeros(nedges+n,1);
ai = zeros(nedges+n,1);
if triplet, tripi = zeros(nedges+n,1); % triplet index
else tripi = [];
end

%
% 1. build csr representation with a set of extra edges from vertex i to
% vertex m+i
%
rp(1)=0;
for i=1:nedges
    rp(nzi(i)+1)=rp(nzi(i)+1)+1;
end
rp=cumsum(rp); 
for i=1:nedges
    if triplet, tripi(rp(nzi(i))+1)=i; end % triplet index
    ai(rp(nzi(i))+1)=nzv(i);
    ci(rp(nzi(i))+1)=nzj(i);
    rp(nzi(i))=rp(nzi(i))+1;
end
for i=1:n % add the extra edges
    if triplet, tripi(rp(i)+1)=-1; end % triplet index
    ai(rp(i)+1)=0;
    ci(rp(i)+1)=m+i;
    rp(i)=rp(i)+1;
end
% restore the row pointer array
for i=n:-1:1
    rp(i+1)=rp(i);
end
rp(1)=0;
rp=rp+1;

%
% 1a. check for duplicates in the data
%
colind = false(m+n,1);
for i=1:n
    for rpi=rp(i):rp(i+1)-1
        if colind(ci(rpi)), error('bipartite_matching:duplicateEdge',...
            'duplicate edge detected (%i,%i)',i,ci(rpi)); 
        end
        colind(ci(rpi))=1;
    end
    for rpi=rp(i):rp(i+1)-1, colind(ci(rpi))=0; end % reset indicator
end
