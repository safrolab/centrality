% 
A = Problem.A;
A(A>0) = 1;
G = graph(A);
n = G.numnodes;
p = 0.1;
delta_all_nodes = zeros(n,1);
niter = 1000;

for i=1:n
    init_active = [i];
    d = delta(G, init_active,p, niter);
    delta_all_nodes(i) = d;
    [i,d]
end