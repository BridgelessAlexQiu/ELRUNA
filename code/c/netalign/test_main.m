%% Main testing script

%% evaluate_alignment
A = [0 1 1; 1 0 1; 1 1 0];
B = [0 1 1 1; 1 0 1 1; 1 1 0 1; 1 1 1 0];
ma = [1 2 3];
mb = [1 2 3];
evaluate_alignment(A,B,ma,mb);
ma = [1 2 3];
mb = [2 3 4];
evaluate_alignment(A,B,ma,mb);



%% bipartite_matching
msgid='bipartite_matching:testFailed';
[val ma mb mi] = bipartite_matching([1 2.5],[1 1], [1 2]);
if val~=2.5, error(msgid,'incorrect matching value=%f ~= %f', val, 2.5); end
if any(mi~=[0; 1]), error(msgid,'incorrect matching indicator'); end

try
    [val ma mb mi] = bipartite_matching([1 2 2.5],[1 1 1], [1 1 2]);
    error(msgid,'duplicate edge test failed');
catch
end

% test the example;
load('../data/example-overlap.mat');
val = bipartite_matching(w,li,lj);
val = bipartite_matching(sparse(li,lj,w,max(li),max(lj)));

%% isorank

%test the example
load('../data/example-overlap.mat');
a = 3; b = 17;
x=isorank(S,w,a,b,li,lj); % best solution at any iterate
[weight overlap]=mwmround(x,S,w,li,lj);
x=isorank(S,w,a,b); % only the converged isorank solution

%% load_netalign_problem
[S,w,li,lj] = load_netalign_problem('musm-homo');
[S,w,li,lj,A,B,L,extra] = load_netalign_problem('example-2');
[S,w,li,lj] = load_netalign_problem('lcsh2wiki-small');