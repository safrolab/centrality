function[coverage] = infection_cascade_mod(G, init_active,p)
n = G.numnodes;
active_nodes = zeros(n,1);
active_nodes(init_active) = 1;
[num, ~] = size(init_active);
newly_active = [init_active, zeros(1, n-num)];
while num > 0
    [newly_active, active_nodes, num] = ICM_time_step(G,active_nodes,newly_active,num, p,n);
end
coverage = nnz(active_nodes);
end