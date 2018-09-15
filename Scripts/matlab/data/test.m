n = G.numnodes;
install_percentage = 0.5;
install = randsample(n, ceil(install_percentage*n));
is_susceptible = zeros(n,1);
is_susceptible(install) = 1;
p = 0.2;
full_soc = 30;
niter = 2;
start_node = 3;
%rand_seed = randi(1000);
rand_seed = 932;
rng(rand_seed)
[active, infected] = exp_susceptible_spread(G, start_node, ...
    full_soc, p, is_susceptible, niter);
rng(rand_seed)
exp_d = delta(G, [start_node],p, niter);
[rand_seed, active, infected, exp_d]