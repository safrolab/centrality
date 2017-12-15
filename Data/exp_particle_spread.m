function[exp_spread] = exp_particle_spread(G, start_node, full_soc,...
 install_dic, max_time, niter)

spread = zeros(niter, 1);
max_time = G.numnodes;
for i = 1:niter
    spread(i) = particle_spread(G, start_node, full_soc, ...
                                install_dic, max_time);
end
exp_spread = sum(spread)/niter;

end