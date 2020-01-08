function [mbest, hista, histb] = netalignbp(S,w,a,b,li,lj,gamma,dtype,maxiter,verbose)
% NETALIGNBP Solve the network alignment problem with Belief Propagation
%
% 

% David F. Gleich, Ying Wang, and Mohsen Bayati
% Copyright, Stanford University, 2007-2009
% Computational Approaches to Digital Stewardship

%  History
%  2009-06-02: Implemented Mohsen's new updates to get a higher overlap

if ~exist('a','var') || isempty(a), a=1; end
if ~exist('b','var') || isempty(b), b=1; end
if ~exist('gamma','var') || isempty(gamma), gamma=0.99; end
if ~exist('dtype', 'var') || isempty(dtype), dtype=2; end
if ~exist('maxiter', 'var') || isempty(maxiter), maxiter=100; end
if ~exist('verbose', 'var') || isempty(verbose), verbose=1; end 

nedges = length(li);
nsquares = nnz(S)/2;
m = max(li);
n = max(lj);

% compute a vector that allows us to transpose data between squares.  
% Recall the BP algorithm requires edge(i,j) to send messages to edge(r,s)
% when (i,j) and (r,s) form a square.  However, edge(i,j) needs information
% the information that (r,s) sent it from the previous iteraton.  
% If we imagine that each non-zero of S has a value, we want to tranpose
% these values.
[sui, suj] = find(triu(S,1)); % only consider each square once.
SI = sparse(sui,suj,1:length(sui),size(S,1),size(S,2)); % assign indices 
SI = SI + SI'; % SI now has symmetric indices 
[si, sj, sind] = find(SI);
SP = sparse(si,sind,true,size(S,1),nsquares); % each column in SP has 2 nz
[sij, sijrs] = find(SP);
sind = (1:nnz(SP))';
spair = sind; spair(1:2:end) = sind(2:2:end); spair(2:2:end) = sind(1:2:end);
% sij, sijrs maps between rows and squares
% spair is now an indexing vector that accomplishes what we need

% Initialize the messages
ma = zeros(nedges,1);
mb = ma;
ms = zeros(nnz(S),1);
sums = zeros(nedges,1);

damping = gamma;
curdamp = 1;
iter = 1;
alpha = a;
beta = b;

% Initialize history
hista = zeros(maxiter,4); % history of messages from ei->a vertices
histb = zeros(maxiter,4); % history of messages from ei->b vertices
fbest = 0; fbestiter = 0;
if verbose % print the header
    fprintf('%4s   %4s   %7s %7s %7s %7s   %7s %7s %7s %7s\n', ...
        'best', 'iter', 'obj_ma', 'wght_ma', 'card_ma', 'over_ma', ...
        'obj_mb', 'wght_mb', 'card_mb', 'over_mb');
end

% setup the matching problem once
[rp, ci, ai, tripi, matn, matm] = bipartite_matching_setup(...
                                    w,li,lj,m,n);         
mperm = tripi(tripi>0); % a permutation for the matching problem
clear ai;

