function [varargout]=mwmround(x,S,w,li,lj,n,m)
% MWMROUND Round a fractional network alignment solution with maxweight matching
%
% [overlap weight]=mwmround(x,S,w,li,lj,n,m) returns the weight and overlap
% induced by rounding a fractional network alignment indicator to a
% matching.
%
% [ma mb mi weight overlap]=mwmround(x,S,w,li,lj,w,n,m) returns the matching
% information too.
%
% Input:
% x  : the fractional indicator (or solution)
% S  : the matrix of squares indexed for li,lj
% w  : the true weight of each edge (li,lj)
% li : the starting point of each possible edge 
% lj : the ending point of each possible edge
% n  : [optional] the number of row vertices (default:max(li))
% m  : [optional] the number of column vertices (default:max(lj))
%
% Example:
%   % Call with triplet arrays (allows x=0!)
%   load(fullfile('..','data','example-overlap.mat'));
%   x = isorank(S,w,1,1,li,lj);
%   [ma mb mi weight overlap] = mwmround(x,li,lj,max(li),max(lj));
%   fprintf('weight=%g, overlap=%g cardinality=%g', ...
%               weight, overlap, sum(mi));

%  History
%  2009-06-02: Fixed bug with logical S and mi

if ~exist('n','var') || isempty(n), n = max(li); end
if ~exist('m','var') || isempty(m), m = max(lj); end

[val, ma, mb, mi] = bipartite_matching(x,li,lj,n,m);
weight = sum(w(mi)); 
overlap = (mi'*(S*double(mi)))/2; 

if nargout<3, varargout{1} = overlap; varargout{2} = weight; 
else 
    varargout{1} = ma; varargout{2} = mb; varargout{3} = mi; 
    varargout{4} = weight; varargout{5} = overlap; 
end

