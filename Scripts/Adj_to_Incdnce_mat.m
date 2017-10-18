function[Incidence_mat, abs_Inc] = Adj_to_Incdnce_mat(Adj)

[~, n] = size(Adj);

%Remove double edges must be a single edge
m =nnz(Adj);
C = Adj - 0.3*Adj';
L = tril(C);
L(L<0.5) = 0;
L(L>0.9) = 0;
L(L>0.5) = 1;
Adj = Adj - L;
Adj(Adj < 1) = 0;
m =nnz(Adj);
Incidence_mat = sparse(n,m);
abs_Inc = sparse(n,m);
[row, col] = find(Adj);
edge_indx = [row,col];

%this is a slow way to build the matrix
%for efficiency this must be changed

for edge=1:m
    from = edge_indx(edge, 1);
    to = edge_indx(edge, 2);
    
    Incidence_mat(from, edge) = 1;
    Incidence_mat(to, edge) = -1;
    abs_Inc(from, edge) = 1;
    abs_Inc(to, edge) = 1;
end
