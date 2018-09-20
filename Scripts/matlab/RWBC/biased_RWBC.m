%biased RWBC
%%
A = [0 1 1 1 0 0 0 0 0 0 0
    1 0 1 0 1 0 0 0 0 0 0
    1 1 0 1 0 1 0 0 0 0 0
    1 0 1 0 0 0 1 0 0 0 0
    0 1 0 0 0 1 0 1 0 0 0
    0 0 1 0 1 0 1 0 1 0 0
    0 0 0 1 0 1 0 0 0 1 0
    0 0 0 0 1 0 0 0 1 0 1
    0 0 0 0 0 1 0 1 0 1 1
    0 0 0 0 0 0 1 0 1 0 1
    0 0 0 0 0 0 0 0 0 0 0];
t = 11;
n = 11;
A = sparse(A);
%%
A = [0 1 0 
    1 0 1
    0 0 0];
t = 3;

%%
A = [0 1 0 0 0 0 0 0
    0 0 1 0 0 0 0 0 
    0 1 0 1 0 0 0 0 
    0 0 0 0 1 0 0 0
    0 0 0 0 0 1 1 0
    0 0 0 1 0 0 0 0
    0 0 0 0 0 0 0 1
    0 0 0 0 0 0 0 0];
[~,n] = size(A);
t = n;
A = sparse(A);
%%
A = [0 1 1 1 1 0 0 0 0 0
    1 0 1 1 1 1 0 0 0 0 
    1 1 0 1 1 0 0 0 0 0
    1 1 1 0 1 0 0 0 0 0 
    1 1 1 1 0 0 0 0 0 0
    0 1 0 0 0 0 1 1 1 1
    0 0 0 0 0 1 0 1 1 1
    0 0 0 0 0 1 1 0 1 1
    0 0 0 0 0 1 1 1 0 1
    0 0 0 0 0 0 0 0 0 0];
[~,n] = size(A);
t = n;
A = sparse(A);
%%
A =[0 1 0 0 0 0 0 0
   0 0 1 0 1 0 0 0
   1 0 0 1 0 0 0 0
   0 1 0 0 1 0 0 0
   0 0 0 0 0 1 1 0
   0 0 0 0 0 0 0 1
   0 0 0 0 0 1 0 1
   0 0 0 0 0 0 0 0];
[~,n] = size(A);
t = n;
%%
A = sparse(A);
dist = graphshortestpath(A', t) + 1;
%dist = ones(n,1);
W = diag(dist.^(-1));
A = A*W;
%%
[~,n] = size(A);
D = diag(A*ones(n,1));
A_t = A;
D_t = D;
D_t(t,:) = [];
D_t(:,t) = [];
A_t(t,:) = [];
A_t(:,t) = [];
D_t_inv = D_t^(-1);
D(t,t) = 1;
D_inv = D^(-1);
D_inv(t,t)  = 0;
M = D_inv*A;
M_t = D_t\A_t;
I_t = speye(n-1);

T_t = (I_t - M_t)\speye(n-1,n-1);
s = zeros(1,n);
s(1) = 1;
T  = zeros(n,n);
T(1:n-1, 1:n-1) = T_t;
r = s*T;
r(t) = 1;
R = spdiags([r'], 0, n,n);
flow = R*M;
%cen = s*TA;
%T_t = (I_t - M_t)\D_t_inv;
%T = zeros(n,n);
%T(1:n-1,1:n-1)= TA_t;
%F = diag(s*TA);
%flow = F*M;
G = digraph(flow);
plot(G,'EdgeLabel',G.Edges.Weight)
%%
[~,n] = size(A);
D = diag(A*ones(n,1));
L = D - A;
L_t = L;
L_t(n,:) = [];
L_t(:,n) = [];
T_t = L_t^(-1);
T = zeros(n,n);
T(1:n-1,1:n-1)= T_t;
s = zeros(1,n);
s(1) = 1;
F = diag(s*T);
flow = F*A;
G = digraph(flow);
plot(G,'EdgeLabel',G.Edges.Weight)