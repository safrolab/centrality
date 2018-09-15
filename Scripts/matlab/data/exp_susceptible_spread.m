function[active, infected] = exp_susceptible_spread(G, start_node, ...
    full_soc, p, is_susceptible, niter)

active = zeros(niter, 1);
infected = zeros(niter, 1);
parfor i = 1:niter
   [num_active, num_infected] =  ...
       susceptible_spread(G, start_node, full_soc, p, is_susceptible);
   active(i) = num_active;
   infected(i) = num_infected;
end

active = sum(active)/niter;
infected = sum(infected)/niter;

end