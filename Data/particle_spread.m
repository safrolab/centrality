function[node_coverage] = ...
    particle_spread(G, start_node, full_soc, install_dic, max_time)


%%G is a directed graph

n = G.numnodes;
current_soc = full_soc;
visited = zeros(n,1);
visited(start_node) = 1;
current_node = start_node;

for i=1:max_time
    if current_node > 0
        [current_soc, current_node, visited] = ...
            particle_spread_time_step(G, current_soc, full_soc,...
            current_node, visited,install_dic); 
   elseif current_node == -1
       break
    end    
end

node_coverage = nnz(visited);
end