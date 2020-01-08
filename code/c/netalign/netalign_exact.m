function xbest=netalign_exact(S,w,a,b,li,lj)
% NETALIGN_EXACT Solve the network alignment with exhaustive enumeration
%
% x=netalign_exact(S,w,a,b,li,lj) solves the binary QP
%
%   max  a*(w'*x)+b*(x'*S*x)/2
%   s.t. x is matching on the edges li, lj
%
% by exhaustively enumerating all variables x. 
%   
% Example:
%   load('../data/example-overlap.mat');
%   a = 3; b = 17;
%   x=netalign_exact(S,w,a,b,li,lj); % best solution at any iterate
%   [weight overlap]=mwmround(x,S,w,li,lj);

% David F. Gleich
% Copyright, Stanford University, 2009

%  2009-02-15: Approximate initial coding date

n = size(S,1);
if n>=25
    warning('netalign_exact:bigProblem',...
        ['Your problem has n=%i, which takes %g steps, ' ...
         'consider an approximate solver.'], n, exp(log(2)*n));
end

x = zeros(n,1);
j = n;
maxval = 0;
xbest = x;
while j>=1
    j = n;
    while j>=1 && x(j)==1
        j=j-1; 
    end
    if j<1, break; end
    x(j)=1;
    for k=(j+1):n, x(k)=0; end
    
    if all(accumarray(li,x)<=1) && all(accumarray(lj,x)<=1)
        val = a*w'*x + b*x'*S*x/2;
        if val>maxval
            maxval = val;
            xbest = x;
        end
    end
end 
        
