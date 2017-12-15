function[visit_count] = ...
    traffic_count(G, start_node, full_soc, install_dic, max_time)


%%G is a directed graph

n = G.numnodes;
current_soc = full_soc;
visit_count = zeros(n,1);
visit_count(start_node) = 1;
current_node = start_node;

for i=1:max_time
    if current_node > 0
        [current_soc, current_node, visit_count] = ...
            traffic_count_time_step(G, current_soc, full_soc,...
            current_node, visit_count,install_dic); 
   elseif current_node == -1
       break
    end    
end

end