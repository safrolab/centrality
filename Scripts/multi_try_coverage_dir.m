function[coverage, active_nodes] = multi_try_coverage_dir(G, init_active,p, immune, full_soc, install)

%%G is a directed graph

n = G.numnodes;
active_nodes = zeros(n,1);
active_nodes(init_active) = 1;
soc = zeros(n,1);
soc(init_active) = full_soc;
soc(install) = full_soc;
has_spread = zeros(n,1);
[num, ~] = size(init_active);
newly_active = [init_active, zeros(1, n-num)];
is_immune = zeros(n,1);
%is_immune(immune) = 1;
while num > 0
    [newly_active, soc,active_nodes, has_spread, num] = ...
    MT_time_step(G,soc, active_nodes,newly_active, is_immune,has_spread, num, p,n); 
end
coverage = nnz(active_nodes);

end