function [mbest hista histb] = netalignmbp(S,w,a,b,li,lj,gamma,dtype,maxiter,verbose)
% NETALIGNMBP Solve the network alignment problem with Belief Propagation
%
% This version of network alignment uses the matrix formulation of the 
% algorithm.

% David F. Gleich, Ying Wang, and Mohsen Bayati
% Copyright, Stanford University, 2007-2009
% Computational Approaches to Digital Stewardship

if ~exist('a','var') || isempty(a), a=1; end
if ~exist('b','var') || isempty(b), b=1; end
if ~exist('gamma','var') || isempty(gamma), gamma=0.99; end
if ~exist('dtype', 'var') || isempty(dtype), dtype=2; end
if ~exist('maxiter', 'var') || isempty(maxiter), maxiter=100; end
if ~exist('verbose', 'var') || isempty(verbose), verbose=1; end 

nedges = length(li); nsquares = nnz(S)/2; m = max(li); n = max(lj);

% the following is elegant, but inefficient :-(
%Ar = sparse(li,1:nedges,1,m,nedges); [ari arj arv]=find(Ar'*Ar-speye(nedges));
%Ac = sparse(lj,1:nedges,1,n,nedges); [aci acj acv]=find(Ac'*Ac-speye(nedges));

% Initialize the messages
y = zeros(nedges,1); z = y; Sk = 0*S; 
if dtype>1, d = y; end % needed for damping scheme
% Initialize a few parameters
damping = gamma; curdamp = 1; iter = 1; 

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
[rp ci ai tripi matn matm] = bipartite_matching_setup(...
                                    w,li,lj,m,n);
mperm = tripi(tripi>0);

while iter<=maxiter
    curdamp = damping*curdamp;
    Sknew = bound(Sk' + b*S,0,b);
    if dtype>1, dold=d; end
    d = sum(Sknew,2);
    
    ynew = a*w - max(0,implicit_maxprod(n,lj,z)) + d;
    znew = a*w - max(0,implicit_maxprod(m,li,y)) + d;
    % NOTE in comparison netalignbp, othersum isn't needed because othersum
    % of Sknew = d*S - Sknew
    Skt = diag(sparse(ynew+znew-a*w-d))*S-Sknew;
    if dtype==1
        Sk = curdamp*Skt+ (1-curdamp)*Sk;
        y = curdamp*ynew+(1-curdamp)*y;
        z = curdamp*znew+(1-curdamp)*z;
    elseif dtype==2
        prev = (y+z-a*w+dold);
        y = ynew+(1-curdamp)*prev;
        z = znew+(1-curdamp)*prev;
        clear prev;
        Sk = Skt + (1-curdamp)*(Sk+Sk'-b*S);
    elseif dtype==3
        prev = (y+z-a*w+dold);
        y = curdamp*ynew+(1-curdamp)*prev;
        z = curdamp*znew+(1-curdamp)*prev;
        clear prev;
        Sk = curdamp*Skt + (1-curdamp)*(Sk+Sk'-b*S);
    end
    hista(iter,:) = round_messages(y,S,w,a,b,rp,ci,tripi,matn,matm,mperm);
    histb(iter,:) = round_messages(z,S,w,a,b,rp,ci,tripi,matn,matm,mperm);
    if hista(iter,1)>fbest
        fbestiter=iter; mbest=y; fbest=hista(iter,1);
    end
    if histb(iter,1)>fbest
        fbestiter=-iter; mbest=z; fbest=histb(iter,1);
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

end

function S=bound(S,a,b)
  S=spfun(@(x) max(x+b,0) - max(x+a,0),S); 
end
function y=maxprod(ai,aj,av,m,x) 
  y=-inf*ones(m,1);
  for i=1:numel(ai), y(ai(i)) = max(y(ai(i)),av(i)*x(aj(i))); end
end
function y=implicit_maxprod(n,ai,x)
% implicitly compute 
%   Ai=sparse(ai,1:length(ai),1,n,length(z))
%   A=Ar'*Ar - speye(length(z))
%   maxprod(A,x)
% which has a very nice structure if you look at the actual summation
% definition.  It is just the maximum value 
  N = length(ai);
  y=-inf*ones(N,1);
  max1 = -inf*ones(n,1);
  max2 = -inf*ones(n,1);
  max1ind = zeros(n,1);
  for i=1:N
    if x(i)>max2(ai(i))
      if x(i)>max1(ai(i))
          max2(ai(i)) = max1(ai(i));
          max1(ai(i)) = x(i);
          max1ind(ai(i)) = i;
      else
          max2(ai(i)) = x(i);
      end
    end
  end
  for i=1:N
    if i==max1ind(ai(i))
      y(i)=max2(ai(i));
    else
      y(i)=max1(ai(i));
    end
  end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function info=round_messages(messages,S,w,alpha,beta,rp,ci,tripi,n,m,perm)
ai=zeros(length(tripi),1); ai(tripi>0)=messages(perm);
[val ma mb mi]= bipartite_matching_primal_dual(rp,ci,ai,tripi,n,m);
matchweight = sum(w(mi)); cardinality = sum(mi); overlap = (mi'*(S*double(mi)))/2; 
f = alpha*matchweight + beta*overlap;
info = [f matchweight cardinality overlap];
end
