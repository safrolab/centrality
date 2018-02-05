function [centrality] = st_biased_random_walk_BC(A, n, s, t)
%This function assumes the following:
%   1) A is a sparse matrix
%   2) Every node has finite distance to node t
% dist = graphshortestpath(A', t) + 1;
%dist_inv = dist.^(-1);
%dist_inv = exp(-dist);
%dist = ones(1,n);
%dist_inv = dist;

%W = spdiags([dist_inv'], 0, n,n);
%A = A*W;
%A = A.*dist_inv; %A = A*W;
d = A*ones(n,1);
%d(t) = 1;
%d_inv = d.^(-1);
%M = A.*d_inv;
D = spdiags([d], 0, n,n);
D(t,t) = 1;
M = D\A;
A_t = A;
%d_inv_t = d;
%d_inv_t(t) = [];
D_t = D;
D_t(t,:) = [];
D_t(:,t) = [];
A_t(t,:) = [];
A_t(:,t) = [];

ss = sparse(n,1);
ss(s) = 1;
ss_t = ss;
ss_t(t) = [];

D_t_inv = D_t^(-1);
M_t = D_t\A_t;
%M_t = A_t.*d_inv_t;
I_t = speye(n-1);

V_t = (I_t - M_t')\ss_t;
V = sparse(n,1);
if t == 1
    V(2:n) = V_t;
elseif t == n
    V(1:n-1) = V_t;
else
    V(1:t-1) = V_t(1:t-1);
    %Z(1:t-1, t+1:n) = Z_t(1:t-1, t:n-1);
    V(t+1:n) = V_t(t:n-1);
    %Z(t+1:n, t+1:n) = Z_t(t:n-1, t:n-1);
end
%{
Z_t = (I_t - M_t)\speye(n-1,n-1);
s_index = sparse(1,n);
s_index(s) = 1;
Z  = sparse(n,n);
if t == 1
    Z(2:n-1, 2:n-1) = Z_t;
elseif t == n
    Z(1:n-1, 1:n-1) = Z_t;
else
    Z(1:t-1, 1:t-1) = Z_t(1:t-1, 1:t-1);
    Z(1:t-1, t+1:n) = Z_t(1:t-1, t:n-1);
    Z(t+1:n, 1:t-1) = Z_t(t:n-1, 1:t-1);
    Z(t+1:n, t+1:n) = Z_t(t:n-1, t:n-1);
end

V = s_index*Z;
%}
D_V = spdiags([V], 0, n,n);
flow_mat = D_V*M;
%flow_mat = M.*V;
%G = digraph(flow_mat);
%plot(G,'EdgeLabel',G.Edges.Weight)
net_flow_mat = abs(flow_mat - flow_mat');
centrality = 0.5*net_flow_mat*ones(n,1);
%centrality = (s_index*TA)';
centrality(s) = 1;
centrality(t) = 1;
%{
T_t = (I_t - M_t)\D_t_inv;
T = zeros(n,n);
T(1:n-1,1:n-1)= T_t;
F = diag(s_index*T);
flow = F*A;
G = digraph(flow);
plot(G,'EdgeLabel',G.Edges.Weight)
%}
end