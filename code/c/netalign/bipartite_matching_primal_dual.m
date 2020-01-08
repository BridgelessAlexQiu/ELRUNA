function [val m1 m2 mi]=bipartite_matching_primal_dual(...
                            rp, ci, ai, tripi, n, m)
% BIPARTITE_MATCHING_PRIMAL_DUAL Solve a max-weight matching instance
%
%   This code is designed to be used after calling
%   BIPARTITE_MATCHING_SETUP
%   and implements the algorithm.
%
%   [val m1 m2] = bipartite_matching_primal_dual(rp,ci,ai,tripi,n,m)
%   where the options are the output of bipartite_matching_setup.
%
%   When tripi is not empty (which occurs when bipartite_matching_setup
%   was called with triplet input), then there is an additional output:
%   [val m1 m2 mi] = bipartite_matching_primal_dual(...)
%   See BIPARTITE_MATCHING for a description of the additional output
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
% See also BIPARTITE_MATCHING, BIPARTITE_MATCHING_SETUP

% History
% :2010-05-28: Added comments

% David Gleich and Ying Wang
% Copyright, Stanford University, 2008-2010
% Computational Approaches to Digital Stewardship

alpha=zeros(n,1); % variables used for the primal-dual algorithm
beta=zeros(n+m,1);
queue=zeros(n+m,1);
t=zeros(n+m,1);
match1=zeros(n,1);
match2=zeros(n+m,1);
tmod = zeros(n+m,1);
ntmod=0;


% 
% initialize the primal and dual variables
%
for i=1:n
    for rpi=rp(i):rp(i+1)-1
        if ai(rpi) > alpha(i), alpha(i)=ai(rpi); end
    end
end
% dual variables (beta) are initialized to 0 already
% match1 and match2 are both 0, which indicates no matches
i=1;
while i<=n
    % repeat the problem for n stages
    
    % clear t(j)
    for j=1:ntmod, t(tmod(j))=0; end
    ntmod=0;
    

    % add i to the stack
    head=1; tail=1;
    queue(head)=i; % add i to the head of the queue
    while head <= tail && match1(i)==0
        k=queue(head);
        for rpi=rp(k):rp(k+1)-1
            j = ci(rpi);
            if ai(rpi) < alpha(k)+beta(j) - 1e-8, continue; end % skip if tight
            if t(j)==0,
                tail=tail+1; queue(tail)=match2(j);
                t(j)=k;
                ntmod=ntmod+1; tmod(ntmod)=j;
                if match2(j)<1,
                    while j>0, 
                        match2(j)=t(j);
                        k=t(j);
                        temp=match1(k);
                        match1(k)=j;
                        j=temp;
                    end
                    break; % we found an alternating path
                end
            end
        end
        head=head+1;
    end
    
    if match1(i) < 1, % still not matched, so update primal, dual and repeat
        theta=inf;
        for j=1:head-1
            t1=queue(j);
            for rpi=rp(t1):rp(t1+1)-1
                t2=ci(rpi);
                if t(t2) == 0 && alpha(t1) + beta(t2) - ai(rpi) < theta,
                    theta = alpha(t1) + beta(t2) - ai(rpi);
                end
            end
        end
        
        for j=1:head-1, alpha(queue(j)) = alpha(queue(j)) - theta; end
        
        for j=1:ntmod, beta(tmod(j)) = beta(tmod(j)) + theta; end
            
        continue;
    end
        
    i=i+1; % increment i
end

val=0;
for i=1:n
    for rpi=rp(i):rp(i+1)-1
        if ci(rpi)==match1(i), val=val+ai(rpi); end
    end
end
noute = 0; % count number of output edges
for i=1:n
    if match1(i)<=m, noute=noute+1; end
end
m1=zeros(noute,1); m2=m1; % copy over the 0 array
noute=1;
for i=1:n
    if match1(i)<=m, m1(noute)=i; m2(noute)=match1(i);noute=noute+1; end
end

if nargout>3
    mi= false(length(tripi)-n,1);
    for i=1:n
        for rpi=rp(i):rp(i+1)-1
            if match1(i)<=m && ci(rpi)==match1(i), mi(tripi(rpi))=1; end
        end
    end
end
