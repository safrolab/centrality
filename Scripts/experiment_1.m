function[deg_cen] = experiment_1(G,A)
%{ 
Experiment to compare immunization strategies
Compare coverage for random start node
1. Compute Katz, exp_soc_katz, and degree centralities
2. Immunize top-m nodes. Remove them from graph
3. Install k nodes at random
4. Pick random node, u, that belongs to all 3 graphs
5. Compute expected coverage Exp_cov(u)
6. Repeat 3 - 5, niter times
%}
% katz, soc_katz
A(A>0) = 1;
steps = 3;
install_percentage = 0.05;
niter = 10000;
katz = Katz(A);
exp_soc_katz = Exp_SOC_Katz(A, steps, install_percentage, niter);
deg_cen = G.outdegree;
scatter(katz, exp_soc_katz)
end