function[soc_cover, katz_cover, deg_cover, random_cover, ...
    top_kaz, top_soc_k, top_deg, install, test_nodes] = experiment_1(G,A)

%{ 
Experiment to compare immunization strategies
Compare coverage for random start node
1. Compute Katz, exp_soc_katz, and degree centralities
2. Immunize tmatop-m nodes. Remove them from graph
3. Install k nodes at random
4. Pick random node, u, that belongs to all 3 graphs
5. Compute expected coverage Exp_cov(u)
6. Repeat 3 - 5, niter times
%}
% katz, soc_katz
A(A>0) = 1;
[~, n] = size(A);
%P = speye(n);
%P = P(randperm(n),:);
%A = P*A*P';
steps = 3;
num_immunize = 100;
install_percentage = 0.1;
niter = 1;
katz = Katz(A);
exp_soc_katz = Exp_SOC_Katz(A, steps, install_percentage, niter);
deg_cen = G.outdegree;
%scatter(exp_soc_katz, katz)

%Top nodes
[~, katz_order] = sort(katz,'descend');
[~, soc_katz_order] = sort(exp_soc_katz,'descend');
[~, deg_order] = sort(deg_cen,'descend');
top_kaz = katz_order(1:num_immunize);
top_soc_k = soc_katz_order(1:num_immunize);
top_deg = deg_order(1:num_immunize);
top_random = randsample(1:n, num_immunize);
no_start = zeros(n,1);
no_start(top_kaz) = 1;
no_start(top_soc_k) = 1;
no_start(top_deg) = 1;

%Immunize
ntrials = 20;
niter2 = 1;
soc_cover = zeros(ntrials,1);
katz_cover = zeros(ntrials, 1);
deg_cover = zeros(ntrials, 1);
random_cover = zeros(ntrials, 1);
possible_install_nodes = find(~no_start);
%num_install = ceil(install_percentage*n);
num_install = 1;
[max_install_size, ~] = size(possible_install_nodes); 
%perm = randperm(num_immunize,num_install);
perm = randperm(max_install_size,num_install);
install = possible_install_nodes(perm);

test_nodes = zeros(ntrials, 1);
steps = 10;
[steps,steps, steps]

parfor i=1:ntrials
    node = randi(n);
    if no_start(node) == 0
        [i,i]
        test_nodes(i) = node;
        [soc_cover_val, ~] = delta_soc(G, [node], 1, top_soc_k, steps, niter2, install);
        [katz_cover_val, ~] = delta_soc(G, [node], 1, top_kaz, steps, niter2, install);
        [deg_cover_val, ~] = delta_soc(G, [node], 1, top_deg, steps, niter2, install);
        [rand_cover_val,~] = delta_soc(G, [node], 1, top_random, steps, niter2, install);
        soc_cover(i) = soc_cover_val;
        katz_cover(i) = katz_cover_val;
        deg_cover(i) = deg_cover_val;
        random_cover(i) = rand_cover_val;
    end
end
soc_cover = soc_cover(soc_cover~=0);
katz_cover = katz_cover(katz_cover~=0);
deg_cover = deg_cover(deg_cover~=0);
random_cover = random_cover(random_cover~=0);
test_nodes = test_nodes(test_nodes ~=0);

end