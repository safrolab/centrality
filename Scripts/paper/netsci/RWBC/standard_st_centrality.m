function [ centrality ] = standard_st_centrality( A, source, terminal )
%STANDARD_ST_CENTRALITY Summary of this function goes here
%   Detailed explanation goes here
% input, adjancency matrix, source node, terminal node
% Returns the centrality score for this s - t pair

A(A > 0) = 1;
n = max(size(A));

I = speye(n);
D = A*ones(n,1);
D = diag(D);
L = sparse(D - A);
L_t = L;
L_t(terminal,:) = [];
L_t(:,terminal) = [];      
s = zeros(n-1, 1);
if source < terminal
    s(source) = 1;
else
    s(source-1) = 1;
end
V_t = L_t\s;
V = sparse(n,1);
V(1:terminal-1) = V_t(1:terminal-1);
V(terminal) = 0;
if terminal +n < n
    V(terminal+1:n) = V_t(terminal:n-1);
end
D_V = spdiags([V], 0, n,n);
flow_mat = D_V*A;
%G = digraph(flow_mat);
%plot(G,'EdgeLabel',G.Edges.Weight)
net_flow_mat = abs(flow_mat - flow_mat');
centrality = 0.5*net_flow_mat*ones(n,1);
centrality(source) = 1;
centrality(terminal) = 1;

end

