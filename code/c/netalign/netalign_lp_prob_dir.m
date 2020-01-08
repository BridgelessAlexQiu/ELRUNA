function [f,A,b,si,sj]=netalign_lp_prob(S,w,alpha,beta,li,lj,form)
% NETALIGN_LP Formulate the data for solving network alignment as an LP.
%
% [f,A,b]=netalign_lp_prob(S,w,alpha,beta,li,lj) yields the data for the
% mixed integer linear program
%   maximize    f'*x
%   subject to  0 <= Ax <= 1
%               x(1:length(li)) is 0 or 1
% that is equivalent to the quadratic binary program
%   maximize    alpha*w'*x + beta/2*x'*S*x
%   subject to  x is a matching on li, lj
% 
% [f,A,b]=netalign_lp_prob(S,w,alpha,beta,li,lj,'all') gives a formulation
% with more variables and constraints.
%
% [f,A,b,Si,Sj]=netalign_lp_prob(S,w,alpha,beta,li,lj,...) returns
% the information to construct the approximate matrix S 


if ~exist('form','var') || isempty(form), form='sym'; end

nedges = length(li); 
m = max(li); 
n = max(lj);

formadj = 1;

nsquares = nnz(S);
[si sj] = find(S);
formadj = 0.5;
Sind = sparse(si,sj,1:nsquares,nedges,nedges); % index the squares

S1 = sparse(si,1:nsquares,1,nedges,nsquares);
S2 = sparse(sj,1:nsquares,1,nedges,nsquares);


f = [alpha*w(:); beta*formadj*ones(nsquares,1)];

Ar = sparse(li,1:nedges,1,m,nedges); 
Ac = sparse(lj,1:nedges,1,n,nedges); 

Amatch = [Ar sparse(m,nsquares); Ac sparse(n,nsquares)];
bmatch = ones(m+n,1);

Aval = [-S1' speye(nsquares); -S2' speye(nsquares)];
bval = zeros(2*nsquares,1);

A = [Amatch; Aval];
b = [bmatch; bval];

if strcmp(form,'tight')
    % create a tight lp form
    
    % This means we add constraints
    %   Sum over l  S_{ij,kl} \le x_ij for all ij and k
    %   Sum over k  S_{ij,kl} \le x_ij for all ij and l
    %
    % In other words, we go through S row by row (S is not-symmetric
    % so column access is equivalent faster and we use St below)
    % and find all k such that S_{ij,kl} is non-zero.
   
    St = S';
  
    %
    % For each k, we add a constraint of the form 
    %   Sum over l  S_{ij,kl} \le x_ij for all ij and k    
    
    %
    % Step 1. compute the number of constraints
    %
    nrows = 0;   % number of "tight" lp constraints
    nterms = 0;  % number of non-zeros in tight lp constraints
    % initialize counters to check for uniqueness and duplicates
    count_ks = zeros(nedges,1);
    count_ls = zeros(nedges,1);
    for i=1:nedges
        % for each column in St (row in S), find the number of constraints we'll add
        % (nnewrows) and the number of non-zeros (added directly to nterms)
        col_nonzeros = find(St(:,i));
        nnewrows = 0;
        for nzi = 1:length(col_nonzeros)
            kl_ind = col_nonzeros(nzi);
            if count_ks(li(kl_ind)) == 0
                count_ks(li(kl_ind)) = 1;
                nnewrows = nnewrows + 1;
            end
            if count_ls(lj(kl_ind)) == 0
                count_ls(lj(kl_ind)) = 1;
                nnewrows = nnewrows + 1;
            end
        end
        % update the counts
        nrows = nrows + nnewrows;
        nterms = nterms + 2*length(col_nonzeros) + nnewrows;
        for nzi = 1:length(col_nonzeros) % reset the counters
            kl_ind = col_nonzeros(nzi);
            count_ks(li(kl_ind)) = 0;
            count_ls(lj(kl_ind)) = 0;
        end
    end
    
    % alloc triplet arrays for tight LP constraints
    tighti = zeros(nterms,1); 
    tightj = zeros(nterms,1);
    tightv = zeros(nterms,1);
    curconstraint = 1;
    curnz = 1;
    
    Sindt = Sind';
    for i=1:nedges
        % run through all columns of S again and extra data on the 
        % matching problems in each column
        ij_ind = i;
        Scol = Sindt(:,i);
        [col_nonzeros ignore yinds] = find(Scol); 
        ks = zeros(length(col_nonzeros),1);
        ls = ks;
        for nzi = 1:length(col_nonzeros)
            kl_ind = col_nonzeros(nzi);
            ks(nzi) = li(kl_ind);
            ls(nzi) = lj(kl_ind);
        end
        
        % sort the k's so we can run through the data efficiently
        [sorted_ks,perm] = sort(ks);
        
        pi=1;
        while pi<=length(col_nonzeros)
            k = sorted_ks(pi);
            % count the number of terms we are going to sum
            % for this k (this is the sum over l)
            pi2 = pi;
            nsumterms = 0;
            while pi2<=length(col_nonzeros) && sorted_ks(pi2) == k
                nsumterms = nsumterms + 1;
                pi2 = pi2+1;
            end
            ti = 1;                       % current term
            terms = zeros(nsumterms+1,1); % the list of terms we will sum
            
            % add the current entry to the sum
            terms(ti) = yinds(perm(pi))+nedges;
            ti = ti+1;
            pi = pi+1;
            
            % build up all the other l with start point k
            while pi<=length(col_nonzeros) && sorted_ks(pi) == k
                % while we aren't too far and we still start with k
                terms(ti) = yinds(perm(pi))+nedges;
                ti = ti+1;
                pi = pi+1;
            end
            
            % add the right hand term (x_ij)
            terms(end) = ij_ind;
            
            tighti(curnz:curnz+nsumterms) = curconstraint;
            tightj(curnz:curnz+nsumterms) = terms;
            tightv(curnz:curnz+nsumterms-1) = 1;
            tightv(curnz+nsumterms) = -1; % this means sum_l terms - x_ij <= 0
            curnz = curnz + nsumterms + 1;
            curconstraint = curconstraint+1;
        end
        
        %
        % Now run the same thing but for ls's instead
        
        [sorted_ls,perm] = sort(ls);
        
        pi=1;
        while pi<=length(col_nonzeros)
            l = sorted_ls(pi);
            pi2 = pi;
            nsumterms = 0;
            while pi2<=length(col_nonzeros) && sorted_ls(pi2) == l
                nsumterms = nsumterms + 1;
                pi2 = pi2+1;
            end
            ti = 1;                   % current term
            terms = zeros(nsumterms+1,1);
            terms(ti) = yinds(perm(pi))+nedges;
            ti = ti+1;
            pi = pi+1;
            
            % build up all the other l with start point k
            while pi<=length(col_nonzeros) && sorted_ls(pi) == l
                % while we aren't too far and we still start with l
                terms(ti) = yinds(perm(pi))+nedges;
                ti = ti+1;
                pi = pi+1;
            end
            terms(end) = ij_ind;
            tighti(curnz:curnz+nsumterms) = curconstraint;
            tightj(curnz:curnz+nsumterms) = terms;
            tightv(curnz:curnz+nsumterms-1) = 1;
            tightv(curnz+nsumterms) = -1;
            curnz = curnz + nsumterms + 1;
            curconstraint = curconstraint+1;
        end
    end
    % build the tight constraint matrix and add it.
    Atight = sparse(tighti,tightj,tightv,nrows,nedges+nsquares);
    A = [A; Atight];
    b = [b; zeros(nrows,1)];
end