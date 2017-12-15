function[counter] = exp_traffic_count(G, full_soc, install_dic, ...
    max_time, niter)
n = G.numnodes;
par_counter = zeros(n, niter);

parfor i = 1:niter
    start_node = randi(n);
    par_counter(:,i) = par_counter(:,i) + traffic_count(G, start_node, full_soc,...
        install_dic, max_time);
end
counter = par_counter*ones(niter, 1);
end