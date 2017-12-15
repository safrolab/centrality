function[node_congestion] = experiment_3(G,A)

%{ 
Experiment to identify congested nodes
1. Pick random k installation
2. Compute SOC_katz, katz, and degree
3. Apply particle tracking model with given k installation
4. Compute average congestion of each node, by running (3) niter times
5. Compare ranking
%}
% katz, soc_katz
A(A>0) = 1;
[~, n] = size(A);
%P = speye(n);
%P = P(randperm(n),:);
%A = P*A*P';
install_percentage = 0.05;
num_labelled_nodes = ceil(install_percentage*n);
install = randperm(n,num_labelled_nodes);
full_soc = 3;
katz = Katz(A);
soc_katz = SOC_Katz_install_nodes(A, full_soc,num_labelled_nodes, install);
deg_cen = G.outdegree;

%Top nodes
[~, katz_order] = sort(katz,'descend');
[~, soc_katz_order] = sort(soc_katz,'descend');
[~, deg_order] = sort(deg_cen,'descend');


%compute congestion

niter = 100;
num_time_steps = 100;
num_new_particles = ceil(0.1*n);
total_congestion = zeros(n, niter);
for i=1:niter
   new_particles = randsample(1:n, num_new_particles);
   counter = congestion(G, new_particles, full_soc, install, num_time_steps);
   total_congestion(:,i) = counter;
    
end

node_congestion = total_congestion*ones(niter,1);
scatter(node_congestion, soc_katz)

end