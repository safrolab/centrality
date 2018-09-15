function[A] = edgefile2mat(edgefile)
%{
Reads edgefile and returns a sparse matrix
Note: Indexing of edgefile may not necessarily start from 1.

Returns, matrix with MATLAB indexing
%}
formatSpec = '%d %d';
sizeA = [2 Inf];
fileID = fopen(edgefile, 'r');
edges = fscanf(fileID, formatSpec, sizeA);
edges = edges';
[num_edges, ~] = size(edges);
indx = 0;
for i=1:num_edges
    if edges(i, 1) == 0 || edges(i, 2) == 0
        indx = 1;
        break
    end
end
max_nodes = max(edges);
n = max(max_nodes) + indx;
A  = sparse(n,n);
for i=1:num_edges
    s = edges(i,1) + indx;
    t = edges(i,2) + indx;
    A(s,t) = 1;
end
A(A >0 ) =1;
end