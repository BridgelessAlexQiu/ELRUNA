%% A Demonstration of the Matlab network alignment tools

%% Setup the data directory
datadir = fullfile('..','data');

%% Load data for figure 2
load(fullfile(datadir,'example-2.mat'));

%% Plot the graph
gplot(triu(spaugment(L,0)),ABxy,'k--'); hold on;
gplot(A,ABxy(1:size(A,1),:),'b.-');
gplot(B,ABxy(size(A,1)+1:end,:),'r.-'); hold off;
axis equal; axis off; set(gcf,'Color',[1 1 1]);

%%
% Convert to canonical form
[S,w,li,lj] = netalign_setup(A,B,L);
nedges = length(w);

%% Convert to a linear program
[f Alp b]=netalign_lp_prob(S,w,0,1,li,lj);

%%
% Solve with linprog
[ylp,fval,flag] = linprog(-f,Alp,b,[],[],zeros(size(f)),ones(size(f))); flag
% Round the solution
[ma mb xlp weight overlap] = mwmround(ylp(1:nedges), S, w, li, lj); 
%overlap
%weight
    
%% 
% Plot the solution
gplot(triu(spaugment(L,0)),ABxy,'k--'); hold on;
gplot(A,ABxy(1:size(A,1),:),'b.-');
gplot(B,ABxy(size(A,1)+1:end,:),'r.-'); 
gplot(spaugment(sparse(li,lj,xlp,size(L,1),size(L,2))),ABxy,'k-'); hold off;
axis equal; axis off; set(gcf,'Color',[1 1 1]);


%% Solve the problem exactly
xe = netalign_exact(S,w,0,1,li,lj);



%% Load a small example
A = readSMAT(fullfile(datadir,'example-overlap-A.smat'));
B = readSMAT(fullfile(datadir,'example-overlap-B.smat'));
L = readSMAT(fullfile(datadir,'example-overlap-L.smat'));

%% Compute the QP variables
[Se Le] = make_squares(A,B,L);
li = Le(:,1);
lj = Le(:,2);
w = Le(:,3);
S = sparse(Se(:,1),Se(:,2),1,nnz(L),nnz(L));

%% Solve using IsoRank
x=isorank(S,w,1,1,li,lj);

%% Solve usng BP
mbest = netalignbp(S,w,1,1,li,lj);

