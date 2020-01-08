function [xbest fupper hist] = netalign_lagrange(S,w,a,b,li,lj,stepm,rtype,maxiter,verbose)
% NETALIGN_LAGRANGE Solve the network alignment problem
% with Lagrangean relaxation
% 

% David F. Gleich, Ying Wang, and Mohsen Bayati
% Copyright, Stanford University, 2008-2009
% Computational Approaches to Digital Stewardship

if ~exist('a','var') || isempty(a), a=1; end
if ~exist('b','var') || isempty(b), b=1; end
if ~exist('stepm','var') || isempty(stepm), stepm=100; end
if ~exist('rtype','var') || isempty(rtype), rtype=1; end
if ~exist('maxiter', 'var') || isempty(maxiter), maxiter=1000; end
if ~exist('verbose', 'var') || isempty(verbose), verbose=1; end 

m = max(li);
n = max(lj);

[rp ci ai tripi matn matm] = bipartite_matching_setup(w,li,lj,m,n); 
mperm = tripi(tripi>0); % a permutation for the matching problem

S = triu(S);
S = double(S);
U = sparse(size(S,1),size(S,2));
xbest = w;
xbest(:) = 0;

flower = 0;
fupper = Inf;
next_reduction_iteration = stepm; % reduce the step
gamma = 1;

hist = zeros(maxiter,7);

if verbose % print the header
    fprintf('%5s   %4s   %8s   %7s %7s  %7s %7s %7s %7s\n', ...
        'best', 'iter', 'norm-u', 'lower','upper', 'obj', 'weight', 'card', 'overlap');
end    
for iter = 1:maxiter
    nw = a * w + b *  (sum(max(0, .5 * S + U), 2) + sum(max(0, .5 * S - U),1)');
    %[val ma mb mi]= bipartite_matching(nw,li,lj,m,n);
    ai=zeros(length(tripi),1); ai(tripi>0)=nw(mperm);
    [val ma mb mi]= bipartite_matching_primal_dual(rp,ci,ai,tripi,matn,matm);
    % compute statistics 
    matchval = mi'*w;
    overlap = mi'*S*mi; % no divide by 2 is okay, because S = triu(S) :-).
    card = length(ma);
    f = a*matchval + b*overlap;
    
    if val<fupper
        fupper=val;
        next_reduction_iteration = iter+stepm;
    end
    if f>flower
        flower=f;
        itermark = '*';
        xbest = mi;
    else
        itermark = ' ';
    end        
    
    if rtype==1
        % no work
    elseif rtype==2
        mw = S*mi;
        mw = mw + S'*mi;
        mw = a*w + b/2*mw;
       
        ai=zeros(length(tripi),1); ai(tripi>0)=mw(mperm);
        [val ma mb mx] = bipartite_matching_primal_dual(rp,ci,ai,tripi,matn,matm);
        
        card = length(ma);
        matchval = mx'*w;
        overlap = mx'*S*mx;
        f = a*matchval + b*overlap;
        
        if f>flower
            flower=f;
            itermark = '**';
            mi = mx;
            xbest = mw;
        end
    end
    
    % report on current iter
    hist(iter,1:end) = [norm(nonzeros(U),1), flower, fupper, f, matchval, card, overlap];
    
    if verbose
        fprintf('%5s   %4i   %8.1e   %7g %7g  %7g %7g %7i %7i\n', ...
            itermark, iter, norm(nonzeros(U),1), ...
            flower, fupper, ...
            f, matchval, card, overlap);
    end
    
    if iter==next_reduction_iteration
        gamma = gamma*0.5;
        if verbose
            fprintf('%5s   %4s   reducing step to %g\n', '', '', gamma);
        end
        next_reduction_iteration = iter+stepm;
    end
    
    U = bound(U - (diag(sparse(mi)) * S - S * diag(sparse(mi))) * gamma, -.5, .5);
    
end

function S=bound(S,a,b)
S=spfun(@(x) min(max(x,a),b), S);

