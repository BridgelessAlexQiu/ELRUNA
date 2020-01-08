function [x flag reshist]=full_isorank(A,B,L,a,b,ctype,allstats,pralpha,...
    tol,maxit,verbose)
% FULL_ISORANK Solve an isorank problem on the full biaprtite graph
%
% For IsoRank on the full bipartite graph, we can take advantage of the
% structure of the PageRank problem to let the computation proceed where
% our sparse variant would run out of memory.  The key difference is that
% for the sparse case, we must have S explicitly formed, whereas for the
% full case, the matrix S is just the product graph.  We can then compute
% matrix vector products without forming the matrix S.
%
% X = full_isorank(A,B,L) computes a heuristic X for the network alignment
% problem
%
%   maximize    sum(sum(alpha*L.*X + (beta/2)*(AXB').*X))
%   subject to  X is a matching
%
% where the output X is a set of real number that yield the matching
% after solving a maximum weight matching problem on X.  See the example
% for how to compute an actual matching from the output.  (This formulation
% is identical to our alternate formulations with S, where S = kron(B,A)
% and we have ``unvec''ed the problem.)
%
% x = full_isorank(A,B,L,a,b,ctype,allstats,alpha,tol,maxit,verbose) fully
% specifies all options.  
%
%   a - the value of alpha in the objective
%   b - the value of beta in the objective
%   ctype - the computation type
%     ctype(1) = maximum number of entries in the working vector to keep at
%       each iteration, if ctype(1) == Inf, then we optimize for no
%       truncation of the solution.  So only specify ctype(1) if you really
%       want truncated solutions.
%     ctype(2) = rounding type (only takes effect if allstats=1)
%       ctype(2) = 0 => take the best result of all rounding schemes
%       ctype(2) = 1 => use standard rounding (just X)
%       ctype(2) = 2 => use alpha*L + beta/2*(AXB') as a heuristic instead
%   allstats - if we should round the solution at each iteration
%     our standard procedure is to try every iterate from the method as a
%     potential heuristic and return only the best value.  This can consume
%     extra time, but can often produce slightly better results.  if
%     allstats = 0, then we disable this option and the computation
%     proceeds more quickly, but the results may not be quite as good.
%   pralpha - the value of alpha for the PageRank problem. 
%   tol - the stopping tolerance for the PageRank problem, if the
%     difference between vectors is smaller than tol, we stop.  This option
%     is not very meaningful with a truncated computation.
%   maxit - the maximum number of PageRank iterations
%   verbose - true if we should print information as we go.
%
% The default options are 
%    a = 0.5, b = 1, ctype=[Inf 1], allstats=1, pralpha=b/(a+b), 
%    tol=1e-7, maxit=50, verbose=1
%
% Example:
%   

% David F. Gleich
% Copyright, Stanford University, 2009

% 2008-06-03: Initial version
% 2008-06-04: Added truncated computation following Berger et al.

P = normout(A);
Q = normout(B);
m=size(P,1);
n=size(Q,1);
N = n*m;

if ~exist('L','var') || isempty(L), L=ones(m,n)./N; end
if ~exist('a','var') || isempty(a), a=0.5; end
if ~exist('b','var') || isempty(b), b=1; end
if ~exist('ctype','var') || isempty(ctype), ctype = [Inf 1]; end
if ~exist('tol','var') || isempty(tol), tol=1e-7; end
if ~exist('pralpha','var') || isempty(pralpha), pralpha = b/(a+b); end
if ~exist('maxit','var') || isempty(maxit), maxit=50; end
if ~exist('verbose','var') || isempty(verbose), verbose=true; end
if ~exist('allstats','var') || isempty(allstats), allstats=true; end

alpha = pralpha;
w = L(:);
v = L(:);
if issparse(v) 
    v=v./csum(nonzeros(v));
else
    v=v./csum(v);
end
assert(all(v>=0)); 

if ctype(1)==Inf
    % no truncation
    trunc = false;
else
    trunc = true;
    trunckeep = ctype(1);
end    

rtype = ctype(2);

if allstats
    % extra history information
    rhistsize=5; 

    % Convert A and B into CSR arrays
    [rpA ciA] = sparse_to_csr(A); As.rp = rpA; As.ci = ciA;
    [rpB ciB] = sparse_to_csr(B); Bs.rp = rpB; Bs.ci = ciB;

    if ~trunc
        % we can cache the matching problem
        % allocate ei, and ej 
        ei = reshape(repmat((1:m)',1,n),N,1);
        ej = reshape(repmat((1:n),m,1),N,1);

        % setup the matching problem once
        [rp ci ai tripi] = bipartite_matching_setup(full(w),ei,ej,m,n);       
        clear ei ej;
        xperm = tripi(tripi>0);
    end
else
    % no extra work and small history
    rhistsize=1; 
end

t0 = clock;
if trunc && ~issparse(v)
    warning('full_isorank:truncChanged',...
        'truncated isorank computation requires a sparse matrix L, switching ctype');
    trunc = false;
end
if trunc && trunckeep < nnz(v)
    warning('full_isorank:truncChange',...
        'increasing ctype(1) from %i to %i because L has %i non-zeros',...
        trunckeep, 2*nnz(L), nnz(L));
    trunckeep = 2*nnz(L);
end

if trunc
    x = v; % v is always sparse here
else    
    x = zeros(N,1); 
    if issparse(v), vi=find(v); x(vi)=x(vi)+nonzeros(v); else x=x+v; end
end

delta = 2;
iter = 0;
reshist=zeros(maxit,rhistsize); 

xbest=x; fbest=0; fbestiter=0;
if verbose && allstats% print the header
    fprintf('%5s   %4s   %8s   %7s %7s %7s %7s\n', ...
        'best', 'iter', 'pr-delta', 'obj', 'weight', 'card', 'overlap');
end

while iter<maxit && delta>tol
    if trunc
        y = x./csum(nonzeros(x));
    else
        y=x./csum(x); 
    end
    x=reshape(x,m,n); 
    y=reshape(y,m,n);
    for i=1:n, x(:,i) = alpha*(P'*(y*Q(:,i))); end 
    x=reshape(x,N,1); 
    y=reshape(y,N,1);
    if trunc
        gamma = csum(nonzeros(y)) - csum(nonzeros(x));
        x=x+gamma*v;
        delta = csum(abs(nonzeros(y-x)));
        % truncate now...
        xi = find(x);
        xv = nonzeros(x);
        [xs xp] = sort(xv,1,'descend');
        keep = min(nnz(x),trunckeep);
        x = sparse(xi(xp(1:keep)), 1, xs(1:keep),N,1);
    else
        gamma = csum(y) - csum(x);
        if issparse(v), x(vi)=x(vi)+nonzeros(v)*gamma; else x=x+gamma*v; end
        delta=normdiff(y,x); 
    end
    iter=iter+1; 
    dt=etime(clock, t0); reshist(iter)=delta;
    if allstats
        if trunc
            X = reshape(x,m,n);
            [val ma mb] = bipartite_matching(X);
            val = full(sum(sum(sparse(ma,mb,1,m,n).*X)));
        else
            if rtype==1
                xf = x;
            else
                % compute AXB
                xf = x;
                xf=reshape(xf,m,n); 
                x=reshape(x,m,n);
                for i=1:n, xf(:,i) = (beta/2)*(A*(x*B(:,i))); end 
                xf=reshape(xf,N,1); 
                x=reshape(x,N,1);
                xf = xf + alpha*w;
            end
            ai=zeros(length(tripi),1); ai(tripi>0)=xf(xperm);
            [val ma mb match]= bipartite_matching_primal_dual(rp,ci,ai,tripi,m,n);
            val=full(sum(w(match))); 
        end
        overlap=count_overlap(As,Bs,[ma mb]);
        f = a*val + b*overlap;
        if f>fbest, xbest=x; fbest=f; fbestiter=iter; itermark='*'; 
        else itermark=' ';
        end
    end
    if verbose && allstats
        fprintf('%5s   %4i   %8.1e   %7g %7g %7i %7i   %6.2fs\n', ...
            itermark, iter, delta, f, val, length(ma), overlap, dt);
        reshist(iter,2:end) = [a*val + b*overlap, val, length(ma), overlap];
    elseif verbose
        fprintf('%4i    %8.1e    %6.2f sec\n', iter, delta, dt);
    end

end

flag=delta>tol; reshist=reshist(1:iter);
if allstats, x=xbest; end

x=reshape(x,m,n);

% if flag, s='finished'; else s='solved'; end
% fprintf('%8s %10s(a=%6.4f) in %5i multiplies to %8e tolerance\n', ...
%     s, mfilename, a, nm, dlta);