while iter<=maxiter
    prevma = ma;
    prevmb = mb;
    prevms = ms;
    prevsums = sums;
    curdamp = damping*curdamp;
    
    omaxb = max(othermaxplus(2,li,lj,mb,m,n),0);
    omaxa = max(othermaxplus(1,li,lj,ma,m,n),0);
    
    msflip = ms(spair); % swap ij->ijrs to rs->ijrs 
    mymsflip = msflip+beta;
    mymsflip = min(beta,mymsflip);
    mymsflip = max(0,mymsflip);
        
    sums = accumarray(sij,mymsflip,[nedges 1],@sum,0);
    
    ma = alpha*w - omaxb + sums;
    mb = alpha*w - omaxa + sums;
    
    ms = alpha*w(sij)-(omaxb(sij) + omaxa(sij));
    ms = ms + othersum(sij,sijrs,mymsflip,nedges,nsquares);

    % Original updates
    if dtype==1
        ma = curdamp*(ma) + (1-curdamp)*(prevma);
        mb = curdamp*(mb) + (1-curdamp)*(prevmb);
        ms = curdamp*(ms) + (1-curdamp)*(prevms);
    elseif dtype==2
        ma = ma + (1-curdamp)*(prevma+prevmb-alpha*w+prevsums);
        mb = mb + (1-curdamp)*(prevmb+prevma-alpha*w+prevsums);
        ms = ms + (1-curdamp)*(prevms+prevms(spair)-beta);
    elseif dtype==3
        ma = curdamp*ma + (1-curdamp)*(prevma+prevmb-alpha*w+prevsums);
        mb = curdamp*mb + (1-curdamp)*(prevmb+prevma-alpha*w+prevsums);
        ms = curdamp*ms + (1-curdamp)*(prevms+prevms(spair)-beta);
    end
    
    % now compute the matchings
    hista(iter,:) = round_messages(ma,S,w,alpha,beta,rp,ci,tripi,matn,matm,mperm);
    histb(iter,:) = round_messages(mb,S,w,alpha,beta,rp,ci,tripi,matn,matm,mperm);
    if hista(iter,1)>fbest
        fbestiter=iter; mbest=ma; fbest=hista(iter,1);
    end
    if histb(iter,1)>fbest
        fbestiter=-iter; mbest=mb; fbest=histb(iter,1);
    end
    
    if verbose
        if fbestiter==iter, bestchar='*a'; 
        elseif fbestiter==-iter, bestchar='*b';
        else bestchar='';
        end
        fprintf('%4s   %4i   %7g %7g %7i %7i   %7g %7g %7i %7i\n', ...
            bestchar, iter, hista(iter,:), histb(iter,:));
    end
    iter=iter+1;
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function info=round_messages(messages,S,w,alpha,beta,rp,ci,tripi,n,m,perm)
ai=zeros(length(tripi),1); ai(tripi>0)=messages(perm);
[val, ma, mb, mi]= bipartite_matching_primal_dual(rp,ci,ai,tripi,n,m);
matchweight = sum(w(mi)); cardinality = sum(mi); overlap = (mi'*(S*double(mi)))/2; 
f = alpha*matchweight + beta*overlap;
info = [f matchweight cardinality overlap];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function omp=othermaxplus(dim,li,lj,lw,m,n)
% OTHERMAXPLUS Apply the other-max-plus operator to a sparse matrix
%
% The other-max-plus operator applies the max-plus aggegration function
% over the rows or columns of the matrix, where, for 
% each non-zeros, the non-zero itself cannot be the maximum.  Consequently,
% Hence, it's the max-plus of all the "other" elements in the row or column
% (which is controlled by dim).
%
% omp=othermaxplus(dim,li,lj,lw,m,n) applies the other-max-plus operator
% to the matrix sparse(li, lj, lw, m, n).  The return value omp gives
% the other-max-plus value for each non-zero element, e.g. the matrix
% is sparse(li, lj, omp, m, n).

if dim==1
    % max-plus over cols
    i1 = lj;
    i2 = li;
    N = n;
else
    % max-plus over rows
    i1 = li;
    i2 = lj;
    N = m;
end

% the output of the other-max-plus is either the maximum element 
% in the row or column (if the element itself isn't the maximum) or
% the second largest element in the row or column (if the element itself
% IS the maximum).

dimmax1 =0*ones(N,1);      % largest value
dimmax2 = 0*ones(N,1);     % second largest value, 
% this is correct because of the definition of the max-plus function.  
dimmaxind = zeros(N,1);   % index of largest value
nedges = length(li);

for i=1:nedges
    if lw(i) > dimmax2(i1(i))
        if lw(i) > dimmax1(i1(i))
            dimmax2(i1(i)) = dimmax1(i1(i));
            dimmax1(i1(i)) = lw(i);
            dimmaxind(i1(i)) = i2(i);
        else
            dimmax2(i1(i)) = lw(i);
        end
    end 
end

omp = zeros(size(lw));
for i=1:nedges
    if i2(i) == dimmaxind(i1(i))
        omp(i) = dimmax2(i1(i));
    else
        omp(i) = dimmax1(i1(i));
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function os=othersum(si,sj,s,m,n) %#ok<INUSD,INUSL>
% OTHERSUM Compute the sum of each column of the matrix, without each
% individual entry.  This corresponds to a matrix where each entry is the
% sum of each column but with each entry subtracted.  

rowsum=accumarray(si,s,[m,1]);
os=rowsum(si)-s;    

