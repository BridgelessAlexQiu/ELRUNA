function [S,w,li,lj,A,B,L,extra]=load_netalign_problem(prob)
% LOAD_NETALIGN_PROBLEM Load data for a named network alignment problem
%
% Problems:
%   example-2
%   lcsh2wiki-small
%   lcsh2wiki
%   dmela-scere
%   musm-homo

% Copyright, David F. Gleich 2010
% 

mfilepath=fileparts(mfilename('fullpath'));
rootpath=fileparts(mfilepath);

datadir = fullfile(rootpath,'data');
privatedatadir = fullfile(rootpath,'private_data');

extra = [];

switch prob

    case 'lcsh2wiki-small'
        load(fullfile(privatedatadir,'lcsh2wiki-small.mat'));
        w = lw;
        extra.Alabels = Alabels;
        extra.Blabels = Blabels;

    case 'lcsh2wiki'
        A = readSMAT(fullfile(privatedatadir,'lcsubj-sym.smat'));
        B = readSMAT(fullfile(privatedatadir,'wikipedia-200704-categories-sym.smat'));
        S = readSMAT(fullfile(privatedatadir,'lcsubj2wikipedia-qp-squares.smat'));
        Ldata = load(fullfile(privatedatadir,'lcsubj2wikipedia-qp-squares.edges'));
        li = Ldata(:,1)+1; 
        lj = Ldata(:,2)+1;
        w = Ldata(:,3);
        L = sparse(li,lj,1,size(A,1),size(B,1));
        
    case 'musm-homo'
        load(fullfile(datadir,'natalie_graphs.mat'));
        
    case 'dmela-scere'
        load(fullfile(datadir,'dmela-scere.mat'));
        extra.Liso = Liso;
        
    case 'example-2'
        load(fullfile(datadir,'example-2.mat'));
        [S,w,li,lj] = netalign_setup(A,B,L);
        extra.ABxy = ABxy;

    otherwise
        % just a regular old load
        filename = fullfile(datadir,sprintf('%s.mat',prob));
        if exist(filename,'file')
            load(filename)
        else
            error('netalign:unknownProblem',...
                'the problem %s is not recognized because %s does not exist', ...
                probl, filename)
        end
end
